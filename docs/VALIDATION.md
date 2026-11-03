# 验证记录

日期：2026-11-03。本记录仅针对当前包及自带起步原型，不代表未来每次生成的产物均已验证。

## 已执行

- Skill Creator 官方 `quick_validate.py`：通过，检查入口元信息与命名。
- 本包 `python scripts/check_package.py`：通过，检查元信息、Markdown 相对链接、HTML ID/锚点及离线资源约束。
- 元信息与 GitHub Actions 配置：通过 YAML 解析。
- 检查器负例：临时包中的缺失引用、重复 HTML ID、远程脚本均被拒绝，原包未修改。
- 本地 Edge 无头浏览器操作：空态、必填校验、失败后保留输入并重试、创建、删除至空态、浏览器返回、未知 hash 回退、刷新清空均通过。
- 输入 HTML 字符串按文本显示，没有生成对应的 HTML 元素。
- 1280px 桌面、375px 与 320px 窄屏检查通过；窄屏无页面横向溢出。已目视检查桌面及 375px 截图。
- 浏览器运行期间无页面脚本异常，无 HTTP/HTTPS 外部资源请求。

## 尚未验证

- `evals/cases.md` 中的完整代理行为评估。
- 所有浏览器、辅助技术和其他代理平台的兼容性。
- GitHub Actions 的云端运行结果；本地执行的是同一结构检查。

## 验证环境

Windows，本机 Edge；维护时的 PyYAML 和 Playwright 仅安装在仓库外的临时验证目录。Skill 用户无需安装这些依赖。
