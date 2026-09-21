# 发布约定

本文档规定 `dify-echarts-chart-generator` 的版本、验证、打包和 GitHub Release 流程。
当前仓库没有自动发布工作流，发布由仓库维护者按本约定手动完成。

## 版本与变更记录

- 版本号以 `pyproject.toml` 的 `[project].version` 为准。
- 使用 `MAJOR.MINOR.PATCH` 版本格式，并使用 `vMAJOR.MINOR.PATCH` 作为 Git tag。
- `manifest.yaml`、Tool 参数、ECharts option 结构、输出文本或 HTML 语义发生用户可见
  变化时，必须先在 `CHANGELOG.md` 的对应版本条目中记录兼容性影响。
- 版本号和更新日志在同一个 Pull Request 中修改；PR 目标为 `main`，不得直接推送或
  强推 `main`。
- 尚未形成正式版本的变化写入 `[未发布]`，不要在没有实际发布内容时伪造历史版本
  条目。

## 发布前检查

合并版本 PR 前，至少执行与当前 `main` CI 一致的检查：

```powershell
uv sync --frozen
uv run python -m unittest discover -s tests -v
```

涉及 Tool 输入、图表数据校验或输出结构时，还要覆盖 bar/line、pie、scatter、空数据、
数量不一致、非法坐标和无效 pie value 等边界，并确认输出仍可由调用方传给
`echarts.setOption(option)`。

如果本次发布包含 Dify 插件包，应在安装了 Dify Plugin CLI 的隔离环境执行：

```powershell
dify plugin package .
```

确认生成的 `.difypkg` 与 `manifest.yaml` 版本一致，包内不包含 Plugin Debug key、
环境变量、用户数据或本地临时文件。Dify 真实运行验证需要单独配置授权的 Debug key；
本地 unittest 不能代替 Dify Plugin Runtime 验收。

可选 HTML 预览会从公开 CDN 加载 ECharts JavaScript。发布说明应保留这一浏览器侧网络
边界，不能把它描述为插件运行时完全无网络请求。

## 发布步骤

1. 从 `main` 创建版本 PR，更新 `pyproject.toml` 版本号和 `CHANGELOG.md`。
2. 等待 CI 通过，并完成 Tool 契约、Dify 运行时、隐私边界和打包内容审查后合并。
3. 在已合并的 `main` 提交上创建对应的 `vMAJOR.MINOR.PATCH` tag，并推送该 tag；不
   修改或覆盖已有 tag。
4. 基于该 tag 创建 GitHub Release，标题使用版本号，正文引用 `CHANGELOG.md` 中的
   对应版本条目；如有正式 `.difypkg`，将其作为同一版本的发布附件。
5. 发布后确认 Release、tag、`pyproject.toml` 版本、`manifest.yaml` 版本和插件包
   元数据一致；发现问题时按补丁版本发布修复，不回写已发布版本。

## 回滚边界

发布回滚不得通过删除或覆盖 tag 伪造历史。插件源码、`manifest.yaml`、Tool 参数契约、
生成的 ECharts option、HTML 预览和 Dify 安装包必须分别评估；已经安装旧包的用户应
通过新版本修复或明确的插件回退流程处理。
