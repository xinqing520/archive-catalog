# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 规范，版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

- （待规划：真实 .xlsx 示例文件、英文文档、skill 图标等）

## [1.0.0] - 2026-08-13

### 新增
- **主流程** `SKILL.md`：识别源文件 → 格式差异应对 → 提取 → 规范化 → 日期分级 → 高亮 → 输出 → 并入 → 校验
- **参考文件** `references/`：
  - `format.md` — 输出格式模板、字段规范、日期/高亮规则
  - `format-adaptation.md` — 格式差异应对（列偏移/表头移位/多段乱码/无档号/日期多样/.xls/.docx/.zip）
  - `ocr-fixes.md` — OCR 修正清单（通用 + 各单位积累）
- **脚本** `scripts/`：
  - `archive_cli.py` — 一体化 CLI（build / merge / check / highlight 四个子命令）
  - `norm_common.py` — 通用字段规范化函数模板（档号/文号/题名/责任者/页数/日期）
  - `test_norm_common.py` — pytest 单测（19 用例，覆盖规范化与日期规则）
- **示例** `examples/example.md` — 处理效果示例与典型 OCR 错例
- **工程文件**：README.md、LICENSE（MIT）、.gitignore、`_meta.json`、CHANGELOG.md

### 关键规则
- 日期异常分级：9 位占位（`201000000`）留空；8 位月份非法（`20188927`）询问用户；7 位缺位（`2019000`）询问用户
- 合并新批次基于已确认成品，不从原始源重建

[1.0.0]: https://github.com/xinqing520/archive-catalog/releases/tag/v1.0.0
