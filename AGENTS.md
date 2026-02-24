# AGENTS.md

> Purpose: This file provides context, conventions, and setup instructions for AI agents working on this repository.

## 1. Project Overview
- Description: This repository contains scripts to convert PDF files to text files.
- Language: Python
- Package Manager: `uv` (Do not use pip or poetry directly)

## 2. Directory Structure

```
.
├── .gitignore                    # Git ignore file
├── AGENTS.md                     # This file
├── example/pdf/                  # Example PDF files to use for testing
├── example/txt/                  # Example text files to use for testing
├── extract_pdf_text.py           # Script to extract text from PDF files
├── package-lock.json             # Lock file for dependencies
├── pyproject.toml                # Project configuration
├── README.md                     # Project description
└── uv.lock                       # Lock file for dependencies
```

## 3. Development Workflow & Commands
Always use `uv` for package management and script execution.

### Setup
- First time setup: `uv sync` (Installs environment based on lockfile)
- Update environment: `uv sync`

### Dependency Management
- Add production dependency: `uv add <package_name>`
- Add dev/test dependency: `uv add <package_name> --group test`
- Remove dependency: `uv remove <package_name>`

### Running Code
- Run script: `uv run python <script_path>`

### Testing
- Install test environment: `uv sync --group test`
- Run all tests: `uv run pytest`
- Write tests for new features
- Maintain existing test coverage
- Use pytest fixtures for common setup
- Create separate test files for each module
- Create test in a `tests/` directory at the root level
- Name test files as `test_<module>.py`
- Test coverage: `uv run pytest --cov=.`
- **Important**: Always test the script with the PDF files in the `example/pdf/` directory and compare the output with the text files in the `example/txt/` directory.

## Development Workflow
1. Write/update tests first (TDD approach)
2. Implement changes
3. Run tests to ensure they pass
4. Format code with Black

## 4. Coding Conventions & Style

### Formatting
- Formatter: Black
  - Command: `uv run black .`
  - Rule: Always run formatting before declaring a task complete.
- Follow PEP 8 conventions
- Use type hints where appropriate
- Write docstrings for functions and classes

### Commenting
- Use clear and concise comments to explain non-obvious code
- Use docstrings for all public modules, functions, classes, and methods


### Type Hinting
- Use standard Python type hints for function arguments and return values.
- Example: `def my_func(name: str) -> int:`

## 5. Critical Rules for Agents
- Do not update `uv.lock` manually. Use `uv add` or `uv sync`.
- Check `pyproject.toml` to see existing dependencies before adding new ones.
- Run tests after every significant code change to ensure no regressions.
- Ensure code is formatted with Black
- Preserve existing code style and patterns
- Aways update the README.md file with instructions for running the code. Be concise, don't include unnecessary information. Focus on how to run the code for testing.
- Ask for clarification if requirements are unclear
