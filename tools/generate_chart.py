import json
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.chart_builder import ChartInputError, build_html, build_option, parse_json


class GenerateChartTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            chart_data = parse_json(tool_parameters.get("chart_data", ""), "chart_data")
            option = build_option(
                chart_type=tool_parameters.get("chart_type", "bar"),
                title=tool_parameters.get("title", ""),
                chart_data=chart_data,
                theme=tool_parameters.get("theme", "default"),
                show_legend=tool_parameters.get("show_legend", True),
                show_toolbox=tool_parameters.get("show_toolbox", True),
            )
            output_format = tool_parameters.get("output_format", "option_json")
            if output_format in {"option_json", "both"}:
                yield self.create_text_message(json.dumps(option, ensure_ascii=False, indent=2))
            if output_format in {"html", "both"}:
                yield self.create_text_message(build_html(option))
        except ChartInputError as exc:
            yield self.create_text_message(f"ECharts chart generation failed: {exc}")
