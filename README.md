
# softwarecitationauditor

**softwarecitationauditor** is a Python command-line tool to extract software mentions from research papers (PDFs) and check whether they are properly cited, using the OpenAI API — with **experimental support** for Claude and Gemini.

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

## ⚡ Experimental: Using Other Models

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

✅ **Note:** You must set the correct API keys:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`

---

## ✍️ Custom Prompt

Edit the `prompt.in` file in the `softwarecitationauditor` folder:

```
Given the following paper body and bibliography, extract the software tools used in the paper and check if they are properly cited.

Body:
{{BODY_TEXT}}

Bibliography:
{{BIBLIOGRAPHY_TEXT}}

Return the result as a Markdown table with columns: Software, Mentioned, Properly Cited.
```

---

## 📁 Output

- Downloaded PDFs → `downloads/` folder
- Reports → `reports/` folder (`<pdf-id>_report.md`)

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
