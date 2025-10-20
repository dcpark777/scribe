Contributing
============

Thank you for your interest in contributing to Scribe! This document provides guidelines for contributing to the project.

Getting Started
---------------

1. **Fork the repository** on GitHub
2. **Clone your fork** locally::

   git clone https://github.com/your-username/scribe.git
   cd scribe

3. **Install development dependencies**::

   poetry install

4. **Run tests** to ensure everything works::

   make test

Development Setup
-----------------

**Prerequisites:**

* Python 3.8 or higher
* Poetry for dependency management
* Git for version control

**Development Environment:**

1. **Install dependencies**::

   poetry install

2. **Run tests**::

   make test

3. **Run linting**::

   make lint

4. **Format code**::

   make format

5. **Type checking**::

   make type-check

Contributing Guidelines
----------------------

**Code Style:**

* Follow PEP 8 for Python code
* Use type hints for all functions and methods
* Write comprehensive docstrings
* Use meaningful variable and function names

**Testing:**

* Write tests for all new functionality
* Ensure all tests pass before submitting
* Aim for high test coverage
* Use descriptive test names

**Documentation:**

* Update documentation for any API changes
* Add examples for new features
* Keep the user guide up to date

**Commit Messages:**

* Use clear, descriptive commit messages
* Reference issues when applicable
* Use conventional commit format when possible

Pull Request Process
--------------------

1. **Create a feature branch**::

   git checkout -b feature/your-feature-name

2. **Make your changes** following the guidelines above

3. **Run tests and linting**::

   make test
   make lint
   make format

4. **Commit your changes**::

   git commit -m "Add your feature"

5. **Push to your fork**::

   git push origin feature/your-feature-name

6. **Create a pull request** on GitHub

**Pull Request Requirements:**

* All tests must pass
* Code must be properly formatted
* Documentation must be updated
* Changes must be backwards compatible (unless it's a major version)

Issue Reporting
---------------

**Before reporting an issue:**

1. Check if the issue has already been reported
2. Try the latest version of Scribe
3. Provide a minimal reproduction case

**When reporting an issue, include:**

* Scribe version
* Python version
* Operating system
* Steps to reproduce
* Expected behavior
* Actual behavior
* Error messages or logs

Feature Requests
----------------

**When requesting a feature:**

1. Check if the feature has already been requested
2. Provide a clear description of the feature
3. Explain the use case and benefits
4. Consider implementation complexity

**Good feature requests include:**

* Clear problem statement
* Proposed solution
* Use cases and examples
* Potential implementation approach

Code of Conduct
---------------

**Our Pledge:**

We are committed to providing a welcoming and inclusive environment for all contributors.

**Expected Behavior:**

* Be respectful and inclusive
* Use welcoming and inclusive language
* Be respectful of differing viewpoints
* Accept constructive criticism
* Focus on what's best for the community

**Unacceptable Behavior:**

* Harassment or discrimination
* Trolling or inflammatory comments
* Personal attacks
* Public or private harassment
* Publishing private information

License
-------

By contributing to Scribe, you agree that your contributions will be licensed under the same license as the project (MIT License).

Contact
-------

* **GitHub Issues**: For bug reports and feature requests
* **Discussions**: For questions and general discussion
* **Email**: For security issues or private matters

Thank you for contributing to Scribe!
