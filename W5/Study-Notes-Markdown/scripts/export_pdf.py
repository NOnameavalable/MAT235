#!/usr/bin/env python3
"""Export the Week 5 Markdown with readable lists and print-specific layout.

Requires the existing Pandoc and XeLaTeX installation. By default writes to a
temporary output directory; pass --output-dir to choose a delivery directory.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('names', nargs='*', default=['Study-Notes', 'Answers-and-Practice'])
parser.add_argument('--output-dir', type=Path)
args = parser.parse_args()
base = Path(__file__).resolve().parent.parent
out = args.output_dir or Path(tempfile.mkdtemp(prefix='mat235-w5-pdf-'))
out.mkdir(parents=True, exist_ok=True)
pandoc = shutil.which('pandoc') or '/Users/stevenli/opt/anaconda3/bin/pandoc'
engine = shutil.which('xelatex') or '/Library/TeX/texbin/xelatex'
for name in args.names:
    if name not in ['Study-Notes', 'Answers-and-Practice']:
        parser.error('Choose Study-Notes or Answers-and-Practice.')
    common = [pandoc, str(base / (name + '.md')), '--from=gfm+tex_math_dollars',
              '--standalone', '--resource-path=' + str(base),
              '--lua-filter=' + str(base / 'scripts/pdf-layout.lua'),
              '--include-in-header=' + str(base / 'scripts/pdf-layout.tex'),
              '-V', 'papersize=letter', '-V', 'fontsize=11pt',
              '-V', 'geometry:margin=0.7in', '-V', 'colorlinks=true',
              '-V', 'linkcolor=NavyBlue', '-V', 'urlcolor=NavyBlue',
              '-V', 'filecolor=NavyBlue']
    # Keep intermediate LaTeX and logs beside the staged PDFs for QA.
    subprocess.run(common + ['--to=latex', '-o', str(out / (name + '.tex'))],
                   cwd=base, check=True)
    result = subprocess.run(common + ['--pdf-engine=' + engine,
                            '-o', str(out / (name + '.pdf'))],
                            cwd=base, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out / (name + '.log')).write_text(result.stdout + result.stderr)
    if result.returncode:
        raise SystemExit(result.stderr)
    pdf_python = '/Users/stevenli/.codex/venvs/docling-cli/bin/python'
    subprocess.run([pdf_python, str(base / 'scripts/pdf_links.py'),
                    str(out / (name + '.pdf'))], check=True)
    print(out / (name + '.pdf'))
