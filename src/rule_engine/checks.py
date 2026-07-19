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