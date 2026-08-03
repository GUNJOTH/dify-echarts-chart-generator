"""Dependency-free ECharts option construction and validation."""

from __future__ import annotations

import json
from typing import Any


SUPPORTED_TYPES = {"bar", "line", "pie", "scatter"}
THEMES = {
    "default": ["#5470C6", "#91CC75", "#FAC858", "#EE6666", "#73C0DE", "#3BA272"],
    "dark": ["#4992FF", "#7CFFB2", "#FDDD60", "#FF6E76", "#58D9F9", "#05C091"],
    "business": ["#1677FF", "#36CFC9", "#95DE64", "#FFC53D", "#FF7A45", "#9254DE"],
}


class ChartInputError(ValueError):
    pass


def parse_json(value: str, field_name: str, default: Any = None) -> Any:
    if not value or not value.strip():
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise ChartInputError(f"{field_name} must be valid JSON: {exc.msg}") from exc


def build_option(
    chart_type: str,
    title: str,
    chart_data: Any,
    theme: str = "default",
    show_legend: bool = True,
    show_toolbox: bool = True,
) -> dict[str, Any]:
    if chart_type not in SUPPORTED_TYPES:
        raise ChartInputError(f"Unsupported chart_type '{chart_type}'.")
    if theme not in THEMES:
        raise ChartInputError(f"Unsupported theme '{theme}'.")
    if not isinstance(chart_data, dict):
        raise ChartInputError("chart_data must be a JSON object.")

    series = chart_data.get("series")
    if not isinstance(series, list) or not series:
        raise ChartInputError("chart_data.series must be a non-empty array.")
    if chart_type == "pie":
        normalized_series = _pie_series(series)
    elif chart_type == "scatter":
        normalized_series = _scatter_series(series)
    else:
        categories = chart_data.get("categories")
        if not isinstance(categories, list) or not categories:
            raise ChartInputError("bar and line charts require chart_data.categories as a non-empty array.")
        normalized_series = _category_series(series, len(categories), chart_type)

    option: dict[str, Any] = {
        "color": THEMES[theme],
        "title": {"text": title or "Untitled chart", "left": "center"},
        "tooltip": {"trigger": "item" if chart_type == "pie" else "axis"},
        "legend": {"show": show_legend, "top": 32},
        "series": normalized_series,
    }
    if chart_type in {"bar", "line"}:
        option.update({"grid": {"left": 48, "right": 24, "bottom": 48, "containLabel": True}, "xAxis": {"type": "category", "data": chart_data["categories"], "axisLabel": {"interval": 0}}, "yAxis": {"type": "value"}})
    elif chart_type == "scatter":
        option.update({"grid": {"left": 48, "right": 24, "bottom": 48, "containLabel": True}, "xAxis": {"type": "value"}, "yAxis": {"type": "value"}})
    if show_toolbox:
        option["toolbox"] = {"right": 16, "feature": {"saveAsImage": {}, "restore": {}, "dataView": {"readOnly": True}}}
    return option


def _category_series(series: list[Any], category_count: int, chart_type: str) -> list[dict[str, Any]]:
    result = []
    for index, item in enumerate(series, 1):
        _ensure_series(item, index)
        data = item["data"]
        if not isinstance(data, list) or len(data) != category_count:
            raise ChartInputError(f"series[{index}].data must contain exactly {category_count} values.")
        result.append({"name": item["name"], "type": chart_type, "data": data, "smooth": chart_type == "line"})
    return result


def _pie_series(series: list[Any]) -> list[dict[str, Any]]:
    if len(series) != 1:
        raise ChartInputError("pie charts accept exactly one series.")
    item = series[0]
    _ensure_series(item, 1)
    data = item["data"]
    if not isinstance(data, list) or not data or not all(isinstance(point, dict) and "name" in point and "value" in point for point in data):
        raise ChartInputError("pie series data must be [{\"name\": \"A\", \"value\": 10}].")
    return [{"name": item["name"], "type": "pie", "radius": ["35%", "65%"], "data": data, "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0, 0, 0, 0.25)"}}}]


def _scatter_series(series: list[Any]) -> list[dict[str, Any]]:
    result = []
    for index, item in enumerate(series, 1):
        _ensure_series(item, index)
        data = item["data"]
        if not isinstance(data, list) or not data or not all(isinstance(point, list) and len(point) >= 2 for point in data):
            raise ChartInputError("scatter series data must be [[x, y], ...].")
        result.append({"name": item["name"], "type": "scatter", "symbolSize": 12, "data": data})
    return result


def _ensure_series(item: Any, index: int) -> None:
    if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not item["name"].strip() or "data" not in item:
        raise ChartInputError(f"series[{index}] requires a non-empty name and data.")


def build_html(option: dict[str, Any]) -> str:
    option_json = json.dumps(option, ensure_ascii=False).replace("</", "<\\/")
    return """<!doctype html>
<html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><title>ECharts preview</title>
<script src=\"https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js\"></script></head>
<body><div id=\"chart\" style=\"width:100%;height:560px\"></div><script>
const chart = echarts.init(document.getElementById('chart'));
chart.setOption(""" + option_json + """);
window.addEventListener('resize', () => chart.resize());
</script></body></html>"""
