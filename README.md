# softwarecitationauditor

**softwarecitationauditor** is a Python command-line tool to extract software mentions from research papers (PDFs) and check whether they are properly cited, using structured LLM queries — supporting OpenAI, Claude, Gemini, and Ollama.

---

## 🚀 Features

- Download papers from URLs or local PDF files
- Extract software mentions from the paper body
- Check if the software is properly cited in the bibliography
- Save analysis reports as Markdown files
- Use a customizable prompt from `prompt.in`
- Process multiple PDFs from an input list file
- Show progress with a progress bar
- ✅ **Experimental:** Use alternative models like Claude or Gemini

---

## 📦 Installation

Clone or download this repository, then install it:

```
uv pip install --editable .
```

Make sure you have `uv` installed. If not, run:

```
pip install uv
```

---

## ⚙️ Usage

### Single PDF

```
softwarecitationauditor https://arxiv.org/pdf/2304.12345.pdf
```

### Multiple PDFs from input file

```
softwarecitationauditor --input-file pdf_list.txt
```

Example `pdf_list.txt`:
```
https://arxiv.org/pdf/2304.12345.pdf
/local/path/paper1.pdf
https://arxiv.org/pdf/2305.67890.pdf
```

---

## 🤖 Model Support

You can switch providers and models using:

```
--provider [openai|claude|gemini] --model [model_name]
```

### Examples:

- OpenAI GPT-4:
  ```
  softwarecitationauditor --provider openai --model gpt-4 https://arxiv.org/pdf/2304.12345.pdf
  ```

- Anthropic Claude:
  ```
  softwarecitationauditor --provider claude --model claude-3-opus https://arxiv.org/pdf/2304.12345.pdf
  ```

- Google Gemini:
  ```
  softwarecitationauditor --provider gemini --model gemini-1.5-pro https://arxiv.org/pdf/2304.12345.pdf
  ```

- Ollama
  ```
  softwarecitationauditor --provider ollama --model llama3 https://arxiv.org/pdf/2304.12345.pdf
  ```

✅ **Note:** You must set the correct API keys or install LLAMA3 using ollama:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- Use command ```ollama install llama3``` to pull llama3 model with ollama API end point.

---

## ✍️ Custom Prompt

The tool uses a `prompt.in` file with clearly defined multi-step prompts. Each step must return only a valid JSON object, with no markdown or extra explanation.

Each step is separated by:
```
--- step N ---
```

Example:

```
--- step 1 ---
Given the following paper body and bibliography, identify all software tools mentioned in the body. Return only a JSON list of software tool names.

Body:
{{BODY_TEXT}}

Bibliography:
{{BIBLIOGRAPHY_TEXT}}

Return only a valid JSON array like: ["Tool1", "Tool2", ...]
Do not include markdown formatting or explanations.

--- step 2 ---
For each software tool identified in Step 1, check if it appears in the bibliography. Return a JSON list of objects with fields: name, cited (true/false), and reason.

Use the same Body and Bibliography as Step 1.
Return only a valid JSON list of objects.

--- step 3 ---
For all software tools where cited is false, generate a suggested BibTeX entry. Return a JSON list of objects with name and bibtex fields.
```

This format ensures predictable parsing and reliable multi-step model execution.

---

## 📁 Output

- Downloaded PDFs → `downloads/` folder
- Reports → `reports/` folder (`<pdf-id>_report.md`)

---

### 🧠 Multi-Step Reasoning

This tool breaks down the analysis into multiple LLM steps:
- Step 1: Identify software tools mentioned
- Step 2: Check if each tool is cited in the bibliography
- Step 3: Suggest missing citations for uncited tools

Each step is designed to produce clean structured JSON output and is handled sequentially via the selected model provider.

---

## 💡 Environment Setup

Export API keys:

```
export OPENAI_API_KEY=sk-xxxxxx
export ANTHROPIC_API_KEY=xx-xxxxxx
export GEMINI_API_KEY=xx-xxxxxx
```

---

## 🧪 Running Tests

```
uv pip install --editable .[test]
pytest
```

---

## 🔥 Project Structure

```
softwarecitationauditor/
├── __init__.py
├── main.py
├── downloader.py
├── extractor.py
├── openai_checker.py
├── prompt.in
downloads/
reports/
tests/
```

---

## 🛡 License

MIT License

---

⚠️ **Disclaimer:**  
Claude and Gemini integration is experimental. API formats may change; test carefully before production use.
