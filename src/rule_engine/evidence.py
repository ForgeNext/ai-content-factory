"""Rule Engineの実行結果をEvidenceとして保存する。"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .result import EngineResult


class EvidenceWriter:
    """Rule EngineのEvidenceをJSON形式で保存する。"""

    def __init__(
        self,
        output_directory: Path,
    ) -> None:
        self.output_directory = output_directory

    def write(
        self,
        result: EngineResult,
        context: dict[str, Any] | None = None,
    ) -> Path:
        """実行結果をEvidenceファイルとして保存する。"""

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        executed_at = datetime.now().astimezone()
        timestamp = executed_at.strftime("%Y%m%d_%H%M%S_%f")

        output_path = (
            self.output_directory
            / f"rule_engine_{timestamp}.json"
        )

        payload = {
            "engine": "ForgeNext Rule Engine",
            "version": "1.1.0",
            "executed_at": executed_at.isoformat(),
            "result": result.to_dict(),
            "context": context or {},
        }

        output_path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return output_path