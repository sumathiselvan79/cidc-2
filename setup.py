"""
Setup configuration for Enhanced PDF Form Processing System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf-form-processor",
    version="1.0.0",
    author="Development Team",
    description="Enhanced PDF form processing with semantic retrieval, domain knowledge, and validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pdf-form-processor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies (none required - uses standard library)
    ],
    extras_require={
        "ml": [
            "scikit-learn>=1.0.0",
            "numpy>=1.20.0",
            "pandas>=1.3.0",
        ],
        "semantic": [
            "sentence-transformers>=2.2.0",
            "torch>=2.0.0",
        ],
        "nlp": [
            "spacy>=3.0.0",
            "nltk>=3.6.0",
        ],
        "transformers": [
            "transformers>=4.0.0",
            "torch>=2.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
        "all": [
            # All optional dependencies
            "scikit-learn>=1.0.0",
            "numpy>=1.20.0",
            "pandas>=1.3.0",
            "sentence-transformers>=2.2.0",
            "torch>=2.0.0",
            "spacy>=3.0.0",
            "nltk>=3.6.0",
            "transformers>=4.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
    },
    include_package_data=True,
    keywords="pdf forms extraction retrieval validation compliance",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pdf-form-processor/issues",
        "Documentation": "https://github.com/yourusername/pdf-form-processor/blob/main/DOCUMENTATION_INDEX.md",
        "Source Code": "https://github.com/yourusername/pdf-form-processor",
    },
)
