# Legal knowledge base skill

[中文 README](README.md) · [English skill](SKILL.md) · [中文 Skill](SKILL.zh-CN.md)

Tell the assistant which legal field you want to learn. It builds an Obsidian subject map, linked concepts, rules, cases and topics, then adapts outputs to teaching, legal practice, exams, research or exploration.

This is an AI workflow, not an Obsidian plugin. Version 2 supports starting without a prepared source collection or a precise research question.

## Start here

After installation, send this in Codex:

```text
Use $legal-knowledge-base. I want to learn AI data compliance
for legal work at companies in mainland China.
Create a separate subject library inside my Obsidian vault.
Start with a subject map and one usable introductory topic.
My vault path is: insert the actual path.
```

If you have not chosen a purpose, simply name the legal field. The assistant uses available context to establish the location and jurisdiction, starts in exploratory mode and lets the purpose change later. Supply textbooks, syllabi, PDFs, Word files or exam materials when available. Extraction/OCR depends on the available tools; unreadable material remains explicitly pending.

## What it produces

- Configuration: subject, jurisdiction, time scope, purposes, path and requested coverage.
- Navigation: core questions, prerequisites, topic relationships, sequence, existing notes and missing sources.
- Source-linked concepts, rules, cases and topic notes with navigable relationships.
- Purpose-specific outputs, with feedback records when actual evidence is available.
- Structural checks, current coverage and the next useful step.

A first batch contains connected substantive content, not a claim of exhaustive coverage. Missing sources remain visible.

## Purposes and feedback

| Purpose | Possible outputs | Feedback evidence |
|---|---|---|
| Teaching | Lecture sequence, slide outline, discussion prompts and source notes | Rehearsal, user review, learner questions |
| Legal practice | Issue analysis, review checklist, process or assessment workpaper | Trial use with materials, business/legal review |
| Exams | Syllabus map, exercises, explanations and error analysis | Actual answers, marking criteria, errors |
| Research/exploration | Concept distinctions, literature/question maps, research notes | Follow-up questions, counterexamples, use attempts |

Purposes can overlap or change. The workflow does not impose exams or infer mastery from generated notes. Missing feedback does not block library construction. A Markdown slide outline is not a PPTX file; producing an actual presentation requires appropriate file-generation capability.

## Legal database connectors: mandatory pre-retrieval check

Before retrieving statutes or cases, check MCP discovery for Wolters Kluwer China Law & Reference (威科先行), PKULaw (北大法宝) and comparable legal databases. Verify exposed, authorized capabilities with a read-only operation and prioritize relevant working connectors. If absent or inaccessible, explain the limitation and continue through official sources. A discovered tool is not proof of connectivity; search access is not full-text access.

Record the check and actual sources in the configuration and source inventory. The skill does not include database credentials or automatically activate subscriptions. See the [connector procedure](references/legal-source-connectors.md).

## Structure and links

One Obsidian vault can contain several sibling subject libraries. The core consists of sources, rules, cases, topics (including concept cards) and selected templates. Teaching, practice, other outputs and feedback folders are enabled when useful. Existing conventions are preserved.

A topic map (MOC) is a navigation note. Frontmatter is the metadata at the top of a note. Wikilinks use Obsidian's `[[note path]]` notation.

Version 2 uses consistent metadata link lists and visible indexes. Rules link back to cases, topics list their members and outputs cite supporting cards. Dataview is optional; explicit lists work without it.

## Install in Codex

Copy the whole folder to `~/.codex/skills/legal-knowledge-base/` or your configured `$CODEX_HOME/skills/legal-knowledge-base/`. If the download folder has a suffix such as “开源版”, name the installed folder `legal-knowledge-base` and preserve its contents.

On macOS, Finder's “Go to Folder” accepts the location above. Reload available skills, then invoke `$legal-knowledge-base` in Codex.

```text
legal-knowledge-base/
├── SKILL.md / SKILL.zh-CN.md
├── README.md / README.en.md
├── agents/openai.yaml
├── references/
├── assets/templates/
├── scripts/validate_vault.py
└── tests/
```

References and note templates are currently in Chinese. The English and Chinese entrypoints share the same field contract rather than generating incompatible schemas.

## Validation and existing libraries

The optional read-only helper requires Python 3.9+ and PyYAML. Run from the skill directory:

```sh
python3 scripts/validate_vault.py --vault "/your/Obsidian vault" --subject "Data compliance"
```

It checks v2 fields, statuses, link resolution, topic membership and reverse indexes. It neither verifies legal sources online nor executes Dataview in Obsidian. Without Python/PyYAML, the assistant can perform equivalent checks from the schema reference.

Map legacy fields and value types first. The helper does not rename or migrate files. Updating the skill does not automatically update an existing subject library.

## Maintenance

See the [workflow](SKILL.md), [purpose design](references/subject-design.md), [shared schema](references/card-schemas.md) and [source-verification procedure](references/authority-tiers.md).

The two entry documents are synchronized at version 2.1 (note schemas remain v2). On a source change, the workflow traces affected notes and marks conclusions for review. Scheduled background monitoring requires an actual scheduled task.

## Publication and license

This repository contains the bilingual skill and user guides, shared Chinese references and note templates, and the structural validation tool.

No open-source license has been selected yet.
