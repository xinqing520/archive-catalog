# 🗂️ archive-catalog

**Claude Code skill for archive catalog batch processing** — parse, normalize, and build uniform-format catalogs from OCR-generated Excel files, with batch merge and final validation.

Designed for government/office archives digitization (Party Committee Office, Trade Union, United Front, etc.): turn "scanned → OCR'd Excel" into a standardized, archivable, mergeable master catalog.

---

## ✨ Features

- **Auto-detect source type**: archive catalog (with archive numbers) / volume catalog (without) / case-level catalog
- **Tolerant of format variations**: column shifts, header repositioning, multi-section OCR noise, missing archive numbers, varied date formats, `.xls`/`.docx`/`.zip` sources — see [format adaptation](references/format-adaptation.md)
- **Field normalization**: archive numbers unified to `QUANZONG-ws·year-term-code-no` (lowercase, `·` separator, 4-digit); clean OCR errors in 文号/题名/责任者/页数/日期
- **Date anomaly handling**:
  | Form | Handling |
  |------|----------|
  | 9-digit placeholder (`201000000` / `202000000`) | blank it out |
  | 8-digit invalid month (`20188927`) | ask user to confirm |
  | 7-digit truncated (`2019000` / `2019012`) | ask user to complete |
- **Yellow highlight** for uncertain items — user cancels highlight to confirm
- **Uniform output**: 9-col (with archive no.) / 7-col (without), 宋体, full borders, centered, auto wrap, auto row height
- **Batch merge**: merge into confirmed master catalog, **never rebuild from original sources** (preserves manual confirmations)
- **Final validation**: sequence continuity, unique & valid archive numbers, no residual highlights, date/page legality
- **Ready-to-use scripts**: `scripts/archive_cli.py` one-shot CLI, `scripts/norm_common.py` template

---

## 📦 Install

```bash
# One-shot installer
bash install.sh

# Or git clone
git clone https://github.com/xinqing520/archive-catalog.git ~/.claude/skills/archive-catalog
```

Run `/skills` in a Claude Code session to verify. Trigger phrases: "处理档案目录", "归档目录", "档号规范化", "合并总目录".

---

## 🚀 Quick Start

### Build a new master catalog

```
Put OCR source files (e.g. 1。1.xlsx) into the project
→ open in Claude Code → say "处理档案目录"
→ skill detects type, parses, normalizes, builds the unified output
```

### Merge a new batch

```bash
cp master.xlsx master_bak.xlsx          # 1. back up
python scripts/archive_cli.py merge master.xlsx new-batch.xlsx   # 2. merge
python scripts/archive_cli.py check master.xlsx                  # 3. validate
```

> ⚠️ Always merge into the **confirmed master catalog**; never rebuild from raw sources, or you'll re-apply cancelled highlights.

### Use the CLI

```bash
python scripts/archive_cli.py build 成品.xlsx src1.xlsx [src2.xlsx ...]  # build
python scripts/archive_cli.py check 成品.xlsx                             # validate
python scripts/archive_cli.py highlight 成品.xlsx [--clear]               # highlights
```

---

## 📁 Structure

```
archive-catalog/
├── SKILL.md                  # main workflow
├── references/
│   ├── format.md             # output format, field rules, date/highlight rules
│   ├── format-adaptation.md  # handling unfamiliar/different source formats
│   └── ocr-fixes.md          # OCR fix list (common + per-organization)
├── scripts/
│   ├── archive_cli.py        # one-shot CLI (build/merge/check/highlight)
│   ├── norm_common.py        # normalization function template
│   └── test_norm_common.py   # pytest unit tests
├── examples/                 # worked examples
├── .github/workflows/ci.yml  # CI auto-test
├── _meta.json                # skill metadata
├── install.sh                # one-shot installer
├── CHANGELOG.md
├── README.md                 # Chinese docs
├── README.en.md              # this file
├── LICENSE
└── .gitignore
```

---

## 🧠 Core Rules

| Item | Rule |
|------|------|
| Archive number | `QUANZONG-ws·year-term-no`, e.g. `1031-ws·2019-d30-0029` (lowercase, `·`, 4-digit no) |
| Term codes | `y`=permanent, `d30`=30yr, `d10`=10yr |
| QUANZONG | per organization (Trade Union 1031 / Party Committee Office 1001 / United Front 1012) |
| Date | 8-digit `YYYYMMDD`; year-only `YYYY0000`, month-only `YYYYMM00` are valid |
| Principles | pure-sequence-empty→delete; complete-but-missing-field→keep; clear OCR errors→auto-fix; uncertain→🟡 highlight |
| Missing archive no. | leave blank, never fabricate |

---

## 🔧 Extending

1. **New organization**: add its OCR fixes to `references/ocr-fixes.md`; set its QUANZONG in `scripts/archive_cli.py`
2. **New format variant**: record it in `references/format-adaptation.md`
3. **New normalization rule**: add to `scripts/norm_common.py` replacement list + test case

Both OCR fixes and format-adaptation lists are **cumulative** — richer with use.

---

## ❓ FAQ

**Q: Can it read legacy `.xls`?**
A: openpyxl can't. Convert to `.xlsx` first (Excel Save As / LibreOffice), or ask for `.xlsx`.

**Q: File has no archive numbers?**
A: Leave the column blank, never fabricate. Split sheets by year.

**Q: Date is year-only?**
A: Convert to `YYYY0000` (e.g. `2018` → `20180000`), which is valid.

**Q: 9-digit date (e.g. 201000000)?**
A: Blank it out per the rule.

**Q: Two adjacent rows look identical — duplicate?**
A: Uncertain → yellow highlight, let human decide.

---

## 📜 License

[MIT](LICENSE)
