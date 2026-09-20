# 贡献指南

## 开始前

先阅读 README、GOVERNANCE.md 和 SECURITY.md。使用项目声明的 Python、Node 和依赖管理工具，不擅自替换锁文件或运行工具链。

## 分支与 Pull Request

从 main 创建用途明确的开发分支，例如 feat/<short-name>、fix/<short-name>、docs/<short-name> 或 chore/<short-name>。不要直接向 main 推送。

Pull Request 应说明变更目的、API/数据/规则/模型影响、实际验证命令、风险、兼容性和回滚方式。涉及外部系统的验证必须注明环境和授权边界。

## 提交前检查

~~~powershell
uv sync --frozen
uv run python -m unittest discover -s tests -v
~~~

不得为了让 CI 通过而删除测试、降低断言或提交真实生产数据。

## 依赖和样本

- 不提交 .env、Token、API Key、Cookie、数据库密码或未脱敏业务样本。
- 新增依赖前检查现有锁文件，变更后同步锁文件。
- 上传文件、音频、图片、Excel、数据集和模型权重应使用最小化、去标识化样本。