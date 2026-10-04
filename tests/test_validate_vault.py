"""Exercise real templates and broken relationship graphs in isolated temporary vaults."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate_vault.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class VaultChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="legal-skill-test-")
        self.addCleanup(self.tmp.cleanup)
        self.vault = Path(self.tmp.name)
        self.subject = "测试学科"
        self.files = {
            "配置": "00-建库配置", "导航": "00-学科导航",
            "来源": "00-Inbox/来源清单", "规范": "01-法规层/测试规范",
            "案例": "02-案例层/测试案例", "概念": "03-专题层/概念卡/测试概念",
            "专题": "03-专题层/MOC-测试主题", "产出": "06-产出物/测试成果",
            "反馈": "07-反馈与迭代/测试反馈",
        }
        templates = {"配置": "建库配置", "导航": "学科导航", "来源": "来源索引", "专题": "专题MOC", "反馈": "反馈记录"}
        for kind, relative in self.files.items():
            name = templates.get(kind, kind + "卡")
            text = (ROOT / "assets/templates" / (name + ".md")).read_text()
            for key, value in {"title": Path(relative).name, "subject": self.subject,
                               "subject_path": self.subject, "jurisdiction": "测试法域（非真实法律）",
                               "time_scope": "测试时间"}.items():
                text = text.replace("{{" + key + "}}", value)
            path = self.path(kind)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            data, _ = validator.parse_note(path)
            # Synthetic sources only; no assertion of real legal verification.
            if kind in {"规范", "案例", "概念"}:
                data["来源"] = ["测试材料：非真实法律来源"]
            if kind in {"规范", "案例", "概念", "产出", "反馈"}:
                data["所属专题"] = [self.link("专题")]
            if kind in {"案例", "概念"}:
                data["关联法条"] = [self.link("规范")]
            if kind == "产出":
                data["依据卡片"] = [self.link("规范"), self.link("案例"), self.link("概念")]
            if kind == "反馈":
                data["依据卡片"] = [self.link("产出")]
            members = {
                "规范": ["专题", "案例", "概念", "产出"],
                "案例": ["专题", "规范", "产出"],
                "概念": ["专题", "规范", "产出"],
                "专题": ["规范", "案例", "概念", "产出", "反馈"],
                "产出": ["专题", "规范", "案例", "概念", "反馈"],
                "反馈": ["专题", "产出"],
                "导航": ["专题"],
            }.get(kind, [])
            body = "# 结构测试样例\n\n不表达真实法律判断。\n\n## 关联笔记\n" + "\n".join("- " + self.link(x) for x in members)
            self.write(kind, data, body)

    def path(self, kind):
        return self.vault / self.subject / (self.files[kind] + ".md")

    def link(self, kind):
        return "[[" + self.subject + "/" + self.files[kind] + "]]"

    def write(self, kind, data, body):
        self.path(kind).write_text("---\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False) + "---\n" + body)

    def change(self, kind, transform):
        data, body = validator.parse_note(self.path(kind))
        result = transform(data, body)
        self.write(kind, *(result if result else (data, body)))

    def report(self):
        return validator.validate(self.vault, self.subject)

    def messages(self):
        return "\n".join(x["message"] for x in self.report()["issues"])

    def test_templates_form_a_connected_library_without_plugins(self):
        result = self.report()
        self.assertEqual(9, result["notes_checked"])
        self.assertEqual([], result["issues"])

    def test_purposes_can_coexist_and_change_without_duplicate_cards(self):
        for purposes in (["教学"], ["法务实务"], ["考试"], ["探索"], ["教学", "法务实务"]):
            for kind in ("配置", "产出", "反馈"):
                self.change(kind, lambda data, body: data.update(使用目的=purposes))
            self.assertEqual(0, self.report()["errors"])
            self.assertEqual(9, self.report()["notes_checked"])

    def test_body_heading_does_not_replace_metadata(self):
        self.change("案例", lambda data, body: (data, body + "\n## 关联法条\n" + self.link("规范")))
        def remove_field(data, body):
            del data["关联法条"]
        self.change("案例", remove_field)
        self.assertIn("missing field: 关联法条", self.messages())

    def test_plain_title_cannot_masquerade_as_link_object(self):
        self.change("案例", lambda data, body: data.update(所属专题=["MOC-测试主题"]))
        self.assertIn("non-wikilink", self.messages())

    def test_missing_reverse_case_is_reported(self):
        self.change("规范", lambda data, body: (data, body.replace(self.link("案例"), "")))
        self.assertIn("missing member/reverse link", self.messages())

    def test_topic_link_requires_a_topic_target(self):
        self.change("案例", lambda data, body: data.update(所属专题=[self.link("概念")]))
        self.assertIn("target is not 类型=专题", self.messages())

    def test_output_requires_evidence(self):
        self.change("产出", lambda data, body: data.update(依据卡片=[]))
        self.assertIn("output/feedback must link", self.messages())

    def test_verified_rules_require_sources_and_actual_date(self):
        self.change("规范", lambda data, body: data.update(核验状态="已核验", 来源=[]))
        self.assertIn("source evidence is missing", self.messages())
        self.assertIn("actual 核验日期", self.messages())

    def test_recorded_feedback_needs_evidence_but_pending_does_not(self):
        self.assertEqual(0, self.report()["errors"])
        self.change("反馈", lambda data, body: data.update(反馈状态="已验证"))
        self.assertIn("recorded feedback requires", self.messages())

    def test_ambiguous_short_names_fail_but_canonical_paths_work(self):
        other = self.vault / "其他学科/测试规范.md"
        other.parent.mkdir()
        other.write_text("# 只用于歧义测试")
        self.assertEqual(0, self.report()["errors"])
        self.change("案例", lambda data, body: (data, body + "\n[[测试规范]]"))
        self.assertIn("unresolved or ambiguous", self.messages())

    def test_legacy_and_empty_scopes_are_not_silently_validated(self):
        self.change("案例", lambda data, body: data.update(schema_version=1))
        self.assertIn("not a v2 note", self.messages())
        (self.vault / "空库").mkdir()
        self.assertGreater(validator.validate(self.vault, "空库")["errors"], 0)

    def test_scope_cannot_escape_vault(self):
        with self.assertRaises(ValueError):
            validator.validate(self.vault, "..")

    def test_invalid_yaml_field_types_are_reported(self):
        self.change("案例", lambda data, body: data.update(类型=["案例"]))
        self.assertIn("unknown 类型", self.messages())

    def test_template_directory_is_excluded(self):
        path = self.vault / self.subject / "99-Templates/未渲染.md"
        path.parent.mkdir()
        path.write_text("{{title}} [[不存在]]")
        self.assertEqual(0, self.report()["errors"])


if __name__ == "__main__":
    unittest.main()
