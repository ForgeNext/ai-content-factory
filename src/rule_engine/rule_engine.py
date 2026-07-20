"""ForgeNext Rule Engineの実行本体。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .checks import (
    check_incident_closure_evidence,
    check_required_documents,
)
from .evidence import EvidenceWriter
from .result import (
    CheckResult,
    EngineResult,
    RuleStatus,
    determine_engine_status,
)


class RuleEngineBlockedError(RuntimeError):
    """Rule Engineが対象処理を停止した場合に送出する例外。"""

    def __init__(
        self,
        result: EngineResult,
        evidence_path: Path | None = None,
    ) -> None:
        self.result = result
        self.evidence_path = evidence_path

        message = (
            "Rule Engineが対象処理を停止しました。"
            f" status={result.status.value}"
        )

        if evidence_path is not None:
            message += f" evidence={evidence_path}"

        super().__init__(message)


class RuleEngine:
    """ForgeNextの既存会社基準を機械的に照合する。"""

    def __init__(
        self,
        project_root: Path,
        evidence_directory: Path | None = None,
    ) -> None:
        self.project_root = project_root.resolve()

        if evidence_directory is None:
            evidence_directory = (
                self.project_root
                / "output"
                / "rule_engine_evidence"
            )

        self.evidence_writer = EvidenceWriter(
            output_directory=evidence_directory,
        )

    def collect_checks(
        self,
        context: dict[str, Any] | None = None,
    ) -> list[CheckResult]:
        """会社基準とcontextで指定された追加監査を実行する。"""

        checks = check_required_documents(
            project_root=self.project_root,
        )

        if context is None:
            return checks

        incident_closure = context.get("incident_closure")

        if incident_closure is None:
            return checks

        if not isinstance(incident_closure, dict):
            checks.append(
                CheckResult(
                    rule_id="incident.configuration",
                    rule_name="Incident closure configuration",
                    status=RuleStatus.FAIL,
                    message="incident_closureの設定形式が不正です。",
                    evidence={
                        "received_type": type(
                            incident_closure
                        ).__name__,
                    },
                )
            )
            return checks

        incident_id = incident_closure.get("incident_id")
        evidence_path = incident_closure.get("evidence_path")
        required_markers = incident_closure.get("required_markers")
        ceo_approved = incident_closure.get(
            "ceo_approved",
            False,
        )

        configuration_is_valid = (
            isinstance(incident_id, str)
            and bool(incident_id.strip())
            and isinstance(evidence_path, str)
            and bool(evidence_path.strip())
            and isinstance(required_markers, (list, tuple))
            and bool(required_markers)
            and all(
                isinstance(marker, str) and bool(marker.strip())
                for marker in required_markers
            )
            and isinstance(ceo_approved, bool)
        )

        if not configuration_is_valid:
            checks.append(
                CheckResult(
                    rule_id="incident.configuration",
                    rule_name="Incident closure configuration",
                    status=RuleStatus.FAIL,
                    message="インシデント監査の必須設定が不足しています。",
                    evidence={
                        "incident_id": incident_id,
                        "evidence_path": evidence_path,
                        "required_markers": required_markers,
                        "ceo_approved": ceo_approved,
                    },
                )
            )
            return checks

        checks.extend(
            check_incident_closure_evidence(
                project_root=self.project_root,
                incident_id=incident_id.strip(),
                relative_path=evidence_path.strip(),
                required_markers=tuple(required_markers),
                ceo_approved=ceo_approved,
            )
        )

        return checks

    def run(
        self,
        context: dict[str, Any] | None = None,
        block_on_failure: bool = True,
    ) -> tuple[EngineResult, Path]:
        """全チェックを実行し、Evidenceを保存する。"""

        checks = self.collect_checks(
            context=context,
        )
        status = determine_engine_status(checks)
        summary = self._build_summary(
            status=status,
            checks=checks,
        )

        result = EngineResult(
            status=status,
            checks=tuple(checks),
            summary=summary,
        )

        evidence_path = self.evidence_writer.write(
            result=result,
            context=context,
        )

        if block_on_failure and result.blocks_output:
            raise RuleEngineBlockedError(
                result=result,
                evidence_path=evidence_path,
            )

        return result, evidence_path

    @staticmethod
    def _build_summary(
        status: RuleStatus,
        checks: list[CheckResult],
    ) -> str:
        """Rule Engine全体の概要を生成する。"""

        passed_count = sum(
            check.status is RuleStatus.PASS
            for check in checks
        )
        failed_count = sum(
            check.status is RuleStatus.FAIL
            for check in checks
        )
        review_count = sum(
            check.status is RuleStatus.REVIEW_REQUIRED
            for check in checks
        )

        return (
            f"status={status.value}; "
            f"total={len(checks)}; "
            f"pass={passed_count}; "
            f"fail={failed_count}; "
            f"review_required={review_count}"
        )


def run_rule_engine(
    project_root: Path,
    context: dict[str, Any] | None = None,
    block_on_failure: bool = True,
) -> tuple[EngineResult, Path]:
    """Rule Engineを簡単に実行するための公開関数。"""

    engine = RuleEngine(
        project_root=project_root,
    )

    return engine.run(
        context=context,
        block_on_failure=block_on_failure,
    )