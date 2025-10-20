#!/usr/bin/env python3
"""
Setup script for Scribe.

This file provides compatibility with older packaging tools
while Poetry handles the actual packaging.
"""

from setuptools import setup

# This file is mainly for compatibility
# The actual packaging is handled by Poetry via pyproject.toml
if __name__ == "__main__":
    setup()
