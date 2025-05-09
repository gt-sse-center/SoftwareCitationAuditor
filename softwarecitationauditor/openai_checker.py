import os

def load_prompt_template():
    package_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(package_dir, "prompt.in")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"prompt.in file is missing at {prompt_path}")
    with open(prompt_path, "r") as f:
        return f.read()

def extract_and_check_software(body_text, bibliography_text, pdf_filename, provider, model):
    os.makedirs("reports", exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pdf_filename))[0]
    report_name = os.path.join("reports", f"{base_name}_report.md")

    prompt_template = load_prompt_template()
    prompt = prompt_template.replace("{{BODY_TEXT}}", body_text[:4000]) \
                            .replace("{{BIBLIOGRAPHY_TEXT}}", bibliography_text[:4000])

    answer = ""
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content

    elif provider == "claude":
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.content[0].text

    elif provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt)
        answer = response.text

    else:
        raise ValueError(f"Unknown provider: {provider}")

    with open(report_name, "w") as f:
        f.write(answer)
    print(f"✅ Report generated: {report_name}")