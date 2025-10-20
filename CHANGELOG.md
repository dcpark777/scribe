# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet

### Changed
- Nothing yet

### Deprecated
- Nothing yet

### Removed
- Nothing yet

### Fixed
- Nothing yet

### Security
- Nothing yet

## [0.1.0] - 2024-01-15

### Added
- Initial release of Scribe
- YAML dataset definition parser with comprehensive validation
- Python dataclass generator with type hints and validation
- Scala case class generator with Apache Spark integration
- Protocol Buffers generator with multi-language support
- CLI interface with `scribe init` and `scribe generate` commands
- Comprehensive configuration system for all target languages
- Support for primitive types (string, integer, number, boolean)
- Support for complex types (array, object, enum, oneOf)
- Field constraints and validation rules
- Documentation and ownership tracking
- Extensive test coverage (68 tests, 82% coverage)
- Professional documentation with Sphinx
- GitHub Actions CI/CD pipeline
- PyPI packaging and distribution setup

### Features
- **Multi-Language Support**: Generate code for Python, Scala, and Protocol Buffers
- **Type Safety**: Maintain consistent types across all generated code
- **Validation**: Built-in validation rules and constraints
- **Documentation**: Automatic generation of documentation and comments
- **Configuration**: Flexible configuration system for each language
- **CLI Interface**: Easy-to-use command-line interface
- **Extensible**: Easy to add new languages and formats

### Technical Details
- Python 3.8+ support
- Poetry for dependency management
- Comprehensive test suite with pytest
- Code quality tools (black, flake8, mypy)
- Professional documentation system
- MIT License
