# NHH Esperanto Study: Complete Analysis Suite

## Overview

This directory contains comprehensive statistical analyses and visualizations for the NHH Esperanto language learning experiment. The study examines whether AI-assisted instruction improves learning outcomes compared to traditional methods, using 604 participants across three treatment conditions.

## Analysis Reports

### 📊 [ANALYSIS_REPORT.md](ANALYSIS_REPORT.md)
**Primary comprehensive analysis report**
- 15 sections covering all aspects of the study
- Descriptive statistics for demographics, treatment groups, and outcomes
- Correlation analyses and statistical tests
- Detailed interpretations and implications
- **Key Finding:** No significant difference between Control (M=8.08) and AI-assisted (M=8.12) groups, p=0.845

### 🔬 [ADVANCED_ANALYSIS_SUMMARY.md](ADVANCED_ANALYSIS_SUMMARY.md)
**Advanced statistical modeling and effect size analysis**
- Effect size quantification (Cohen's d)
- Heterogeneous treatment effects across demographics
- Temporal patterns and session dynamics
- Question-level performance diagnostics
- Theoretical implications and future directions
- **Key Finding:** Effect sizes near zero (d=0.020), with heterogeneous effects by faculty and prior knowledge

## Analysis Scripts

### `advanced_analysis.py`
Python script generating all 15 visualizations using:
- pandas, numpy for data manipulation
- matplotlib, seaborn for visualization
- scipy for statistical tests
- Effect size calculations, interaction plots, temporal analyses

**To run:**
```bash
python3 analysis/advanced_analysis.py
```

## Visualizations (15 Total)

All visualizations are high-resolution PNG files (300 DPI) with consistent color coding:
- **Grey (#95a5a6)**: Control group
- **Blue (#3498db)**: AI-assisted group
- **Red (#e74c3c)**: AI-guided group

### Basic Descriptive Analysis (1-10)

#### 01_demographics_overview.png
**Four-panel demographic summary**
- Gender distribution (pie chart): 60.1% female, 38.2% male
- Age distribution (bar chart): Peak at ages 19-21
- Faculty distribution (horizontal bar): Economics/Business (22.2%), Other (17.9%)
- GPA distribution (bar chart): Majority at GPA 2 (Good, 53.5%)

#### 02_treatment_performance.png
**Treatment groups and test performance**
- Treatment distribution (bar chart): Balanced design (~33% each)
- Test score distribution (histogram with mean/median lines)
- Box plots: Test scores by treatment group
- Box plots: Test scores by AI use status

#### 03_ai_adoption.png
**AI familiarity and usage patterns**
- AI familiarity levels (bar chart): Most at level 4 (42.5%)
- AI subscription status (pie chart): 54.1% no paid subscription
- Test scores by AI familiarity (box plots)
- Test scores by rule-following behavior

#### 04_time_analysis.png
**Duration and time investment patterns**
- Survey duration distribution (histogram): Mean 67.8 minutes
- Time on test distribution (histogram)
- Time vs score scatter plot (r=0.165, p<0.001)
- Practice questions vs score (error bars showing means and SDs)

#### 05_correlation_heatmap.png
**Correlation matrix of key numeric variables**
- 9 variables: testscore, gpa, AIfamiliar, AIsubscription, followrules, time_test, female, highgpa, nb_practice_questions
- Color-coded correlations from -1 (red) to +1 (blue)
- **Strongest correlation:** GPA × testscore (r=0.42)
- **Weakest correlation:** AI familiarity × testscore (r=-0.03)

#### 06_demographic_performance.png
**Test scores by demographic subgroups**
- Gender comparison (box plots): No significant difference
- GPA levels (box plots): Clear positive trend
- Faculty rankings (horizontal bar): Mean scores with sample sizes
- Year in college (box plots): Slight advantage for advanced students

#### 07_language_background.png
**Multilingual effects on learning**
- Number of languages spoken (bar chart)
- Test scores by language count (box plots)
- Specific language knowledge (bar chart): Spanish, German, French, Italian
- English-only vs multilingual comparison

#### 08_engagement_motivation.png
**Psychological and behavioral indices**
- Six histograms showing distributions of:
  - Index of complement (tool understanding)
  - Index of confidence (test preparation)
  - Index of cheating (perception of AI as cheating)
  - Index of motivation
  - Tools engaged
  - Tools overreliant

#### 09_study_phase_comparison.png
**Pilot vs Main study analysis**
- Phase distribution (pie chart)
- Test scores by phase (box plots)
- Survey duration by phase (box plots)
- Treatment distribution by phase (stacked bar)

#### 10_multivariate_analysis.png
**Complex interactions between variables**
- Treatment × Gender on test scores
- AI familiarity × Treatment interaction
- GPA vs score colored by treatment (scatter)
- Time vs score by AI use (scatter)

### Advanced Statistical Analysis (11-15)

#### 11_advanced_treatment_effects.png
**Sophisticated effect size analysis**
- **Panel 1:** Violin plots with individual observations overlay
- **Panel 2:** Cohen's d effect sizes (horizontal bar chart)
  - AI-assisted vs Control: d=0.020 (negligible)
  - AI-guided vs Control: d=-0.124 (small)
- **Panel 3:** Cumulative distribution functions (CDFs)
- **Panel 4:** Percentile analysis (10th, 25th, 50th, 75th, 90th)

**Key Insight:** Minimal treatment effects across entire distribution, with AI-guided showing slight disadvantage.

#### 12_demographic_interactions.png
**Heterogeneous treatment effects**
- **Panel 1:** Treatment × Faculty (6 faculties, 3 treatment bars each)
  - Economics shows +0.4 point AI advantage
  - Arts shows -0.3 point AI disadvantage
- **Panel 2:** Treatment × Gender (line plot with error bars)
- **Panel 3:** Treatment × GPA (line plot)
  - Medium GPA shows AI advantage
  - Low GPA shows control advantage (expertise reversal)
- **Panel 4:** Treatment × AI Familiarity (line plot)
- **Panel 5:** Treatment × Language Background (grouped bar)
  - Moderate multilinguals (3 languages) benefit from AI
  - Limited multilinguals (1-2) do better in control

**Key Insight:** AI assistance works differently across subgroups—quantitative students and intermediate performers show advantages.

#### 13_temporal_patterns.png
**Session dynamics and timing effects**
- **Panel 1:** Performance over study dates (line plot with error bars)
  - Stable across time (no drift or order effects)
- **Panel 2:** Time-of-day effects (grouped bar)
  - Morning (9am-12pm) shows slight advantage
- **Panel 3:** Duration distribution by treatment (overlaid histograms)
  - AI-assisted sessions ~7 minutes longer
- **Panel 4:** Duration vs performance (scatter with polynomial trend)
  - Inverted-U: Peak at 60-90 minutes
- **Panel 5:** Completion timing throughout day (line plot)
  - Peak completions 3pm-6pm

**Key Insight:** Optimal engagement window is 60-90 minutes; AI-assisted requires more time without better outcomes.

#### 14_question_level_analysis.png
**Item-level diagnostic analysis**
- **Panel 1:** Question difficulty ranking (horizontal bar, color-coded)
  - Red: Hard questions (<50% correct)
  - Orange: Medium (50-70%)
  - Green: Easy (>70%)
- **Panel 2:** Treatment differences by question (horizontal bar)
  - AI advantage on grammar questions (+8%)
  - Control advantage on idioms (-5%)
- **Panel 3:** Question inter-correlations (heatmap, 10×10)
  - Grammar questions cluster together
- **Panel 4:** Early question performance (bar chart)

**Key Insight:** AI helps with systematic grammar but not contextual/idiomatic language use.

#### 15_comprehensive_dashboard.png
**Executive summary integrating all analyses**

**Top Row (4 panels):**
- Sample distribution pie chart (balanced ~33% each)
- Mean scores with 95% CI error bars
- Score distribution overlays (3 histograms)

**Middle Row (2 panels):**
- Descriptive statistics table (N, Mean, Median, SD, Min, Max)
- Demographics summary table

**Third Row (2 panels):**
- Time investment by treatment (box plots)
- Engagement indices by treatment (grouped bar)

**Bottom Row (1 panel):**
- Statistical tests summary table:
  - Independent t-test: Control vs AI-assisted (p=0.845)
  - Independent t-test: Control vs AI-guided (p=0.216)
  - One-way ANOVA: All three groups (p=0.340)
  - All tests: **Not significant**

**Key Insight:** Comprehensive null results across all statistical approaches with adequate power (n~200 per group).

## Key Statistical Results

### Primary Hypotheses

| Hypothesis | Test | Result | Effect Size | Interpretation |
|------------|------|--------|-------------|----------------|
| AI-assisted > Control | t-test | t=-0.196, p=0.845 | d=0.020 | **No effect** |
| AI-guided > Control | t-test | t=1.24, p=0.216 | d=-0.124 | **Small negative** |
| Any treatment difference | ANOVA | F=1.08, p=0.340 | η²=0.004 | **No effect** |

### Secondary Analyses

| Variable | Correlation with Test Score | p-value | Significance |
|----------|----------------------------|---------|--------------|
| Time on test | r=0.165 | <0.001 | ✓ Significant |
| GPA | r=0.42 | <0.001 | ✓ Significant |
| AI familiarity | r=-0.028 | 0.494 | ✗ Not significant |
| Gender | r=-0.02 | 0.715 | ✗ Not significant |

### Sample Characteristics (N=604)

- **Gender:** 60.1% female, 38.2% male, 1.7% other
- **Age:** Modal age 20 (mean ≈ 21)
- **GPA:** 53.5% GPA 2 (Good), 34.1% GPA 1 (Excellent)
- **Faculty:** 22.2% Economics/Business, 17.9% Other, 17.5% Social Sciences
- **AI familiarity:** Mean 3.9/5 (high baseline)
- **AI subscription:** 39.1% have paid subscriptions

### Test Score Summary

| Treatment | N | Mean | SD | Median | Range |
|-----------|---|------|----|----|-------|
| Control | 206 | 8.08 | 1.90 | 8.0 | 1-13 |
| AI-assisted | 183 | 8.12 | 1.89 | 8.0 | 1-13 |
| AI-guided | 193 | 7.84 | 1.92 | 8.0 | 1-13 |
| **Overall** | **582** | **8.02** | **1.91** | **8.0** | **1-13** |

## Practical Implications

### For Educators
1. **AI ≠ automatic improvement** - Current evidence shows equivalence to traditional instruction
2. **Monitor efficiency** - AI-assisted sessions take 10% longer for same outcomes
3. **Target strategically** - Consider AI for intermediate performers and rule-based content
4. **Domain matters** - Quantitative disciplines may benefit more than qualitative

### For AI Developers
1. **Measure learning, not engagement** - High satisfaction doesn't guarantee skill gains
2. **Optimize for efficiency** - AI should save time, not extend it
3. **Personalize deeply** - One-size-fits-all approaches show minimal impact
4. **Test rigorously** - RCTs are essential for validating educational technology

### For Researchers
1. **Report effect sizes** - p-values alone are insufficient
2. **Examine heterogeneity** - Average effects obscure subgroup variation
3. **Use granular measures** - Item-level analysis reveals nuanced patterns
4. **Long-term follow-up** - Single-session tests may miss retention effects

## Limitations

1. **Short-term measurement** - Single test session may not capture long-term retention
2. **Artificial language** - Esperanto may not generalize to natural language learning
3. **Specific AI implementation** - Results reflect particular tools, not AI in general
4. **Student population** - Digitally-native undergraduates may not represent all learners
5. **Single institution** - Norwegian business school sample limits generalizability

## Future Research Directions

1. **Longitudinal designs** - Track learning and retention over weeks/months
2. **Natural languages** - Replicate with Spanish, Mandarin, French, etc.
3. **AI feature decomposition** - Test specific components (feedback, examples, hints)
4. **Adaptive algorithms** - Implement personalization based on learner profiles
5. **Process analysis** - Log interaction data to understand engagement strategies
6. **Qualitative research** - Interview learners about their AI use experiences
7. **Cost-effectiveness** - Compare learning per unit time invested

## Citation

If you use these analyses or visualizations, please cite:

```
NHH Esperanto Study: Comprehensive Data Analysis. (2025).
Advanced statistical analysis of AI-assisted language learning.
GitHub: https://github.com/lukketsvane/nhh-esperanto
```

## File Structure

```
analysis/
├── README.md (this file)
├── ANALYSIS_REPORT.md (primary report, 15 sections)
├── ADVANCED_ANALYSIS_SUMMARY.md (advanced methods, theoretical implications)
├── advanced_analysis.py (Python analysis script)
└── visualizations/
    ├── 01_demographics_overview.png
    ├── 02_treatment_performance.png
    ├── 03_ai_adoption.png
    ├── 04_time_analysis.png
    ├── 05_correlation_heatmap.png
    ├── 06_demographic_performance.png
    ├── 07_language_background.png
    ├── 08_engagement_motivation.png
    ├── 09_study_phase_comparison.png
    ├── 10_multivariate_analysis.png
    ├── 11_advanced_treatment_effects.png
    ├── 12_demographic_interactions.png
    ├── 13_temporal_patterns.png
    ├── 14_question_level_analysis.png
    └── 15_comprehensive_dashboard.png
```

## Contact

For questions about the analysis or requests for additional analyses, please open an issue in the GitHub repository.

---

**Last Updated:** November 13, 2025
**Analysis Version:** 2.0 (Advanced)
**Dataset:** nhh_esperanto_complete_unified.csv (604 participants, 550 variables)
