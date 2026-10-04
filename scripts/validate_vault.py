#!/usr/bin/env python3
"""Read-only structural checks for legal-knowledge-base v2 notes (requires PyYAML)."""
import argparse
import datetime as dt
import json
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML is unavailable; use an environment with PyYAML or perform the documented manual checks.")

COMMON = {"schema_version", "类型", "整理状态", "核验状态", "核验日期", "所属专题", "来源"}
EXTRA = {
    "配置": {"学科", "法域", "时间范围", "学科路径", "使用目的", "汇总方式"},
    "导航": set(),
    "概念": {"关联法条", "关联概念"},
    "规范": {"规范名称", "规范性质", "条款定位", "法域", "版本", "发布日期", "施行日期", "施行状态", "关联法条"},
    "案例": {"文书编号", "作出机关", "作出日期", "材料类型", "程序状态", "关联法条", "关联概念"},
    "专题": {"关联法条", "关联概念"},
    "产出": {"使用目的", "交付形式", "依据卡片", "关联法条", "关联概念"},
    "反馈": {"使用目的", "反馈状态", "反馈来源", "反馈日期", "依据卡片"},
    "来源": set(),
}
RELATIONS = ("所属专题", "关联法条", "关联概念", "依据卡片")
TARGET_TYPES = {"所属专题": "专题", "关联法条": "规范", "关联概念": "概念"}
WORK = {"待整理", "进行中", "已整理", "已归档"}
CHECK = {"待核验", "部分核验", "已核验", "待复核", "不适用"}
LEGAL = {"待核验", "现行有效", "尚未生效", "已废止", "已失效", "已被取代", "草案", "不适用"}
FEEDBACK = {"待反馈", "已记录", "已修订", "已验证"}
WIKI = re.compile(r"\[\[([^\[\]\n]+)\]\]")


def excluded(path):
    return any(part.startswith(".") or part == "99-Templates" for part in path.parts)


def visible_body(body):
    # Ignore example links inside fenced code or comments; preserve actual lists.
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    output, fence = [], None
    for line in body.splitlines():
        mark = re.match(r"^\s*(`{3,}|~{3,})", line)
        if mark:
            token = mark.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            output.append(line)
    return "\n".join(output)


def parse_note(path):
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data, text[match.end():]


def valid_date(value):
    if isinstance(value, dt.date) and not isinstance(value, dt.datetime):
        return True
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            dt.date.fromisoformat(value)
            return True
        except ValueError:
            pass
    return False


def validate(vault, subject):
    vault = Path(vault).resolve()
    scope = (vault / subject).resolve()
    if not vault.is_dir() or not scope.is_dir() or not scope.is_relative_to(vault):
        raise ValueError("vault and subject must exist; subject must be inside the vault")
    if Path(subject).is_absolute():
        raise ValueError("--subject must be a vault-relative path (use . for the whole vault)")
    issues, notes, parsed = [], {}, {}

    def issue(level, path, message):
        issues.append({"level": level, "file": str(path.relative_to(vault)), "message": message})

    # Inventory paths across the vault for unambiguous resolution; read only scoped or referenced notes.
    by_path, by_name = {}, {}
    for path in vault.rglob("*.md"):
        rel = path.relative_to(vault)
        if excluded(rel) or not path.resolve().is_relative_to(vault):
            continue
        by_path[rel.with_suffix("").as_posix()] = path
        by_name.setdefault(path.stem, []).append(path)

    def resolve(raw, origin):
        target = raw.split("|", 1)[0].split("#", 1)[0]
        if not target:
            return origin  # body links to headings in the current note
        target = target.removesuffix(".md")
        if target in by_path:
            return by_path[target]
        if "/" not in target and len(by_name.get(target, [])) == 1:
            return by_name[target][0]
        issue("error", origin, f"unresolved or ambiguous wikilink: [[{raw}]]")
        return None

    for path in by_path.values():
        if not path.is_relative_to(scope):
            continue
        try:
            data, body = parse_note(path)
        except (ValueError, yaml.YAMLError, OSError) as exc:
            issue("error", path, str(exc))
            continue
        if data.get("schema_version") != 2:
            issue("error", path, "not a v2 note; map legacy schemas before running this checker")
            continue
        kind = data.get("类型")
        if not isinstance(kind, str) or kind not in EXTRA:
            issue("error", path, "unknown 类型")
            continue
        for field in sorted(COMMON | EXTRA[kind]):
            if field not in data:
                issue("error", path, f"missing field: {field}")
        for field, choices in (("整理状态", WORK), ("核验状态", CHECK)):
            if not isinstance(data.get(field), str) or data.get(field) not in choices:
                issue("error", path, f"invalid {field}: {data.get(field)!r}")
        for field in ("核验日期", "发布日期", "施行日期", "作出日期", "反馈日期"):
            if data.get(field) not in (None, "") and not valid_date(data[field]):
                issue("error", path, f"invalid date in {field}")
        if data.get("核验状态") == "已核验" and not valid_date(data.get("核验日期")):
            issue("error", path, "已核验 requires an actual 核验日期")
        for field in ("来源", "使用目的"):
            if field in data and (not isinstance(data[field], list) or not all(isinstance(x, str) and x.strip() for x in data[field])):
                issue("error", path, f"{field} must be a list of nonempty strings")
        if kind in {"概念", "规范", "案例", "产出"} and data.get("核验状态") == "不适用":
            issue("error", path, "knowledge and legal-output notes need an explicit verification state")
        if kind in {"概念", "规范", "案例"} and not data.get("来源"):
            level = "error" if data.get("核验状态") == "已核验" else "warning"
            issue(level, path, "source evidence is missing")
        if kind == "规范" and (not isinstance(data.get("施行状态"), str) or data.get("施行状态") not in LEGAL):
            issue("error", path, "invalid 施行状态")
        if kind == "反馈":
            if not isinstance(data.get("反馈状态"), str) or data.get("反馈状态") not in FEEDBACK:
                issue("error", path, "invalid 反馈状态")
            if isinstance(data.get("反馈状态"), str) and data.get("反馈状态") in FEEDBACK - {"待反馈"} and (not data.get("反馈来源") or not valid_date(data.get("反馈日期"))):
                issue("error", path, "recorded feedback requires a source and date")
        if kind in {"配置", "产出", "反馈"} and not data.get("使用目的"):
            issue("error", path, "使用目的 must contain at least one purpose")
        if kind in {"概念", "案例"} and not data.get("所属专题"):
            issue("error", path, "concept/case must belong to a topic")
        if kind in {"产出", "反馈"} and not data.get("依据卡片"):
            issue("error", path, "output/feedback must link its evidence or reviewed target")
        if "{{" in body or any("{{" in str(value) for value in data.values()):
            issue("error", path, "unrendered template parameter in a live note")
        links = set()
        for raw in WIKI.findall(visible_body(body)):
            target = resolve(raw, path)
            if target:
                links.add(target)
        relations = {}
        for field in RELATIONS:
            if field not in data:
                continue
            values = data[field]
            if not isinstance(values, list):
                issue("error", path, f"{field} must be a wikilink list")
                continue
            relations[field] = set()
            for value in values:
                match = WIKI.fullmatch(value) if isinstance(value, str) else None
                if not match:
                    issue("error", path, f"{field} contains a non-wikilink value: {value!r}")
                    continue
                raw = match.group(1)
                target = resolve(raw, path)
                if target:
                    canonical = target.relative_to(vault).with_suffix("").as_posix()
                    if raw != canonical:
                        issue("error", path, f"{field} requires canonical link [[{canonical}]]")
                    relations[field].add(target)
        notes[path] = (data, body, links, relations)
        parsed[path] = data

    for path, (data, body, links, relations) in notes.items():
        for field, targets in relations.items():
            for target in targets:
                if target not in parsed:
                    try:
                        parsed[target] = parse_note(target)[0]
                    except (ValueError, yaml.YAMLError, OSError):
                        parsed[target] = {}
                expected = TARGET_TYPES.get(field)
                if expected and parsed[target].get("类型") != expected:
                    issue("error", path, f"{field} target is not 类型={expected}: {target.name}")
                if target not in links:
                    issue("error", path, f"missing visible link for {field}: {target.name}")
                if target in notes:
                    target_data, _, target_links, _ = notes[target]
                    needs_reverse = field in {"所属专题", "依据卡片"} or (field == "关联法条" and data["类型"] != "规范")
                    if needs_reverse and path not in target_links:
                        issue("error", target, f"missing member/reverse link to {path.name} ({field})")
        if data["类型"] == "专题":
            for member in links:
                if member in notes and notes[member][0]["类型"] not in {"专题", "导航", "配置", "反馈"}:
                    if path not in notes[member][3].get("所属专题", set()):
                        issue("warning", path, f"linked note is not registered as a member; mark it as adjacent if intentional: {member.name}")

    if not notes:
        issue("error", scope, "no v2 notes were checked; an empty scope is not a validated library")
    return {"vault": str(vault), "subject": str(scope.relative_to(vault)), "notes_checked": len(notes),
            "errors": sum(x["level"] == "error" for x in issues),
            "warnings": sum(x["level"] == "warning" for x in issues), "issues": issues,
            "limits": "Structure only; legal accuracy, source accessibility, and live Dataview rendering are not tested."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True)
    parser.add_argument("--subject", required=True)
    args = parser.parse_args()
    try:
        result = validate(args.vault, args.subject)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
