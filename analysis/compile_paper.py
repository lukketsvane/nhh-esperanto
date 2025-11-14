#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compile LaTeX paper to PDF using cloud service or local installation
"""

import subprocess
import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def check_latex_installed():
    """Check if pdflatex is available"""
    try:
        result = subprocess.run(['pdflatex', '--version'],
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def compile_with_pdflatex(tex_file):
    """Compile using local pdflatex"""
    print("Compiling with pdflatex...")

    # Run twice for references
    for i in range(2):
        print(f"Pass {i+1}/2...")
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', tex_file],
            capture_output=True,
            text=True,
            cwd=tex_file.parent
        )

        if result.returncode != 0:
            print(f"Error during compilation:")
            print(result.stdout[-1000:])  # Last 1000 chars
            return False

    print(f"✓ PDF created: {tex_file.with_suffix('.pdf')}")
    return True

def try_install_miktex():
    """Try to install MiKTeX on Windows"""
    print("\nLaTeX not found. Attempting to install MiKTeX...")
    print("This requires admin privileges and internet connection.")

    try:
        # Try winget (Windows Package Manager)
        result = subprocess.run(
            ['winget', 'install', '--id', 'MiKTeX.MiKTeX', '--silent'],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            print("OK MiKTeX installed successfully!")
            return True
        else:
            print("Could not install via winget.")
            return False

    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("winget not available.")
        return False

def create_compilation_instructions(tex_file):
    """Create detailed instructions for manual compilation"""
    instructions = f"""
============================================================================
LaTeX Installation Required
============================================================================

Your LaTeX file is ready at:
{tex_file.absolute()}

To compile it to PDF, you have several options:

OPTION 1: Install LaTeX locally (Recommended)
----------------------------------------------
Windows:
  1. Download MiKTeX: https://miktex.org/download
  2. Install with default settings
  3. Run: cd {tex_file.parent.absolute()}
  4. Run: pdflatex nhh_esperanto_paper.tex
  5. Run: pdflatex nhh_esperanto_paper.tex  (twice for references)

OPTION 2: Use Overleaf (Online, Easy)
--------------------------------------
  1. Go to https://www.overleaf.com
  2. Create free account
  3. Click "New Project" → "Upload Project"
  4. Upload nhh_esperanto_paper.tex
  5. Upload the entire figures_paper/ folder
  6. Click "Recompile" - PDF appears on right side
  7. Download PDF

OPTION 3: Use Other Online LaTeX Compilers
-------------------------------------------
  - Papeeria: https://papeeria.com
  - LaTeX Base: https://latexbase.com
  - CoCalc: https://cocalc.com

OPTION 4: Docker (For Advanced Users)
--------------------------------------
docker run --rm -v "{tex_file.parent.absolute()}:/data" thomasweise/docker-texlive pdflatex nhh_esperanto_paper.tex

============================================================================

All figures are already in place at:
{tex_file.parent / 'figures_paper'}

The paper is 40+ pages with 10 high-quality figures showing:
- Main experimental results (null effects)
- Heterogeneity analysis by gender/GPA
- Mechanism analysis (4 dimensions)
- Statistical confirmation (power, equivalence, Bayes factors)

============================================================================
"""

    print(instructions)

    # Save to file
    instructions_file = tex_file.parent / 'COMPILATION_INSTRUCTIONS.txt'
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)

    print(f"\nOK Instructions saved to: {instructions_file}")

def main():
    # Find the tex file
    script_dir = Path(__file__).parent
    tex_file = script_dir / 'nhh_esperanto_paper.tex'

    if not tex_file.exists():
        print(f"Error: {tex_file} not found!")
        sys.exit(1)

    print("="*80)
    print("LaTeX Paper Compilation Script")
    print("="*80)

    # Check if LaTeX is installed
    if check_latex_installed():
        print("OK pdflatex found!")
        success = compile_with_pdflatex(tex_file)

        if success:
            pdf_file = tex_file.with_suffix('.pdf')
            print(f"\n{'='*80}")
            print(f"SUCCESS! PDF created at:")
            print(f"{pdf_file.absolute()}")
            print(f"{'='*80}")
            sys.exit(0)
        else:
            print("\nCompilation failed. See errors above.")
            sys.exit(1)
    else:
        print("X pdflatex not found")

        # Try to install on Windows
        if sys.platform == 'win32':
            if try_install_miktex():
                print("\nPlease restart your terminal and run this script again.")
                sys.exit(0)

        # Provide instructions
        create_compilation_instructions(tex_file)
        print("\nPlease follow the instructions above to compile your paper.")
        sys.exit(1)

if __name__ == '__main__':
    main()
