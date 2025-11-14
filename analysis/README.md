# NHH Esperanto Study - Analysis and Paper

This directory contains the complete analysis and paper for the AI in the Classroom experiment.

## Contents

### Analysis Scripts
- `pap_analysis.py` - Complete Pre-Analysis Plan implementation
- `create_comprehensive_figures.py` - Creates Figures 1-4 (main results and heterogeneity)
- `create_remaining_figures.py` - Creates Figures 5-10 (mechanisms, attrition, statistical confirmation)

### Paper
- `nhh_esperanto_paper.tex` - Complete LaTeX manuscript with all sections

### Figures
All publication-quality figures (300 DPI) are in `figures_paper/`:
- `Fig01_comprehensive_summary.png` - Main results overview
- `Fig02_triple_interaction.png` - Gender × GPA × Treatment effects
- `Fig03_heterogeneity_heatmap.png` - Effect heterogeneity visualization
- `Fig04_practice_substitution.png` - Practice effort and substitution
- `Fig05_mechanisms.png` - Four mechanism dimensions
- `Fig06_confidence.png` - Confidence and calibration analysis
- `Fig07_attrition.png` - Attrition and dependency
- `Fig08_ai_usage.png` - AI usage patterns
- `Fig09_statistical_confirmation.png` - Null result validation
- `Fig10_correlations.png` - Correlation matrix

## Reproducing the Analysis

### Generate Figures
```bash
cd analysis
python create_comprehensive_figures.py  # Creates Fig 1-4
python create_remaining_figures.py      # Creates Fig 5-10
```

### Compile Paper
To compile the PDF paper:

**Option 1: Local LaTeX installation**
```bash
cd analysis
pdflatex nhh_esperanto_paper.tex
pdflatex nhh_esperanto_paper.tex  # Run twice for references
```

**Option 2: Overleaf**
1. Upload `nhh_esperanto_paper.tex` to Overleaf
2. Upload all figures from `figures_paper/` directory
3. Compile in Overleaf

**Option 3: Online LaTeX compiler**
Use any online LaTeX compiler (e.g., papeeria.com, latexbase.com)

## Key Results

### Main Findings
- **No significant average treatment effects**: Test scores similar across Control (8.13), AI-Assisted (8.18), and AI-Guided (7.99)
- **Significant effort substitution**: AI treatments reduced practice questions by 15-18%
- **Suggestive heterogeneity**: Small, non-significant interactions with gender and GPA
- **Null mechanisms**: No strong effects on confidence, motivation, or cheating perceptions

### Sample
- N = 478 students (Control: 160, AI-Assisted: 165, AI-Guided: 153)
- University of Nottingham students
- Learning topic: Esperanto language

## Authors
- Catalina Franco (NHH Norwegian School of Economics)
- Natalie Irmert (Lund University)
- Siri Isaksson (NHH Norwegian School of Economics)

## Date
December 2024
