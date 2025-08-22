# Python PDF Generator

A command-line tool that converts Markdown documents to professionally formatted PDF reports with intelligent code wrapping and syntax highlighting.

## Overview

This tool provides a streamlined workflow for generating PDF reports from Markdown files:
1. **Markdown → HTML**: Converts Markdown to HTML with syntax highlighting
2. **HTML → PDF**: Renders HTML to PDF with custom styling and page layout

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Requirements

- **Python 3.13.3**
- **[markdown](https://github.com/Python-Markdown/markdown) 3.8.2** - Markdown parsing and HTML conversion
- **[xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf) 0.2.17** - HTML to PDF conversion
- **[pygments](https://github.com/pygments/pygments) 2.19.2** - Syntax highlighting for code blocks

These dependencies were selected for their reliability, active maintenance, and strong community support (all of them are well-maintained and have a lot of stars on GitHub).

## Usage

### Basic Usage

```bash
python main.py <input_file>
```

### Generate Both PDF and HTML

```bash
python main.py <input_file> --html
```

### Example

```bash
python main.py inputs/sample_input.md --html
```

This generates:
- `generated/output.pdf` - The final PDF report
- `generated/output.html` - Intermediate HTML file (with `--html` flag)

## Features ✅

- **Complete Markdown support** - Headers, lists, tables, links, blockquotes
- **Intelligent code wrapping** - Automatic line wrapping with visual continuation indicators
- **Syntax highlighting** - Multiple language support via Pygments
- **Responsive design** - Configurable fonts, margins, and page layout

## Limitations ❌

- **Images** - Not currently supported
- **Mathematical expressions** - LaTeX/MathJax not supported
- **Line numbers on code blocks** - Not currently supported
- **Error handling** - Some errors might not be caught
- **Styling** - Style can be improved

## Known Issues ✨

- **Automatic page breaks** - H1 headers always trigger page breaks (not configurable)
- **Limited CSS support** - Some advanced styling may not render correctly
- **First H1 page break** - Workaround found to avoid the first H1 page break (more in `converters/html_template.py`)

## Development Notes ⏱️

**Total development time: ~4 hours**

### Implementation breakdown:
- **Dependencies research** (20 min) - Evaluating libraries for Markdown/PDF conversion
- **Markdown to HTML conversion** (30 min) - Implementing `MarkdownConverter` class
- **HTML to PDF conversion** (30 min) - Creating `PdfConverter` and `HtmlTemplate` classes
- **Code wrapping system** (2h30) - The most complex component:
  - Initial attempts with CSS-based wrapping failed (xhtml2pdf limitations)
  - Developed manual wrapping algorithm using monospace font calculations
  - Implemented `CodeWrapper` class with intelligent line breaking
  - Integrated Pygments for syntax highlighting
- **HTML template** (1h) - Creating `HtmlTemplate` class:
    - Supports code indentation by replacing leading spaces with &nbsp; entities (to avoid PDF layout issues)
- **CLI interface** (5 min) - Adding command-line argument parsing
- **README redaction** (20 min) - Writing a comprehensive README.md file

### Architecture

The project uses a modular design with separate converters:
- `CodeWrapper` - Handles long line wrapping in code blocks
- `MarkdownConverter` - Converts Markdown to HTML with extensions
- `HtmlTemplate` - Generates styled HTML templates
- `PdfConverter` - Renders final PDF output

There is a `generated` folder that contains the generated PDF and HTML files and a `inputs` folder that contains some sample input files.
