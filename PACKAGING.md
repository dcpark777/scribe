# Packaging and Distribution Guide

This guide covers how to package and distribute the Scribe library.

## Overview

Scribe uses Poetry for dependency management and packaging, with support for:
- Wheel distributions (`.whl`)
- Source distributions (`.tar.gz`)
- PyPI publishing
- GitHub Actions CI/CD

## Package Structure

```
scribe/
├── pyproject.toml          # Poetry configuration
├── MANIFEST.in            # Additional packaging rules
├── setup.py               # Compatibility with older tools
├── LICENSE                # MIT License
├── README.md              # Project documentation
├── CHANGELOG.md           # Version history
├── .pypirc.template       # PyPI configuration template
└── .github/workflows/     # CI/CD pipelines
    ├── ci.yml             # Continuous integration
    └── release.yml        # Release automation
```

## Building Packages

### Local Build

```bash
# Build both wheel and source distributions
make build

# Build only wheel
make build-wheel

# Build only source distribution
make build-sdist
```

### Package Contents

The package includes:
- **Core Library**: `scribe/` module
- **Documentation**: Source RST files
- **Examples**: Sample YAML files and configurations
- **License**: MIT License
- **README**: Project documentation

Excluded from package:
- Test files (`tests/`)
- Build artifacts (`dist/`, `build/`)
- Documentation build files (`docs/_build/`)
- Cache files (`__pycache__/`, `.pytest_cache/`)

## Publishing to PyPI

### Prerequisites

1. **PyPI Account**: Create account at [pypi.org](https://pypi.org)
2. **API Token**: Generate API token in account settings
3. **TestPyPI Account**: Create account at [test.pypi.org](https://test.pypi.org)

### Configuration

1. **Copy PyPI configuration template**:
   ```bash
   cp .pypirc.template ~/.pypirc
   ```

2. **Edit `~/.pypirc`** with your API tokens:
   ```ini
   [pypi]
   username = __token__
   password = pypi-your-api-token-here

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-your-test-api-token-here
   ```

### Publishing Process

#### Test Publishing (Recommended First)

```bash
# Publish to TestPyPI
make publish-test
```

#### Production Publishing

```bash
# Publish to PyPI
make publish
```

### Manual Publishing

```bash
# Build packages
poetry build

# Publish to TestPyPI
poetry publish --repository testpypi

# Publish to PyPI
poetry publish
```

## GitHub Actions CI/CD

### Continuous Integration

The `ci.yml` workflow runs on:
- Push to `main` and `develop` branches
- Pull requests to `main`
- Python versions: 3.8, 3.9, 3.10, 3.11, 3.12

**Jobs:**
- **Test**: Run tests, linting, and type checking
- **Build**: Build packages (on main branch)
- **Publish Test**: Publish to TestPyPI (on main branch)
- **Publish**: Publish to PyPI (on release)
- **Docs**: Build and deploy documentation

### Release Automation

The `release.yml` workflow:
- Runs on manual dispatch
- Bumps version (patch/minor/major)
- Creates GitHub release
- Uploads package assets

### Required Secrets

Set these secrets in GitHub repository settings:

- `PYPI_API_TOKEN`: PyPI API token
- `TEST_PYPI_API_TOKEN`: TestPyPI API token
- `GITHUB_TOKEN`: Automatically provided

## Version Management

### Bumping Versions

```bash
# Patch version (0.1.0 -> 0.1.1)
make version-patch

# Minor version (0.1.0 -> 0.2.0)
make version-minor

# Major version (0.1.0 -> 1.0.0)
make version-major
```

### Manual Version Bump

```bash
poetry version patch
poetry version minor
poetry version major
```

## Package Testing

### Local Testing

```bash
# Build and install locally
make install-local

# Test the installed package
scribe --help
scribe --version

# Uninstall
make uninstall-local
```

### TestPyPI Testing

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ scribe

# Test functionality
scribe init
```

## Package Metadata

### Key Information

- **Name**: `scribe`
- **Version**: Managed by Poetry
- **Description**: "A powerful tool for generating dataset definitions in multiple languages and formats from YAML specifications"
- **License**: MIT
- **Author**: Dan Park <dcpark913@gmail.com>
- **Homepage**: https://github.com/dcpark777/scribe
- **Documentation**: https://scribe.readthedocs.io

### Dependencies

**Runtime Dependencies:**
- `python ^3.8`
- `pyyaml ^6.0`
- `click ^8.0`

**Development Dependencies:**
- `pytest ^7.0`
- `pytest-cov ^4.0`
- `black ^22.0`
- `flake8 ^5.0`
- `mypy ^1.0`
- `sphinx >=4.0,<6.0`
- `sphinx-rtd-theme >=1.0,<2.0`

## Troubleshooting

### Common Issues

1. **Package too large**: Check `pyproject.toml` exclude patterns
2. **Missing files**: Verify `include` patterns in `pyproject.toml`
3. **Build failures**: Check Poetry configuration and dependencies
4. **Publishing errors**: Verify API tokens and PyPI credentials

### Debug Commands

```bash
# Check package contents
poetry run python -c "
import zipfile
with zipfile.ZipFile('dist/scribe-0.1.0-py3-none-any.whl', 'r') as z:
    for info in z.infolist():
        print(info.filename)
"

# Validate package
twine check dist/*

# Check package metadata
poetry run python -c "
import tomllib
with open('pyproject.toml', 'rb') as f:
    data = tomllib.load(f)
    print(data['tool']['poetry'])
"
```

## Best Practices

1. **Always test on TestPyPI first**
2. **Update CHANGELOG.md for each release**
3. **Tag releases in Git**
4. **Use semantic versioning**
5. **Keep package size minimal**
6. **Include comprehensive metadata**
7. **Test installation from PyPI**

## Next Steps

After successful packaging:

1. **Update documentation** with installation instructions
2. **Create GitHub release** with release notes
3. **Announce release** on relevant channels
4. **Monitor package downloads** and user feedback
5. **Plan next version** based on user needs
