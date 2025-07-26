#!/usr/bin/env python3
"""
Setup script for MongoDB MCP Server
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mongodb-mcp-server",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Model Context Protocol (MCP) server for MongoDB using FastMCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mongodb-mcp-server",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    py_modules=["mongo_mcp_server"],
    entry_points={
        "console_scripts": [
            "mongodb-mcp-server=mongo_mcp_server:main",
        ],
    },
    keywords="mongodb mcp model-context-protocol fastmcp database",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/mongodb-mcp-server/issues",
        "Source": "https://github.com/yourusername/mongodb-mcp-server",
        "Documentation": "https://github.com/yourusername/mongodb-mcp-server#readme",
    },
) 