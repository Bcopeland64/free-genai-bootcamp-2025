# Contributing to AlgoMentor

Thank you for your interest in contributing to AlgoMentor! This document provides guidelines and instructions for contributing to the project. By participating, you agree to abide by our code of conduct.

## Table of Contents

1. [Ways to Contribute](#ways-to-contribute)
2. [Development Setup](#development-setup)
3. [Coding Standards](#coding-standards)
4. [Pull Request Process](#pull-request-process)
5. [Adding New Topics or Problems](#adding-new-topics-or-problems)
6. [Improving Documentation](#improving-documentation)
7. [Reporting Issues](#reporting-issues)

## Ways to Contribute

There are several ways you can contribute to AlgoMentor:

- **Code Contributions**: Add new features, fix bugs, or improve performance
- **Content Contributions**: Add new topics, problems, or explanations
- **Documentation**: Improve guides, READMEs, or inline code documentation
- **Testing**: Identify bugs, edge cases, or usability issues
- **UX/UI Improvements**: Enhance the user interface and experience
- **Feedback**: Provide general feedback or suggestions

## Development Setup

To set up the project for local development:

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/algomentor.git
   cd algomentor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set up Ollama** (for local AI model testing)
   ```bash
   # Follow instructions at https://ollama.ai/
   ollama pull llama3  # Or any other supported model
   ```

5. **Create a new branch for your changes**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Coding Standards

We follow PEP 8 guidelines for Python code. Additionally:

- Use meaningful variable and function names
- Write docstrings for all functions, classes, and modules
- Include type hints where appropriate
- Write unit tests for new features
- Keep functions small and focused on a single responsibility
- Limit line length to 100 characters

For frontend code:
- Follow Streamlit best practices
- Use consistent formatting for UI elements
- Ensure responsive design for different screen sizes

## Pull Request Process

1. **Update your fork** to the latest code from the main repository
2. **Make your changes** in a focused feature branch
3. **Write tests** for new features or bug fixes
4. **Run the test suite** to ensure all tests pass
   ```bash
   pytest
   ```
5. **Run linting** to ensure code quality
   ```bash
   flake8
   ```
6. **Commit your changes** with clear, descriptive commit messages
7. **Push to your fork** and submit a pull request
8. **Describe your changes** in the PR description
9. **Wait for review** and address any feedback

## Adding New Topics or Problems

When adding new data structures or algorithms topics:

1. **Create JSON files** in the appropriate format
2. **Follow the existing pattern** for consistency
3. **Include the following for each topic**:
   - Clear and concise description
   - Time and space complexity analysis
   - Python implementation examples
   - Real-world use cases
   - At least 3 practice problems of varying difficulty

When adding new problems:

1. **Follow the problem template** in `backend/data/problems.json`
2. **Ensure test cases** cover edge cases and typical inputs
3. **Include a reference solution** that passes all test cases
4. **Provide hints** that guide without giving away the solution

## Improving Documentation

Documentation improvements are always welcome! When updating documentation:

1. **Keep explanations clear and concise**
2. **Use examples** to illustrate concepts
3. **Target different experience levels** (beginner to advanced)
4. **Update screenshots** if UI changes affect them
5. **Check for typos and grammatical errors**

## Reporting Issues

When reporting issues:

1. **Check existing issues** to avoid duplicates
2. **Use the issue template** if provided
3. **Include detailed steps** to reproduce the issue
4. **Describe expected vs. actual behavior**
5. **Include relevant environment information**:
   - Operating system
   - Python version
   - Browser type and version (for frontend issues)
   - Error messages or logs

Thank you for contributing to making AlgoMentor better for everyone!