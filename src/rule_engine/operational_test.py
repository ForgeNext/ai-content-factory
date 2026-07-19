"""Rule Engine Stage 3 operational verification."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from src.rule_engine import (
    RuleEngineBlockedError,
    run_rule_engine,
)


def copy_required_project_files(
    source_root: Path,
    test_root: Path,
) -> None:
    """Rule Engineの確認に必要な会社文書をテスト領域へコピーする。"""

    targets = [
        Path("blueprint/00_Foundation/purpose.md"),
        Path("blueprint/00_Foundation/mission.md"),
        Path("blueprint/00_Foundation/vision.md"),
        Path("blueprint/00_Foundation/principles.md"),
        Path("blueprint/01_Company/company_constitution.md"),
        Path("blueprint/01_Company/company_standard.md"),
        Path("blueprint/01_Company/employee_standard.md"),
        Path("blueprint/organization_audit.md"),
        Path("current_work_state.md"),
    ]

    for relative_path in targets:
        source_path = source_root / relative_path
        destination_path = test_root / relative_path

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source_path,
            destination_path,
        )


def run_operational_verification() -> None:
    """正常系・異常系・回復系を順番に検証する。"""

    source_root = Path.cwd()

    with tempfile.TemporaryDirectory(
        prefix="forgenext_rule_engine_",
    ) as temporary_directory:
        test_root = Path(temporary_directory)

        copy_required_project_files(
            source_root=source_root,
            test_root=test_root,
        )

        print("=== NORMAL CASE ===")

        normal_result, normal_evidence = run_rule_engine(
            project_root=test_root,
            context={
                "test_case": "normal",
            },
        )

        print(normal_result.status.value)
        print(normal_result.summary)
        print(normal_evidence)

        print()
        print("=== FAILURE CASE ===")

        broken_document = (
            test_root
            / "blueprint"
            / "00_Foundation"
            / "mission.md"
        )

        original_content = broken_document.read_text(
            encoding="utf-8",
        )

        broken_document.write_text(
            "",
            encoding="utf-8",
        )

        try:
            run_rule_engine(
                project_root=test_root,
                context={
                    "test_case": "failure",
                },
            )
        except RuleEngineBlockedError as error:
            print(error.result.status.value)
            print(error.result.summary)
            print(error.evidence_path)
        else:
            raise AssertionError(
                "異常系でRule Engineが停止しませんでした。"
            )

        print()
        print("=== RECOVERY CASE ===")

        broken_document.write_text(
            original_content,
            encoding="utf-8",
        )

        recovery_result, recovery_evidence = run_rule_engine(
            project_root=test_root,
            context={
                "test_case": "recovery",
            },
        )

        print(recovery_result.status.value)
        print(recovery_result.summary)
        print(recovery_evidence)


if __name__ == "__main__":
    run_operational_verification()