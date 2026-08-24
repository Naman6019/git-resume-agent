# Contributing to GitResume AI

Thank you for your interest in contributing to **GitResume AI**!

## Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/git-resume-agent.git
   cd git-resume-agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies in editable mode:**
   ```bash
   pip install -e .
   pip install pytest
   ```

4. **Run the test suite:**
   ```bash
   pytest tests/ -v
   ```

## Pull Request Guidelines

- Create a feature branch (`git checkout -b feat/your-feature-name`).
- Keep code clean, modular, and typed (`pydantic`, `typer`, `rich`).
- Ensure all unit tests pass before submitting.
- Submit a clear Pull Request with context on what was changed.
