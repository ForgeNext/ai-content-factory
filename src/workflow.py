"""ForgeNextの実行Workflow。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from src.rule_engine import (
    EngineResult,
    RuleEngineBlockedError,
    run_rule_engine,
)


@dataclass(frozen=True)
class WorkflowResult:
    """Workflow全体の実行結果。"""

    status: str
    rule_engine_result: EngineResult
    evidence_path: Path
    output: Any | None = None


class Workflow:
    """Rule Engineを必須ゲートとして使用する実行Workflow。"""

    def __init__(
        self,
        project_root: Path,
    ) -> None:
        self.project_root = project_root.resolve()

    def run(
        self,
        task: Callable[[], Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> WorkflowResult:
        """Rule Engine通過後に対象処理を実行する。"""

        rule_result, evidence_path = run_rule_engine(
            project_root=self.project_root,
            context={
                "workflow": "ForgeNext Workflow",
                **(context or {}),
            },
            block_on_failure=True,
        )

        output = task() if task is not None else None

        return WorkflowResult(
            status="COMPLETED",
            rule_engine_result=rule_result,
            evidence_path=evidence_path,
            output=output,
        )


def run_workflow(
    project_root: Path,
    task: Callable[[], Any] | None = None,
    context: dict[str, Any] | None = None,
) -> WorkflowResult:
    """Workflowを簡単に実行するための公開関数。"""

    workflow = Workflow(
        project_root=project_root,
    )

    return workflow.run(
        task=task,
        context=context,
    )


__all__ = [
    "Workflow",
    "WorkflowResult",
    "RuleEngineBlockedError",
    "run_workflow",
]