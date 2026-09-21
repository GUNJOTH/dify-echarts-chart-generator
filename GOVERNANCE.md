# 项目治理约定

## 项目范围和事实来源

本仓库维护 dify-echarts-chart-generator。项目事实以源码、项目配置、锁文件、测试、CI 结果和 Pull Request 记录为准。外部服务、源系统、模型、设备或部署环境的联调结果，必须和离线检查分开记录。

## 分支与合并

main 是默认交付分支。仓库 Ruleset 要求通过 Pull Request，禁止删除和非 fast-forward 更新；人工审批数量仍是单独的治理决策。

开发分支使用 feat/、fix/、docs/、chore/ 等用途前缀。Pull Request 应说明变更范围、验证命令、风险、兼容性影响和回滚方式。

## CI 与验证边界

现有 .github/workflows/verify.yml 已负责 uv 锁定环境和 unittest；本次不重复添加工作流。

本地建议检查：

~~~powershell
uv sync --frozen
uv run python -m unittest discover -s tests -v
~~~

CI 通过不等于生产环境、真实外部服务或真实业务数据验收通过。

## 数据与安全

插件输入、图表配置和 HTML 预览必须避免携带凭据、个人信息或未授权的业务数据。

不得把真实凭据、未脱敏业务数据、生产日志、真实音频、图片、Excel、模型私钥或内部服务地址提交到仓库、Issue 或 Pull Request。