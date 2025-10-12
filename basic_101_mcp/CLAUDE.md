# Development Guidelines

This document contains critical information about working with this codebase. Follow these guidelines precisely: in doubt ask me.

# IMPORTANT: **follow the specifications**
- [uv documentation](https://docs.astral.sh/uv/)

## 🤝 A2A (Agent‑to‑Agent Protocol)
- [A2A specifications (latest version 2025.1)](https://a2a-protocol.org/dev/specification/)
- **GitHub (official project):** [a2aproject/A2A](https://github.com/a2aproject/A2A)  
- **SDKs & Samples:**  
  - [a2aproject/a2a-python](https://github.com/a2aproject/a2a-python)  
  - [a2aproject/a2a-samples](https://github.com/a2aproject/a2a-samples)  

**Usage:**  
Consult these repos for canonical implementations and SDK usage patterns. Only adopt code that is **recently updated** and **not marked deprecated**.


## 🛠️ Google ADK (Agent Development Kit)
- **Specification:** [ADK documentation](https://google.github.io/adk-docs/)
- **Python API Docs:** [ADK APIs] (https://google.github.io/adk-docs/api-reference/python/)  
- **GitHub (toolkits & samples):**  
  - [google/adk-python](https://github.com/google/adk-python)  
  - [google/adk-samples](https://github.com/google/adk-samples)  

**Usage:**  
Reference implementations and sample agents. Use for inspiration, but always validate alignment with the **latest ADK spec** and ensure the code is actively maintained.

## 🔗 MCP (Model Context Protocol)
- **Specification:** [MCP specification (latest)](https://modelcontextprotocol.info/specification/)  
- **GitHub (reference servers):** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)  
- [MCP specifications (latest version 2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18)
- [MCP examples](https://modelcontextprotocol.io/examples)
- [MCP Schema References](https://modelcontextprotocol.io/specification/2025-06-18/schema)
- [MCP Schema References - Resource](https://modelcontextprotocol.io/specification/2025-06-18/schema#resource)

**Usage:**  
Contains reference implementations and community servers. Review for patterns, but only reuse code that is **actively maintained** and **security‑audited**.



## Rules Summary
- Minimalistic: no unused imports, no dead code
- Documented: PEP 257 docstrings, inline comments only when essential
- Step‑by‑step: explicit, no hidden side effects
- 100% compliant: PEP 8, PEP 484, validated with ruff + mypy
- No deprecated code: check Python changelog
- Latest specs: prefer modern stdlib (pathlib, dataclasses)
- Simple code: single responsibility, <50 lines per function
- No fluff: no placeholders, no unused deps
- Must work: fresh uv environment always reproducible
- Eval & test: pytest required, coverage recommended
Run Tests
uv run pytest --maxfail=1 --disable-warnings -q

## Python Version
- Python 3.13.x
- Latest stable release: Python.org Downloads
- No deprecated modules or syntax
- Must pass python -Wd (treat warnings as errors)

### Environment & Package Management
- uv for environment and dependency management
- Docs: uv documentation
- Always pin dependencies in pyproject.toml
- Commit uv.lock for reproducibility

## Core Development Rules

1. Package Management
   - ONLY use uv, NEVER pip
   - Installation: `uv add package`
   - Running tools: `uv run tool`
   - Upgrading: `uv add --dev package --upgrade-package package`
   - FORBIDDEN: `uv pip install`, `@latest` syntax

2. Code Quality
   - Type hints required for all code
   - use pyrefly for type checking
     - run `pyrefly init` to start
     - run `pyrefly check` after every change and fix resultings errors
   - Public APIs must have docstrings
   - Functions must be focused and small
   - Follow existing patterns exactly
   - Line length: 88 chars maximum

3. Testing Requirements
   - Framework: `uv run pytest`
   - Async testing: use anyio, not asyncio
   - Coverage: test edge cases and errors
   - New features require tests
   - Bug fixes require regression tests

4. Code Style
    - PEP 8 naming (snake_case for functions/variables)
    - Class names in PascalCase
    - Constants in UPPER_SNAKE_CASE
    - Document with docstrings
    - Use f-strings for formatting

## Development Philosophy

- **Simplicity**: Write simple, straightforward code
- **Readability**: Make code easy to understand
- **Performance**: Consider performance without sacrificing readability
- **Maintainability**: Write code that's easy to update
- **Testability**: Ensure code is testable
- **Reusability**: Create reusable components and functions
- **Less Code = Less Debt**: Minimize code footprint

## Coding Best Practices

- **Early Returns**: Use to avoid nested conditions
- **Descriptive Names**: Use clear variable/function names (prefix handlers with "handle")
- **Constants Over Functions**: Use constants where possible
- **DRY Code**: Don't repeat yourself
- **Functional Style**: Prefer functional, immutable approaches when not verbose
- **Minimal Changes**: Only modify code related to the task at hand
- **Function Ordering**: Define composing functions before their components
- **TODO Comments**: Mark issues in existing code with "TODO:" prefix
- **Simplicity**: Prioritize simplicity and readability over clever solutions
- **Build Iteratively** Start with minimal functionality and verify it works before adding complexity
- **Run Tests**: Test your code frequently with realistic inputs and validate outputs
- **Build Test Environments**: Create testing environments for components that are difficult to validate directly
- **Functional Code**: Use functional and stateless approaches where they improve clarity
- **Clean logic**: Keep core logic clean and push implementation details to the edges
- **File Organsiation**: Balance file organization with simplicity - use an appropriate number of files for the project scale

## System Architecture
- use Google A2A for Agent to Agent calls
- use FastMCP server to serve Agents' AgentCards as resources
- Agents 
- use pydantic and langchain
- this project is a very simple chatbot. Keep files to a minimum


## GitHub rules

- Create a detailed message of what changed. Focus on the high level description of
  the problem it tries to solve, and how it is solved. Don't go into the specifics of the
  code unless it adds clarity.

- Always commit and push in one go

- Commit practices
  - Make atomic commits (one logical change per commit)


## Python Tools

- use context7 mcp to check details of libraries

## Code Formatting

1. Ruff
   - Format: `uv run ruff format .`
   - Check: `uv run ruff check .`
   - Fix: `uv run ruff check . --fix`
   - Critical issues:
     - Line length (88 chars)
     - Import sorting (I001)
     - Unused imports
   - Line wrapping:
     - Strings: use parentheses
     - Function calls: multi-line with proper indent
     - Imports: split into multiple lines

2. Type Checking
  - run `pyrefly init` to start
  - run `pyrefly check` after every change and fix resultings errors
   - Requirements:
     - Explicit None checks for Optional
     - Type narrowing for strings
     - Version warnings can be ignored if checks pass


## Error Resolution

1. CI Failures
   - Fix order:
     1. Formatting
     2. Type errors
     3. Linting
   - Type errors:
     - Get full line context
     - Check Optional types
     - Add type narrowing
     - Verify function signatures

2. Common Issues
   - Line length:
     - Break strings with parentheses
     - Multi-line function calls
     - Split imports
   - Types:
     - Add None checks
     - Narrow string types
     - Match existing patterns

3. Best Practices
   - Check git status before commits
   - Run formatters before type checks
   - Keep changes minimal
   - Follow existing patterns
   - Document public APIs
   - Test thoroughly
