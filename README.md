<p align="center">
  <img src="assets/readme/cover.svg" alt="PM Skills：从需求洞察到 PRD、原型与验收复盘的完整产品工作流" width="100%">
</p>

<p align="center">
  <strong>需求分析、文档编写、交互设计与交付验证。</strong><br>
  面向产品经理的完整工作流 Skill，适用于不同业务领域与产品形态。
</p>

<p align="center">
  <a href="#capabilities">能力一览</a> ·
  <a href="#prd">PRD 工作台</a> ·
  <a href="#quickstart">快速上手</a> ·
  <a href="#examples">使用示例</a> ·
  <a href="#structure">项目结构</a>
</p>

---

<a id="capabilities"></a>
## 功能范围

根据需求描述与已有材料，生成 HTML 文档、交互原型和验证清单。支持从任一阶段开始，同一需求的产物集中管理、持续同步。

| 阶段 | 解决的问题 | 主要交付物 |
| :--- | :--- | :--- |
| **发现需求** | 谁在什么场景遇到问题，证据是什么，先解决哪一件事 | HTML 需求洞察报告 |
| **定义方案** | 目标、范围、业务规则与页面行为如何写清楚 | HTML PRD |
| **演示交互** | 页面如何操作，流程如何流转，状态如何变化 | 单文件 HTML 原型、业务流程图、Screen Flow |
| **验证交付** | 功能是否符合方案，上线后表现怎样 | 可勾选验收清单、数据分析报告 |

**核心方式：先复制骨架 → 填写业务内容 → 联动原型与流程 → 校验后交付。**

<a id="prd"></a>
## HTML PRD

以 [PRD 正文骨架](assets/templates/prd-content.html) 为起点，保留固定类名、表头、`colgroup`、`.desc-block` 与 `data-preview`，减少从零搭结构造成的遗漏。它是正文片段，需要按照工作流加入完整 HTML 页面外壳与正文样式。

### 文档结构

```text
项目信息 → 版本记录 → 需求背景 → 需求目标 → 需求概述
    → 业务流程图 → 交互流程图 → 详细方案 → 数据埋点 → 时序图
```

- **始终保留**：项目信息、版本记录、需求背景、需求目标、详细方案。
- **按需加入**：需求概述、业务流程图、交互流程图、数据埋点、时序图；确有需要时补充上线计划与附录。裁剪前列明保留/省略项与原因并确认，用户已明确的选择直接沿用。
- **边界归属功能**：异常和边界写进对应功能的【边界说明】，不另设独立章节。章节编号随实际内容连续重排。

<details>
<summary><strong>查看内容规范：目标、背景、范围与详细方案</strong></summary>

| 内容 | 写法 |
| :--- | :--- |
| 需求目标 | 用户结果 / 衡量指标 / 统计口径 / 预期方向 / 目标值五列表；无真实基线写“待基线确认” |
| 需求背景 | 谁在什么场景遇到什么问题 → 产生的影响 → 支撑证据 |
| 需求概述 | 明确“本期范围 / 本期不做什么”，集中承载跨页共享规则 |
| 详细方案 | 一行对应一个界面或状态变体，与具体原型资产关联 |
| 未决事项 | 正文末尾集中列出“待后续确认的产品口径”，注明影响与已知负责人 |

描述列每格保留【页面元素】【交互说明】；按需要加入【功能逻辑】【边界说明】【数据与内容规则】【前置条件与权限】【文案规范】【策略说明】。

用“删掉这个页面后，规则是否仍成立”判断归属：仍成立的跨页规则集中定义，页面引用对应规则；只属于本页的规则留在本格。每条独立成段，不填“无”、不写“同上”。技术接口、参数、字段 key 和错误码不进入详细方案描述列；需要时放进研发向时序说明。

</details>

<details>
<summary><strong>查看阅读体验：双栏原型、滚动联动与缩放</strong></summary>

- 打开 PRD 默认是干净的阅读态；点击“双栏预览”才展开右侧原型 dock。
- iframe 首次展开才加载，支持切页与 scroll-spy：正文滚到某个功能，右侧跟随定位到对应页面。
- 提供 `－ / % / ＋ / 适配` 控件；原型列支持高清截图或可交互 iframe。

</details>

<details>
<summary><strong>查看编辑能力：修改、撤销、保存与复制</strong></summary>

- 正文 `contenteditable`，支持表格增删行、列宽及行高拖拽。
- 文字、增删行、删表和尺寸调整共用撤销/重做栈，兼容 Windows 与 macOS 快捷键；恢复后的控件继续可用。撤销历史仅保存在当前页面内存。
- “保存并通知AI”将修改写回文件；AI 后续读取磁盘内容，同步原型与流程。浏览器能力不足时降级为下载副本，并提示用户使用更新后的文件。
- “一键复制全文”通过本地服务把原型和流程图转为内联 base64 图片。图片默认宽度 2000px、质量 0.9；按文件修改时间缓存，部分失败时明确提示缺失内容。

</details>

### 交付前的机械校验

[PRD 校验器](assets/scripts/validate_prd.py) 检查核心章节、章节编号、固定表头与有效列数、合并单元格、`colgroup`、非空 `data-preview`、描述分块、埋点命名与空值、正文样式和目标表。

```powershell
# 在已初始化的项目中执行；macOS / Linux 将 py -3 换成 python3
py -3 scripts/validate_prd.py "需求名/需求文档/需求名-PRD.html"
```

**校验失败先修复，校验通过后仍需检查内容与视觉。**

## 原型与流程图

| 交付物 | 交互与展示能力 |
| :--- | :--- |
| **HTML 原型** | 单文件交付、hash 跳转、平铺预览、iframe 嵌入；通过浏览器真实渲染导出 PNG |
| **业务流程图** | Mermaid HTML，浅底、细描边、深色文字与直线连接风格，统一 PRD 页面外壳；单独导出高清截图 |
| **交互流程图** | 用缩放 iframe 引用真实原型页，直角折线连接跳转关系，附状态机图例、缩放/拖拽与整图导出 |
| **时序与状态说明** | PRD 最后按需附可复制的 `sequenceDiagram` 与 `stateDiagram-v2` 源码，方便研发复用和测试拆解用例 |
| **Pencil 增强** | 提供 MCP 配置示例与高保真绘制提示；HTML 原型仍是主要交互交付物 |

<details>
<summary><strong>交互流程图的布局与零遮挡检查</strong></summary>

同排节点间隔至少 70px，上下排至少 200px，画布留白至少 30px；回流路径采用错开的轨道。优先根据内容推导画布尺寸。

通过 `auditFlow()` 检查标签压节点、标签重叠、连线穿节点及越界，审计通过才允许导出。修复时扩大画布、增加间距或调整走线，保持分支与文字完整；独立页面与 PRD 嵌入态均需目视检查。

</details>

## 调研、验收与复盘

- **需求洞察**：分析用户场景、痛点、竞品与机会；记录真实证据及缺口。没有材料时给假设和验证计划，模拟反馈单独标记，不混入调研结论。
- **功能验收**：从 PRD 提取核心路径、对应功能边界、视觉与埋点检查，生成支持状态筛选、进度统计、本地保存和报告导出的 HTML checklist。
- **数据复盘**：根据真实业务数据生成指标、表格、图表与行动建议，明确时间、分母及去重口径，区分观察到的变化与原因假设。

## 可运行示例

[收藏功能示例](examples/favorites/README.md) 包含一份 HTML PRD 和两页交互原型。可直接打开检查编辑、撤销重做、双栏预览、收藏与失败重试；保存写回、复制含图和截图导出需要启动本地服务。

<a id="quickstart"></a>
## 快速上手

### 1 · 将 Skill 放进 Codex

需要 Git 和 Python 3.9+。截图服务首次启动时会自动准备运行环境，优先使用已有 Edge / Chrome，未找到时再下载 Chromium。

<details open>
<summary><strong>Windows · PowerShell</strong></summary>

```powershell
git clone https://github.com/Ttttracey/PM_skills.git "$env:USERPROFILE/.codex/skills/pm-workflow"
```

</details>

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
git clone https://github.com/Ttttracey/PM_skills.git ~/.codex/skills/pm-workflow
```

</details>

如设置了自定义 `CODEX_HOME`，使用其 `skills/pm-workflow` 目录。重新打开 Codex，通过 `$pm-workflow` 调用。已有同名目录时先检查个人修改，避免覆盖。

### 2 · 在业务项目中初始化

在你的业务项目目录执行，或由 Skill 检查缺失文件后完成初始化：

```powershell
# Windows
py -3 "$env:USERPROFILE/.codex/skills/pm-workflow/scripts/initialize.py" --project .
```

```bash
# macOS / Linux
python3 "$HOME/.codex/skills/pm-workflow/scripts/initialize.py" --project .
```

初始化会安装工作流、正文骨架、校验器和导出服务。重复执行可修复缺失文件；更新运行时代码前备份，用户编辑过的工作流与模板保留，新版本放进 `.pm-workflow/updates/` 供合并。

### 3 · 开始工作，按需导出

| 平台 | 导出服务启动方式 |
| :--- | :--- |
| Windows | 双击项目根目录的 `启动原型导出服务.bat`，保持服务运行 |
| macOS | 默认注册按需启动器，点击导出时自动启动；也可手动双击 `.command` 入口 |
| Linux | 手动执行 `python3 scripts/start_service.py --serve` |

macOS 不希望注册按需启动器时，初始化加 `--no-launcher`。其只在有请求时拉起服务，不保持空闲工作进程。截图输出到当前需求目录，已有截图仅按导出清单更新，避免误删手工资产。

排查环境、浏览器或端口问题：

```powershell
py -3 scripts/start_service.py --doctor
```

<a id="examples"></a>
## 从一个具体任务开始

```text
$pm-workflow 给课程列表增加收藏功能。先梳理场景和范围，
再写 HTML PRD 和可点击原型；保留空态与失败重试，暂不做收藏分组。
```

```text
$pm-workflow 基于现有 PRD 补充交互流程图，
页面引用真实原型，检查遮挡并导出整图。
```

```text
$pm-workflow 读取这份 PRD 生成验收清单，
覆盖主要路径、权限限制与网络失败恢复。
```

```text
$pm-workflow 根据这份上线数据做复盘，
说明统计口径、观察到的变化及需要继续验证的原因。
```

<a id="structure"></a>
## 产物目录

```text
业务项目/
├── 需求名/
│   ├── 需求文档/          HTML PRD
│   ├── 原型/              可点击 HTML
│   ├── 流程图/            业务流程图 / Screen Flow
│   ├── 原型截图/          原型 PNG
│   ├── 流程图截图/        流程图 PNG
│   ├── 需求挖掘/          洞察报告
│   ├── 验收清单/          交互 checklist
│   ├── 数据分析/          复盘报告
│   └── 沟通记录.md
├── .agents/workflows/     可按项目调整的工作流
├── scripts/               共享骨架、校验器与导出服务
├── .pm-workflow/          本机配置，不提交
└── .handoff/              交接与更新备份，不提交
```

谁先开始就创建需求目录，后续阶段复用；只建立实际用到的子目录。PRD、原型和流程图发生变化时，检查并同步受影响的既有产物。

## 维护与验证

| 想调整什么 | 入口 |
| :--- | :--- |
| 触发条件、路由与共同规则 | [SKILL.md](SKILL.md) |
| PRD、双栏、编辑与流程规范 | [PRD 工作流](assets/workflows/edu-pm-prd.md) |
| 调研、验收与复盘 | [需求洞察](assets/workflows/edu-pm-demand.md) · [功能验收](assets/workflows/edu-pm-acceptance.md) · [数据分析](assets/workflows/edu-pm-data-analysis.md) |
| 文档骨架与机械校验 | [正文骨架](assets/templates/prd-content.html) · [校验器](assets/scripts/validate_prd.py) |
| 自动检查与行为评估 | [回归测试](tests/test_workflow.py) · [评估案例](evals/cases.md) · [验证记录](docs/VALIDATION.md) |

```bash
python scripts/check_package.py
python -m unittest discover -s tests -v
```

GitHub Actions 在 Windows 与 Linux 上运行结构检查和回归测试。自动校验不替代产品内容评审、浏览器检查与最终验收。

维护时可在 Windows + Edge 环境复查浏览器流程：

```powershell
python -m pip install -r requirements-dev.txt
python tests/browser_smoke.py
```

该检查在临时项目运行，结束后停止服务；预览截图保存在 `.test-artifacts/`，不提交到仓库。它覆盖随附示例，不代表所有需求产物均已完成验收。
