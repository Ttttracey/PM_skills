# 收藏功能示例

用于检查实际文件与交互，不包含真实调研数据。示例范围是两页原型和对应 HTML PRD；不演示流程图、埋点或时序图。

## 直接查看

- [PRD](收藏功能/需求文档/收藏功能-PRD.html)：在本地浏览器打开，可编辑文字、增删表格行、调整尺寸、撤销重做与展开双栏原型。
- [原型](收藏功能/原型/收藏功能-prototype.html)：收藏、取消收藏、空态和模拟失败重试，数据刷新后重置。

## 启用保存与导出服务

在仓库根目录运行（Windows 使用 py -3；macOS/Linux 使用 python3）：

```powershell
py -3 scripts/initialize.py --project examples/favorites --no-launcher
py -3 examples/favorites/scripts/start_service.py --serve
```

服务启动后，在输出的本地地址中打开 PRD。通过服务访问可使用带版本校验的保存写回、复制含图与 PNG 导出。直接使用 file:// 打开时，保存采用浏览器文件选择或下载副本。

结构校验：

```powershell
py -3 assets/scripts/validate_prd.py examples/favorites/收藏功能/需求文档/收藏功能-PRD.html
```

可检查：修改背景后撤销/重做；新增表格行再删除并撤销；切换双栏页面；在原型收藏或取消；模拟失败后重试；启动服务后复制含图、保存文档与导出截图。
