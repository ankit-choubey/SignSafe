# Contributing to SignSafe

Thank you for your interest in contributing to SignSafe! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/signsafe.git`
3. Install dependencies: `python install_dependencies.py`
4. Create a new branch: `git checkout -b feature-name`

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
```bash
# Install dependencies
python install_dependencies.py

# Create environment file (optional)
cp .env.template .env
# Add your API keys to .env file
```

### Running the Application
```bash
streamlit run app.py
```

## Project Structure

```
signsafe/
├── src/                    # Source code
│   ├── pipeline/          # Document processing pipeline
│   ├── ui/               # User interface components
│   └── utils/            # Utility modules
├── docs/                 # Documentation
├── tests/                # Test files
├── app.py               # Main application entry point
├── install_dependencies.py # Dependency installer
└── requirements.txt     # Python dependencies
```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

## Making Changes

1. Create a feature branch from `main`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation if needed
6. Commit with clear messages

## Commit Messages

Use clear, descriptive commit messages:
- `feat: add voice chat functionality`
- `fix: resolve PDF parsing issue`
- `docs: update installation guide`
- `refactor: simplify risk analysis logic`

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the version numbers in any examples files and the README.md
3. Ensure your code follows the project's coding standards
4. Include relevant test cases
5. Make sure all tests pass
6. Request review from maintainers

## Testing

- Write unit tests for new features
- Ensure existing tests still pass
- Test with various document types (PDF, images)
- Verify AI integrations work correctly

## Documentation

- Update docstrings for any modified functions
- Add comments for complex logic
- Update README.md if adding new features
- Include examples for new functionality

## Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Sample documents if relevant (without sensitive content)

## Feature Requests

For feature requests, please describe:
- The use case or problem it solves
- Proposed solution
- Any alternatives considered
- Potential impact on existing functionality

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers get started
- Focus on what's best for the community

## Questions?

If you have questions about contributing, please open an issue or reach out to the maintainers.

Thank you for contributing to SignSafe!