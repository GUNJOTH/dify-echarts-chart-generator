from typing import Any

from dify_plugin import ToolProvider


class EChartsChartGeneratorProvider(ToolProvider):
    """No credentials are needed: all chart construction happens locally."""

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        return None
