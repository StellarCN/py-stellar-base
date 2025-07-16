# Contributing to py-stellar-base

Thank you for considering contributing to py-stellar-base! This document provides guidelines and information about how to contribute to this project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Documentation](#documentation)

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone git@github.com:your-username/py-stellar-base.git
   cd py-stellar-base
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/StellarCN/py-stellar-base.git
   ```

## Development Setup

### Prerequisites

- Python 3.9 or higher
- uv for package management

### Environment Setup

1. **Create a virtual environment**:

   ```bash
   uv venv
   ```

2. **Install dependencies**:

   ```bash
   uv sync --all-extras --all-groups
   ```

### Running Tests

To run the test suite, use the following command:

```bash
make unit-test
```

### Code Formatting and Linting

This project uses several tools to maintain code quality:

```bash
# Format code
make pre-commit

# Type check
make type-check
```

## Making Changes

### Before You Start

1. **Check existing issues** to see if your change is already being discussed
2. **Create an issue** for new features or significant changes to discuss the approach and get approval
3. **For bug fixes**: Reference the existing issue or create one if it doesn't exist
4. **Wait for maintainer feedback** before starting work on significant changes
5. **Keep changes focused** - one pull request per feature/fix

### Commit Messages

Follow conventional commit format:

- `feat: add support for med25519 public keys`
- `fix: resolve strkey validation issue`
- `docs: update API documentation`
- `test: add tests for new functionality`
- `refactor: improve code structure`

## Testing

- **All new features** must include tests
- **Bug fixes** should include regression tests
- **Follow existing test patterns** in the `tests/` directory

## Submitting Changes

### Pull Request Process

1. **Create or reference an issue first**:

   - **For new features or significant changes**: Create an issue to discuss the proposed changes before starting work
   - **For bug fixes**: Reference the existing issue or create one if it doesn't exist
   - **For documentation updates**: You can proceed without an issue for minor changes
   - Wait for maintainer approval before starting significant work

2. **Update your fork**:

   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

3. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes** and commit them

5. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a pull request** on GitHub

### Pull Request Requirements

- **Issue exists and is referenced** (required for new features and significant changes)
- Tests pass locally
- Code follows project style guidelines
- Documentation is updated if needed
- Commit messages follow conventional format
- PR description clearly explains the changes

## Documentation

### Code Documentation

- **All public APIs** must have docstrings
- **Follow reStructuredText docstring format**:

  ```python
  @staticmethod
  def decode_med25519_public_key(data: str) -> bytes:
      """Decodes encoded med25519 public key strkey (M...) to raw data.

      :param data: encoded med25519 public key strkey
      :return: raw bytes
      :raises:
          :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
      """
      try:
          return _decode_check(_VersionByte.MED25519_PUBLIC_KEY, data)
      except Exception:
          raise ValueError(f"Invalid Med25519 Public Key: {data}")
  ```

### Examples

- **Add examples** for new features in the `examples/` directory (if applicable)
- **Keep examples simple** and well-commented

## Release Process

Releases are managed by the maintainers and follow semantic versioning:

- **Major versions** (X.0.0): Breaking changes
- **Minor versions** (X.Y.0): New features, backward compatible
- **Patch versions** (X.Y.Z): Bug fixes, backward compatible

Thank you for contributing to py-stellar-base! Your efforts help make the Stellar ecosystem better for everyone.
