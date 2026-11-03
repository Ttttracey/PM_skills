# PM Skills · 轻量产品工作流

面向产品经理的轻量工作流，覆盖 **需求分析 → PRD → 可点击原型**。各阶段可以单独使用，简单需求直接开始，信息不足时只问影响方案的关键问题。

默认中文、Markdown PRD、自包含 HTML 原型。使用本体不需要 Python、Node、后台服务或付费插件。用户指定格式与现有团队约定优先。

## 安装到 Codex

将此仓库下载或克隆到个人技能目录，文件夹命名为 `pm-workflow-lite`：

```powershell
# Windows PowerShell；若目录已存在，请先检查其中的个人修改。
git clone https://github.com/Ttttracey/PM_skills.git "$env:USERPROFILE/.codex/skills/pm-workflow-lite"
```

```bash
# macOS / Linux
git clone https://github.com/Ttttracey/PM_skills.git ~/.codex/skills/pm-workflow-lite
```

重新打开 Codex，输入 `$pm-workflow-lite` 调用。若设置了自定义 `CODEX_HOME`，使用其 `skills/pm-workflow-lite` 目录。该仓库只需完整复制一次，不需要把服务脚本安装进每个业务项目。此版本按 Codex Skill 组织；其他代理平台的自动发现行为未验证。

## 使用示例

```text
$pm-workflow-lite 我想给课程列表增加收藏功能。先帮我梳理用户场景和最小范围。
```

```text
$pm-workflow-lite 根据这份需求分析写精简 PRD，只做收藏和取消收藏，不做分组。没有数据的目标值标待确认。
```

```text
$pm-workflow-lite 按现有 PRD 做一个手机端可点击原型，使用演示数据，包含收藏、空态和失败重试。
```

```text
$pm-workflow-lite 把现有 PRD 的收藏上限改为 100，同时检查已有原型有没有受影响的规则。
```

默认产物：`需求/<需求名>/需求分析.md`、`PRD.md`、`prototype.html`，只生成本次请求的文件，已有目录约定优先。原型可直接在浏览器打开；`assets/prototype-starter.html` 本身也可作为离线交互示例查看，数据刷新后清空。

## 功能特点

- **按需产出**：需求分析、PRD 和原型均可独立使用，也可以串联完成。
- **轻量运行**：无需项目初始化或后台服务，HTML 原型可离线打开。
- **格式灵活**：PRD 默认使用 Markdown，也支持指定格式和团队模板。
- **聚焦关键决策**：只澄清影响方案的信息，信息充分时直接开始。
- **证据清楚**：区分事实、假设与演示数据，缺少证据时给出验证计划。
- **持续迭代**：复用已有需求目录，修改业务规则时检查 PRD 与原型的一致性。

## 维护与验证

- 调整触发范围和共同规则：[SKILL.md](SKILL.md)。
- 调整阶段规范：[需求分析](references/discovery.md)、[PRD](references/prd.md)、[原型](references/prototype.md)。
- 模板：[PRD](assets/prd-template.md)、[HTML 原型](assets/prototype-starter.html)。
- 行为验收：[评估案例](evals/cases.md)。这些是人工或代理评估场景，结构检查不代表行为评估通过。
- 本地结构检查（维护时需 Python 3.9+）：`python scripts/check_package.py`。GitHub Actions 运行同样检查，不安装依赖。

检查覆盖入口元信息、相对链接与包内 HTML 的基础结构，不证明生成内容质量或浏览器交互正确。浏览器检查结果见 [验证记录](docs/VALIDATION.md)。
