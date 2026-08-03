import importlib.util
import pathlib
import unittest

import yaml


MODULE_PATH = pathlib.Path(__file__).parents[1] / "tools" / "chart_builder.py"
SPEC = importlib.util.spec_from_file_location("chart_builder", MODULE_PATH)
chart_builder = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(chart_builder)


class ChartBuilderTests(unittest.TestCase):
    def test_plugin_yaml_references_existing_files(self):
        root = pathlib.Path(__file__).parents[1]
        manifest = yaml.safe_load((root / "manifest.yaml").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "echarts_chart_generator")
        self.assertTrue((root / "_assets" / manifest["icon"]).is_file())
        provider_path = root / manifest["plugins"]["tools"][0]
        self.assertTrue(provider_path.is_file())
        provider = yaml.safe_load(provider_path.read_text(encoding="utf-8"))
        self.assertTrue((root / provider["extra"]["python"]["source"]).is_file())
        tool_path = root / provider["tools"][0]
        self.assertTrue(tool_path.is_file())
        tool = yaml.safe_load(tool_path.read_text(encoding="utf-8"))
        self.assertTrue((root / tool["extra"]["python"]["source"]).is_file())

    def test_line_option_has_category_axis_and_series(self):
        option = chart_builder.build_option("line", "Monthly output", {"categories": ["Jan", "Feb"], "series": [{"name": "Actual", "data": [10, 12]}]})
        self.assertEqual(option["xAxis"]["data"], ["Jan", "Feb"])
        self.assertTrue(option["series"][0]["smooth"])

    def test_pie_rejects_two_series(self):
        with self.assertRaises(chart_builder.ChartInputError):
            chart_builder.build_option("pie", "", {"series": [{"name": "A", "data": []}, {"name": "B", "data": []}]})

    def test_html_escapes_closing_script(self):
        option = chart_builder.build_option("bar", "</script>", {"categories": ["A"], "series": [{"name": "S", "data": [1]}]})
        self.assertIn("<\\/script>", chart_builder.build_html(option))


if __name__ == "__main__":
    unittest.main()
