import os
import json
import logging
from colorama import Fore, Style, init as colorama_init
from rich.console import Console
from rich.table import Table

from .providers import OpenAIProvider, ClaudeProvider, GeminiProvider, OllamaProvider

colorama_init()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

console = Console()

def load_prompt_template():
    package_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(package_dir, "prompt.in")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"prompt.in file is missing at {prompt_path}")
    with open(prompt_path, "r") as f:
        return f.read()

def print_json_as_table(json_data, step_number):
    table = Table(title=f"Step {step_number} - JSON Output")

    rows = []
    if isinstance(json_data, dict):
        keys = ["Key", "Value"]
        rows = [[str(k), json.dumps(v, indent=2) if isinstance(v, (dict, list)) else str(v)] for k, v in json_data.items()]
    elif isinstance(json_data, list) and all(isinstance(row, dict) for row in json_data):
        keys = sorted(set(k for d in json_data for k in d.keys()))
        for item in json_data:
            rows.append([str(item.get(k, "")) for k in keys])
    else:
        logger.info("✅ JSON content (non-tabular):")
        logger.info(json.dumps(json_data, indent=2))
        return

    for key in keys:
        table.add_column(key)

    for row in rows:
        table.add_row(*row)

    console.print(table)

def extract_and_check_software(body_text, bibliography_text, pdf_filename, provider, model, save_report=False, client=None):
    os.makedirs("reports", exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pdf_filename))[0]
    report_name = os.path.join("reports", f"{base_name}_report.md")

    prompt_template = load_prompt_template()
    templates = prompt_template.split("---SPLIT STEP---")

    history = []

    if provider == "openai":
        llm = OpenAIProvider(model, client)
    elif provider == "claude":
        llm = ClaudeProvider(model, client)
    elif provider == "gemini":
        llm = GeminiProvider(model, client)
    elif provider == "ollama":
        llm = OllamaProvider(model, client)
    else:
        raise ValueError(f"Unknown provider: {provider}")

    for step_number, template in enumerate(templates, start=1):
        formatted_prompt = template.strip() \
            .replace("{{BODY_TEXT}}", body_text) \
            .replace("{{BIBLIOGRAPHY_TEXT}}", bibliography_text)
        for i, result in enumerate(history, start=1):
            try:
                json_obj = json.loads(result)
                safe_json = json.dumps(json_obj, indent=2)
            except Exception:
                safe_json = result
            formatted_prompt = formatted_prompt.replace(f"{{{{STEP{i}_RESULT}}}}", f"\n```json\n{safe_json}\n```\n")

        logger.info(f"🚀 Step {step_number}/{len(templates)}: Executing prompt step...")
        result = llm.generate(formatted_prompt)
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

    if save_report:
        with open(report_name, "w") as f:
            f.write(history[-1])
        logger.info(f"✅ Report generated: {report_name}")