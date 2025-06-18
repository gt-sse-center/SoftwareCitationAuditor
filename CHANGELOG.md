# Changelog

All notable changes to **softwarecitationauditor** will be documented in this file.

---

## [Unreleased]

### Added
- Multi-step prompt execution from `prompt.in` using LLMs (OpenAI, Claude, Gemini, Ollama)
- Step-by-step reasoning across:
  - Step 1: Extract software tools
  - Step 2: Check citations
  - Step 3: Suggest BibTeX for uncited tools
- Rich-based table output for better terminal display of results
- Structured logging (log level: DEBUG, INFO, WARNING)
- Colored CLI output for status and results
- Test coverage for CLI, OpenAI checker, and prompt parsing
- CLI refactored to use `typer` for better UX
- Support for local and remote PDF input
- Custom prompt support via `prompt.in` (multi-step and templated)
- Optional saving of reports (`--save-report`)
- Automatic directory management (`downloads/`, `reports/`)
- Support for OpenAI, Claude, Gemini, and Ollama providers

### Changed
- Converted prompts to enforce **strict JSON-only** responses
- Enhanced PDF extraction using `PyMuPDF` page-wise processing
- Refactored OpenAI checker to support sequential step querying
- Improved progress bar to reflect step-by-step processing
- Enhanced test mocking and error handling during JSON parse

### Fixed
- Robust error reporting for invalid JSON response
- Fixed bugs in CLI argument handling and optional input file
- Resolved CLI install issues by correcting package discovery

---

## [0.1.0] – Initial release

- Basic functionality to extract and analyze software citations in research papers