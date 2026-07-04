import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from src.project_os import PROJECT_OS_PROMPT

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("===================================")
print(" ForgeNext Project OS")
print("===================================")
print("終了する場合は exit と入力してください。")

while True:
    user_input = input("\nCEO：")

    if user_input.lower() == "exit":
        print("終了します。")
        break

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
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