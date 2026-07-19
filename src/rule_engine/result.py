"""Rule Engineの判定結果を表すデータ構造。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RuleStatus(str, Enum):
    """Rule Engineで使用する判定状態。"""

    PASS = "PASS"
    FAIL = "FAIL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


@dataclass(frozen=True)
class CheckResult:
    """一つの確認項目に対する判定結果。"""

    rule_id: str
    rule_name: str
    status: RuleStatus
    message: str
    evidence: dict[str, Any] = field(default_factory=dict)

    @property
    def is_passed(self) -> bool:
        """確認項目がPASSかを返す。"""
        return self.status is RuleStatus.PASS

    @property
    def blocks_output(self) -> bool:
        """対象出力を停止すべき状態かを返す。"""
        return self.status in {
            RuleStatus.FAIL,
            RuleStatus.REVIEW_REQUIRED,
        }

    def to_dict(self) -> dict[str, Any]:
        """ログやEvidence保存に使用できる辞書へ変換する。"""
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "status": self.status.value,
            "message": self.message,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class EngineResult:
    """Rule Engine全体の実行結果。"""

    status: RuleStatus
    checks: tuple[CheckResult, ...]
    summary: str

    @property
    def may_proceed(self) -> bool:
        """対象処理を続行できるかを返す。"""
        return self.status is RuleStatus.PASS

    @property
    def blocks_output(self) -> bool:
        """対象出力を停止する必要があるかを返す。"""
        return not self.may_proceed

    @property
    def failed_checks(self) -> tuple[CheckResult, ...]:
        """FAILとなった確認結果を返す。"""
        return tuple(
            check
            for check in self.checks
            if check.status is RuleStatus.FAIL
        )

    @property
    def review_checks(self) -> tuple[CheckResult, ...]:
        """CEO確認が必要な結果を返す。"""
        return tuple(
            check
            for check in self.checks
            if check.status is RuleStatus.REVIEW_REQUIRED
        )

    def to_dict(self) -> dict[str, Any]:
        """ログやEvidence保存に使用できる辞書へ変換する。"""
        return {
            "status": self.status.value,
            "summary": self.summary,
            "may_proceed": self.may_proceed,
            "checks": [check.to_dict() for check in self.checks],
        }


def determine_engine_status(
    checks: list[CheckResult] | tuple[CheckResult, ...],
) -> RuleStatus:
    """個別の確認結果からRule Engine全体の状態を決定する。"""

    statuses = {check.status for check in checks}

    if RuleStatus.FAIL in statuses:
        return RuleStatus.FAIL

    if RuleStatus.REVIEW_REQUIRED in statuses:
        return RuleStatus.REVIEW_REQUIRED

    return RuleStatus.PASS