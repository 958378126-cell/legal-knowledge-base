---
name: legal-knowledge-base
description: Build or maintain an Obsidian knowledge base for a legal subject, including when the user only says they want to learn that field. Create a subject map, linked concepts, rules and cases, then adapt outputs and feedback to teaching, legal practice, exams, research or exploration.
metadata:
  version: "2.1"
---

# Legal knowledge base

[中文说明](SKILL.zh-CN.md). Both entry documents describe the same workflow and version. Maintain them together; `SKILL.md` is the loaded entrypoint. Shared references and note templates use Chinese field names for Chinese-language Obsidian libraries.

Use this skill for “I want to learn data compliance; build its knowledge base in Obsidian,” and for adding materials, repairing links or deriving outputs. A subject, course, legal instrument or interdisciplinary field is sufficient to start; a source collection or precise research question is not a prerequisite.

## 1. Locate the library and choose the mode

Inspect the actual vault, subject folders, templates and relevant project instructions before writing. Distinguish the outer Obsidian vault from its subject libraries. A new field normally gets a sibling folder, not a rename of the current subject. Use a known associated vault; ask for its location only if it cannot be determined safely. Do not scan unrelated personal directories.

- **Subject build**: map a field, then establish a usable first topic and its evidence links.
- **Continue**: inspect existing notes, then extend the requested topic or sources.
- **Audit/repair**: check requested defects; a review alone does not authorize changes.
- **Output**: derive a named deliverable from linked knowledge.
- **Refresh**: check named changes or stale sources and their downstream impact.

Updating this skill is separate from applying it to a live vault. Preserve user edits and original sources. For overwrites or migrations, make a recoverable copy of affected files, record its location and check for concurrent changes; separate backup confirmation is not a routine prerequisite.

## 2. Set the subject and purpose

Read [references/subject-design.md](references/subject-design.md) for a new subject, a purpose change or purpose-specific feedback. Record subject, jurisdiction, time scope, vault-relative subject path, available materials, purposes and intended outputs in `00-建库配置.md` using [its template](assets/templates/建库配置.md).

Infer purposes already stated in context. Allow multiple purposes and later changes. If none is stated, record `探索` provisionally and proceed with a general map and introductory topic. Do not require a questionnaire or impose exams, quizzes, a teaching plan or a work product on every learner. Clarify only facts that materially change legal coverage or the next deliverable.

Separate library completion criteria from evidence of learning or use. Producing notes does not establish mastery; producing a draft does not establish teaching effectiveness, exam performance or operational compliance.

## 3. Create the subject map before bulk cards

Write `00-学科导航.md` with scope, exclusions, core questions, prerequisites, topic relationships, suggested sequence, source entry points and the next useful batch. Textbooks or a syllabus can supply the backbone. Otherwise derive a provisional map from actors, legal relationships, activities, obligations, remedies and practical questions. Mark proposed coverage and uncertain boundaries.

Preserve existing conventions. A new subject can use this structure; create purpose-specific folders only when used:

```text
00-建库配置.md
00-学科导航.md
00-Inbox/        source inventory and unprocessed material
01-法规层/       texts, provisions, standards and guidance with their nature recorded
02-案例层/       judgments, administrative decisions and enforcement materials
03-专题层/       topic maps; 概念卡/ for definitions and distinctions
04-教学层/       optional teaching drafts and slide outlines
05-法务实务层/   optional scenarios, research, review and compliance workpapers
06-产出物/       exam/research/other outputs or released deliverables as needed
07-反馈与迭代/   feedback records when there is evidence to record
99-Templates/    selected, adapted templates
```

Build one coherent starter topic, then expand to the user's requested scope. A useful first delivery includes navigation, a source inventory, necessary concepts, verified rule anchors where obtainable, relevant cases when available, a connected topic map and the selected purpose's next output or action. An empty directory tree is not a completed library. Do not fabricate cases to fill a layer. Track missing sources; if access is limited, report a scaffold or partial batch accurately.

## Mandatory gate before legal-source retrieval

Before any statute, regulation or case retrieval task, including retrieval while drafting the subject map, inspect the available and discoverable MCP connectors for **Wolters Kluwer China Law & Reference (威科先行), PKULaw (北大法宝), and comparable professional legal databases**. Read [references/legal-source-connectors.md](references/legal-source-connectors.md). Do not skip this check and silently default to ordinary web search. Check once per retrieval task and recheck if access changes, not for every note.

For a relevant connector that is exposed and authorized, use a read-only status check or the first necessary public-source query to verify access, and prioritize the working professional connector for appropriate legal retrieval. Tool discovery alone does not prove connectivity, and successful search does not prove full-text access. Record the checked services, actual outcomes and retrieval route in the library's configuration/source inventory. If a connector is absent, inaccessible or unsuitable for the jurisdiction, state that limitation and continue through official sources. Do not claim database access that was not tested or treat database availability as proof of legal authority or currency. A skill-editing-only task does not require unrelated legal queries.

## 4. Create evidence-linked notes

Before creating or repairing notes, read [references/card-schemas.md](references/card-schemas.md) and select the corresponding [templates](assets/templates/). For authority, legal status or temporal application, also read [references/authority-tiers.md](references/authority-tiers.md).

Inventory sources with title, author/issuing body, locator, version/date, nature, intended use and verification gaps. Use available extraction/OCR for Word/PDF or scans and retain page references; unreliable or inaccessible text stays pending rather than being filled from memory.

Create concepts when an independent definition or distinction helps understanding. Store full legal texts and extract provisions when useful for a topic or output. Usually use one case per matter; distinguish court, regulator and secondary summaries. Separate quotation from synthesis, retain locators and verify dates, identifiers, amounts and material calculations. Record jurisdiction, effective dates and actual verification dates separately. Unknown legal status starts as `待核验`; completing a note cannot establish it.

## 5. Connect and verify the modules

The shared schema is the contract between templates and queries. In new libraries, `所属专题`, `关联法条`, `关联概念` and `依据卡片` are lists of quoted, vault-relative wikilinks without `.md`. A heading called “关联法条” is not a metadata field. Existing schemas require an explicit mapping and matching queries; do not silently rename user fields.

Link cases and concepts to rules and topics, topics to members, and outputs to notes supporting specific conclusions. Verify one representative chain before expanding. Keep explicit navigable lists in topic maps and rule reverse indexes. If Dataview is already enabled, optionally add the supplied queries with the real subject path. Without it, use the same lists and update them in the same batch; no plugin installation is required.

## 6. Adapt outputs and feedback to purpose

Use the purpose matrix in `subject-design.md`. Teaching may yield a lecture outline and slide-by-slide evidence notes; practice a fact/rule/action/evidence workpaper; exam study syllabus-aligned exercises and error analysis. Research and exploration can use question maps and unresolved issues. Multiple purposes share cards, with separate output and feedback records.

Review artifacts against their stated purpose and sources. Record feedback when available: rehearsal, actual learner questions, user responses, attempted problems, business review or observed use. Label assistant-generated checks as such. Do not fabricate classroom results, scores, implementation evidence or a “mastered” status. Missing feedback means `待反馈`, not failure, and never blocks initial construction. Link observed gaps to affected cards/topics, make scoped corrections and record the next check.

## 7. Maintain and hand off

On a requested refresh or a discovered source change, verify the new source, retain old versions and traverse `关联法条`, `关联概念`, `所属专题`, `依据卡片` and explicit links to find affected notes. Mark unresolved downstream conclusions `核验状态: 待复核`, explain why and restore verified status only after review. Distinguish historical applicability from present validity. Purpose changes update outputs and priorities, not duplicate source cards. Do not imply background monitoring without an actual scheduled task.

Validate fields, relation types, targets, duplicate/ambiguous names, source evidence and topic/reverse-list consistency. For the v2 schema, use the read-only helper:

```sh
python3 scripts/validate_vault.py --vault /absolute/path/to/vault --subject "Subject library"
```

It requires PyYAML; if unavailable, perform equivalent read-only checks and report the limitation. Map a legacy schema first; this helper is not a migration tool. It checks structure, not legal accuracy or the live Dataview runtime. Inspect a representative query in Obsidian when available; otherwise state live rendering was not tested.

Hand off the entry link, changes, current coverage, selected purposes, checks, legal connector availability and the retrieval route actually used, unresolved sources and next useful step. Do not describe a first batch as an exhaustive library.
