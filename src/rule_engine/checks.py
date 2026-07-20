"""ForgeNextの会社資産と実行状態を確認する基本チェック。"""

from __future__ import annotations

from pathlib import Path

from .result import CheckResult, RuleStatus


REQUIRED_DOCUMENTS: dict[str, str] = {
    "purpose": "blueprint/00_Foundation/purpose.md",
    "mission": "blueprint/00_Foundation/mission.md",
    "vision": "blueprint/00_Foundation/vision.md",
    "principles": "blueprint/00_Foundation/principles.md",
    "company_constitution": (
        "blueprint/01_Company/company_constitution.md"
    ),
    "company_standard": "blueprint/01_Company/company_standard.md",
    "employee_standard": "blueprint/01_Company/employee_standard.md",
    "organization_audit": "blueprint/organization_audit.md",
    "current_work_state": "current_work_state.md",
}


def check_required_document(
    project_root: Path,
    rule_id: str,
    relative_path: str,
) -> CheckResult:
    """必須文書の存在と内容を確認する。"""

    file_path = project_root / relative_path

    if not file_path.exists():
        return CheckResult(
            rule_id=rule_id,
            rule_name=f"Required document: {relative_path}",
            status=RuleStatus.FAIL,
            message="必須文書が存在しません。",
            evidence={
                "path": str(file_path),
                "exists": False,
            },
        )

    if not file_path.is_file():
        return CheckResult(
            rule_id=rule_id,
            rule_name=f"Required document: {relative_path}",
            status=RuleStatus.FAIL,
            message="指定されたパスがファイルではありません。",
            evidence={
                "path": str(file_path),
                "exists": True,
                "is_file": False,
            },
        )

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return CheckResult(
            rule_id=rule_id,
            rule_name=f"Required document: {relative_path}",
            status=RuleStatus.FAIL,
            message="UTF-8形式で文書を読み込めません。",
            evidence={
                "path": str(file_path),
                "exists": True,
                "readable": False,
            },
        )
    except OSError as error:
        return CheckResult(
            rule_id=rule_id,
            rule_name=f"Required document: {relative_path}",
            status=RuleStatus.FAIL,
            message="文書の読み込み中にエラーが発生しました。",
            evidence={
                "path": str(file_path),
                "error": str(error),
            },
        )

    if not content.strip():
        return CheckResult(
            rule_id=rule_id,
            rule_name=f"Required document: {relative_path}",
            status=RuleStatus.FAIL,
            message="必須文書の内容が空です。",
            evidence={
                "path": str(file_path),
                "exists": True,
                "size": 0,
            },
        )

    return CheckResult(
        rule_id=rule_id,
        rule_name=f"Required document: {relative_path}",
        status=RuleStatus.PASS,
        message="必須文書が存在し、内容を読み込めました。",
        evidence={
            "path": str(file_path),
            "exists": True,
            "size": len(content),
        },
    )


def check_required_documents(project_root: Path) -> list[CheckResult]:
    """ForgeNextの必須文書を一括確認する。"""

    results: list[CheckResult] = []

    for document_name, relative_path in REQUIRED_DOCUMENTS.items():
        results.append(
            check_required_document(
                project_root=project_root,
                rule_id=f"document.{document_name}",
                relative_path=relative_path,
            )
        )

    return results


def check_document_markers(
    project_root: Path,
    rule_id: str,
    relative_path: str,
    required_markers: tuple[str, ...],
    rule_name: str | None = None,
) -> CheckResult:
    """Evidence文書に必要な記述が存在するか確認する。"""

    file_path = project_root / relative_path
    display_name = rule_name or f"Document markers: {relative_path}"

    if not file_path.exists():
        return CheckResult(
            rule_id=rule_id,
            rule_name=display_name,
            status=RuleStatus.FAIL,
            message="確認対象のEvidence文書が存在しません。",
            evidence={
                "path": str(file_path),
                "exists": False,
                "required_markers": list(required_markers),
            },
        )

    if not file_path.is_file():
        return CheckResult(
            rule_id=rule_id,
            rule_name=display_name,
            status=RuleStatus.FAIL,
            message="確認対象のパスがファイルではありません。",
            evidence={
                "path": str(file_path),
                "exists": True,
                "is_file": False,
            },
        )

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return CheckResult(
            rule_id=rule_id,
            rule_name=display_name,
            status=RuleStatus.FAIL,
            message="Evidence文書をUTF-8形式で読み込めません。",
            evidence={
                "path": str(file_path),
                "readable": False,
            },
        )
    except OSError as error:
        return CheckResult(
            rule_id=rule_id,
            rule_name=display_name,
            status=RuleStatus.FAIL,
            message="Evidence文書の読み込み中にエラーが発生しました。",
            evidence={
                "path": str(file_path),
                "error": str(error),
            },
        )

    missing_markers = [
        marker
        for marker in required_markers
        if marker not in content
    ]

    if missing_markers:
        return CheckResult(
            rule_id=rule_id,
            rule_name=display_name,
            status=RuleStatus.FAIL,
            message="Evidence文書に必要な記述が不足しています。",
            evidence={
                "path": str(file_path),
                "required_markers": list(required_markers),
                "missing_markers": missing_markers,
            },
        )

    return CheckResult(
        rule_id=rule_id,
        rule_name=display_name,
        status=RuleStatus.PASS,
        message="Evidence文書に必要な記述が確認できました。",
        evidence={
            "path": str(file_path),
            "required_markers": list(required_markers),
            "missing_markers": [],
        },
    )


def check_incident_closure_evidence(
    project_root: Path,
    incident_id: str,
    relative_path: str,
    required_markers: tuple[str, ...],
    ceo_approved: bool = False,
) -> list[CheckResult]:
    """インシデントのEvidenceとCEO承認を確認する。"""

    results = [
        check_document_markers(
            project_root=project_root,
            rule_id=f"incident.{incident_id}.evidence",
            relative_path=relative_path,
            required_markers=required_markers,
            rule_name=f"Incident closure evidence: {incident_id}",
        )
    ]

    results.append(
        CheckResult(
            rule_id=f"incident.{incident_id}.ceo_approval",
            rule_name=f"CEO closure approval: {incident_id}",
            status=(
                RuleStatus.PASS
                if ceo_approved
                else RuleStatus.REVIEW_REQUIRED
            ),
            message=(
                "CEOによる正式クローズ承認が確認されました。"
                if ceo_approved
                else "CEOによる正式クローズ判断が必要です。"
            ),
            evidence={
                "incident_id": incident_id,
                "ceo_approved": ceo_approved,
            },
        )
    )

    return results