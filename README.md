# ECharts Chart Generator for Dify

A no-credential Dify Tool plugin that turns structured data into a valid Apache ECharts 5 option. It can return the option JSON for an existing frontend, a standalone HTML preview, or both.

## Tool input

Use `generate_chart` in a Dify Tool node or Agent. `chart_data` is JSON; do not pass a Markdown code fence.

### Bar / line

```json
{
  "categories": ["1月", "2月", "3月"],
  "series": [
    {"name": "发电量", "data": [120, 132, 101]},
    {"name": "计划", "data": [110, 125, 115]}
  ]
}
```

### Pie

```json
{
  "series": [
    {"name": "缺陷等级", "data": [{"name": "一般", "value": 21}, {"name": "严重", "value": 3}]}
  ]
}
```

### Scatter

```json
{
  "series": [{"name": "机组样本", "data": [[12.3, 80], [14.1, 91]]}]
}
```

## Design decisions

- Validates data shape before output: category counts, pie point names/values, and scatter coordinate pairs.
- Uses no database, network request, or persistent storage; the optional HTML only references the public ECharts CDN when opened in a browser.
- Keeps tool output textual because Dify Tool nodes expose messages/text naturally. For a rendered chart in your application, send the returned JSON into `echarts.setOption(option)`.

## Local verification

The core builder uses only the Python standard library. Run `uv run python -m unittest discover -s tests -v` from this plugin directory. For Dify integration, configure a Plugin Debug key, run `uv sync`, then run `uv run python -m main`.

## Packaging

With the Dify Plugin CLI installed:

```powershell
dify plugin package .
```

Then upload the generated `.difypkg` under **Plugins → Install from local package** in Dify.

## 项目治理入口

- [治理约定](./GOVERNANCE.md)
- [贡献指南](./CONTRIBUTING.md)
- [安全策略](./SECURITY.md)
- Issue 与 Pull Request 请使用仓库模板，并记录实际验证证据。