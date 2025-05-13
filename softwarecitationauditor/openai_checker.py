import os
from openai import OpenAI

def load_prompt_template():
    package_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(package_dir, "prompt.in")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"prompt.in file is missing at {prompt_path}")
    with open(prompt_path, "r") as f:
        return f.read()

def extract_and_check_software(body_text, bibliography_text, pdf_filename, provider, model, client=None):
    os.makedirs("reports", exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pdf_filename))[0]
    report_name = os.path.join("reports", f"{base_name}_report.md")

    prompt_template = load_prompt_template()
    prompt = prompt_template.replace("{{BODY_TEXT}}", body_text) \
                            .replace("{{BIBLIOGRAPHY_TEXT}}", bibliography_text)

    answer = ""
    if provider == "openai":
        client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content
    elif provider == "claude":
        import anthropic
        client = client or anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.content[0].text
    elif provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        client = client or genai.GenerativeModel(model)
        response = client.generate_content(prompt)
        answer = response.text
    elif provider == "ollama":
        import ollama

        client = client or ollama
        model = model or "llama3"

        try:
            response = client.chat(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Ollama REST call failed: {e}")
    else:
        raise ValueError(f"Unknown provider: {provider}")

    with open(report_name, "w") as f:
        f.write(answer)
    print(f"✅ Report generated: {report_name}")