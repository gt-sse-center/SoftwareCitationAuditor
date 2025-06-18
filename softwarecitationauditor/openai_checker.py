import os
import json
import logging
from openai import OpenAI
from colorama import Fore, Style, init as colorama_init
from rich.console import Console
from rich.table import Table
colorama_init()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def load_prompt_template():
    package_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(package_dir, "prompt.in")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"prompt.in file is missing at {prompt_path}")
    with open(prompt_path, "r") as f:
        return f.read()

console = Console()

def print_json_as_table(json_data, step_number):
    if isinstance(json_data, dict):
        table = Table(title=f"Step {step_number} - JSON Output")
        table.add_column("Key")
        table.add_column("Value")
        for key, value in json_data.items():
            value_str = json.dumps(value, indent=2) if isinstance(value, (dict, list)) else str(value)
            table.add_row(str(key), value_str)
        console.print(table)
    elif isinstance(json_data, list) and all(isinstance(row, dict) for row in json_data):
        keys = sorted(set(k for d in json_data for k in d.keys()))
        table = Table(title=f"Step {step_number} - JSON Output")
        for key in keys:
            table.add_column(str(key))
        for item in json_data:
            table.add_row(*(str(item.get(k, "")) for k in keys))
        console.print(table)
    else:
        logger.info("✅ JSON content (non-tabular):")
        logger.info(json.dumps(json_data, indent=2))

def extract_and_check_software(body_text, bibliography_text, pdf_filename, provider, model, save_report=False, client=None):
    os.makedirs("reports", exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pdf_filename))[0]
    report_name = os.path.join("reports", f"{base_name}_report.md")

    prompt_template = load_prompt_template()
    templates = prompt_template.split("---SPLIT STEP---")

    history = []
    answer = ""

    for step_number, template in enumerate(templates, start=1):
        # Replace placeholders
        formatted_prompt = template.strip() \
            .replace("{{BODY_TEXT}}", body_text) \
            .replace("{{BIBLIOGRAPHY_TEXT}}", bibliography_text)
        for i, result in enumerate(history, start=1):
            formatted_prompt = formatted_prompt.replace(f"{{{{STEP{i}_RESULT}}}}", result)

        logger.info(f"🚀 Step {step_number}/{len(templates)}: Executing prompt step...")

        if provider == "openai":
            client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": formatted_prompt}],
            )
            result = response.choices[0].message.content.strip()
        elif provider == "claude":
            import anthropic
            client = client or anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model=model,
                max_tokens=4000,
                messages=[{"role": "user", "content": formatted_prompt}]
            )
            result = response.content[0].text.strip()
        elif provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            client = client or genai.GenerativeModel(model)
            response = client.generate_content(formatted_prompt)
            result = response.text.strip()
        elif provider == "ollama":
            import ollama
            client = client or ollama
            model = model or "llama3"
            try:
                response = client.chat(
                    model=model,
                    messages=[{"role": "user", "content": formatted_prompt}]
                )
                result = response["message"]["content"].strip()
            except Exception as e:
                raise RuntimeError(f"Ollama REST call failed: {e}")
        else:
            raise ValueError(f"Unknown provider: {provider}")

        logger.debug(f"Raw result for step {step_number}:\n{result}")

        history.append(result)
        try:
            parsed_json = json.loads(result)
            logger.info(f"✅ Step {step_number} completed.")
            print_json_as_table(parsed_json, step_number)
        except json.JSONDecodeError as e:
            logger.warning(f"Step {step_number} result is not valid JSON. Showing preview instead.")
            logger.debug(f"JSON decode error: {e}")
            logger.warning(f"✅ Step {step_number} completed. Output (raw text preview):\n{result[:200]}{'...' if len(result) > 200 else ''}")

    answer = history[-1]

    if save_report:
        with open(report_name, "w") as f:
            f.write(answer)
        logger.info(f"✅ Report generated: {report_name}")