import os
import sys
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

PROMPT = (
    "あなたはコードレビュー担当者です。以下の git diff を要約し、"
    "変更による影響を説明してください:\n\n{diff}\n"
)


def main(diff_path: str, output_path: str = "analysis.txt"):
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY 環境変数が設定されていません")

    with open(diff_path, "r", encoding="utf-8") as f:
        diff_content = f.read()

    prompt = PROMPT.format(diff=diff_content)

    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    analysis = response.choices[0].message.content

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(analysis)

    print(f"解析結果を {output_path} に書き込みました")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: analyze_diff.py <diff_path> [output_path]")
        sys.exit(1)
    diff_path = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "analysis.txt"
    main(diff_path, output)
