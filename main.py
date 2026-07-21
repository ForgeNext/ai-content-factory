"""ForgeNext Project OS runtime entry point."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from src.prompts.ceo import CEO_PROMPT
from src.prompts.project_os import PROJECT_OS_PROMPT
from src.rule_engine.rule_engine import (
    RuleEngineBlockedError,
    run_rule_engine,
)


PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEYが設定されていません。"
        "プロジェクトルートの.envを確認してください。"
    )

client = OpenAI(api_key=api_key)


def run_pre_execution_check(
    user_input: str,
) -> bool:
    """OpenAI API実行前にForgeNext Rule Engineを通す。"""

    context = {
        "runtime": {
            "entry_point": "main.py",
            "operation": "project_os_response",
            "requested_by": "CEO",
            "user_input_present": bool(user_input.strip()),
        }
    }

    try:
        result, evidence_path = run_rule_engine(
            project_root=PROJECT_ROOT,
            context=context,
            block_on_failure=True,
        )
    except RuleEngineBlockedError as error:
        print("\n===================================")
        print(" Rule Engine: OUTPUT BLOCKED")
        print("===================================")
        print(f"Status: {error.result.status.value}")
        print(f"Summary: {error.result.summary}")

        if error.evidence_path is not None:
            print(f"Evidence: {error.evidence_path}")

        print(
            "FAILまたはREVIEW_REQUIREDのため、"
            "OpenAI APIの実行を停止しました。"
        )
        return False

    print("\n===================================")
    print(" Rule Engine: PASS")
    print("===================================")
    print(f"Summary: {result.summary}")
    print(f"Evidence: {evidence_path}")

    return True


def main() -> None:
    """ForgeNext Project OSを対話形式で実行する。"""

    print("===================================")
    print(" ForgeNext Project OS")
    print("===================================")
    print("終了する場合は exit と入力してください。")

    while True:
        user_input = input("\nCEO：").strip()

        if user_input.lower() == "exit":
            print("ForgeNext Project OSを終了します。")
            break

        if not user_input:
            print("入力が空です。指示を入力してください。")
            continue

        if not run_pre_execution_check(user_input):
            continue

        response = client.responses.create(
            model="gpt-5.5",
            input=[
                {
                    "role": "system",
                    "content": CEO_PROMPT,
                },
                {
                    "role": "system",
                    "content": PROJECT_OS_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )

        print("\nProject OS：")
        print(response.output_text)


if __name__ == "__main__":
    main()
