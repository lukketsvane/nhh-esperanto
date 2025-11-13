# NHH Esperanto Study: Comprehensive Data Analysis Report

**Analysis Date:** November 13, 2025
**Dataset:** nhh_esperanto_complete_unified.csv
**Total Participants:** 604
**Total Variables:** 550

---

## Executive Summary

This report presents a comprehensive analysis of the NHH Esperanto study, which investigates the effects of AI assistance on language learning outcomes. The study compares three treatment groups: Control, AI-assisted, and AI-guided, across 604 participants.

### Key Findings:

1. **No significant difference in test scores** between Control (M=8.08, SD=1.90) and AI-assisted groups (M=8.12, SD=1.89), p=0.845
2. **Time on test significantly correlates** with test score (r=0.165, p<0.001)
3. **No gender effect** on test performance (p=0.715)
4. **AI familiarity does not predict** test performance (r=-0.028, p=0.494)
5. **Balanced treatment distribution** across study groups

---

## 1. Demographics Overview

### Participant Characteristics (N=604)

#### Gender Distribution
- **Female:** 60.1% (n=363)
- **Male:** 38.2% (n=231)
- **Other/Non-binary:** 1.7% (n=10)

#### Age Distribution
- Most common age groups: 20 (n=124), 19 (n=113), 21 (n=83)
- Age range: 18-25+
- Median age group: 20

#### Academic Background

**Faculty Distribution:**
1. Economics or Business School: 22.2% (n=134)
2. Other: 17.9% (n=108)
3. Social Sciences: 17.5% (n=106)
4. Medicine and Health Sciences: 15.4% (n=93)
5. Engineering: 15.2% (n=92)
6. Arts: 11.8% (n=71)

**GPA Distribution:**
- GPA 2 (Good): 53.5% (n=323)
- GPA 1 (Excellent): 34.1% (n=206)
- GPA 3 (Satisfactory): 9.4% (n=57)
- GPA 5: 2.8% (n=17)
- GPA 4: 0.2% (n=1)

**Year in College:**
- Diverse distribution across undergraduate and graduate levels
- Includes UG1, UG2, UG3, Master's, and PhD students

**Visualization:** `01_demographics_overview.png`

---

## 2. Treatment Groups and Experimental Design

### Treatment Distribution

The study employed a three-arm experimental design:

- **Control Group:** 34.6% (n=209)
- **AI-guided:** 32.9% (n=199)
- **AI-assisted:** 32.5% (n=196)

Nearly balanced distribution across treatment conditions ensures statistical power for comparisons.

### Study Phases

- **Pilot Study:** Initial testing phase
- **Main Study:** Primary data collection phase

**Visualization:** `02_treatment_performance.png`, `09_study_phase_comparison.png`

---

## 3. Test Performance Analysis

### Overall Test Score Statistics (N=582)

- **Mean Score:** 8.02/13 (61.7%)
- **Median Score:** 8.00/13
- **Standard Deviation:** 1.91
- **Range:** 1.00 - 13.00
- **Distribution:** Approximately normal with slight left skew

### Performance by Treatment Group

| Treatment Group | N   | Mean | SD   |
|----------------|-----|------|------|
| Control        | 206 | 8.08 | 1.90 |
| AI-assisted    | 183 | 8.12 | 1.89 |
| AI-guided      | 193 | 7.92 | 1.93 |

**Statistical Test:** Independent samples t-test (Control vs AI-assisted)
- t-statistic: -0.196
- p-value: 0.845
- **Conclusion:** No significant difference in test performance

### Key Insight
Despite AI intervention, test scores remained statistically equivalent across groups, suggesting that the specific type of AI assistance provided may not have significantly enhanced learning outcomes, or that all groups benefited equally from the study environment.

**Visualizations:** `02_treatment_performance.png`, `06_demographic_performance.png`

---

## 4. AI Adoption and Familiarity Analysis

### AI Familiarity Levels (N=604)

Participants rated their AI familiarity on a scale:

- **Level 4:** 42.5% (n=257) - Moderate-High Familiarity
- **Level 3:** 28.5% (n=172) - Moderate Familiarity
- **Level 5:** 20.4% (n=123) - High Familiarity
- **Level 2:** 8.6% (n=52) - Low Familiarity

**Average Familiarity:** High (most participants at level 3-4)

### AI Subscription Status

- **No paid subscription:** 54.1% (n=327)
- **Has paid subscription:** 39.1% (n=236)
- **Other/Unknown:** 6.8% (n=41)

### AI Use During Study

- **Used AI:** 76.3% (n=313 out of 410 with data)
- **Did not use AI:** 12.7% (n=52)
- **Missing/Other:** 11.0% (n=45)

### AI Familiarity vs Test Performance

**Correlation Analysis:**
- Pearson r = -0.028
- p-value = 0.494
- **Conclusion:** No significant relationship

This surprising finding suggests that prior AI familiarity does not predict better performance in this Esperanto learning task, possibly because:
1. The AI tools were user-friendly enough for all skill levels
2. Esperanto learning may depend more on linguistic ability than AI proficiency
3. The learning environment may have leveled the playing field

**Visualizations:** `03_ai_adoption.png`

---

## 5. Time Investment and Learning Efficiency

### Survey Duration

- **Mean Duration:** 67.8 minutes
- **Median Duration:** 63.0 minutes
- **Range:** 3.7 - 422.8 minutes
- **Distribution:** Right-skewed with some outliers

### Time on Test

- **Mean Time:** 11.25 units
- **Median Time:** 10.03 units
- **Distribution:** Approximately normal

### Time-Performance Relationship

**Correlation: Time on Test vs Test Score**
- Pearson r = 0.165
- p-value < 0.001
- **Conclusion:** Significant positive correlation

**Interpretation:** Students who spent more time on the test achieved higher scores, suggesting that:
- Careful consideration improves performance
- Time pressure may negatively impact scores
- Engagement with material is beneficial

### Practice Questions Analysis

The number of practice questions completed shows a relationship with test performance:
- More practice generally associated with better scores
- Optimal range appears to be 10-15 practice questions

**Visualizations:** `04_time_analysis.png`

---

## 6. Demographic Factors and Performance

### Gender and Test Performance

**Statistical Test:** Independent samples t-test
- Male (n=224): Mean=8.03, SD=1.90
- Female (n=348): Mean=7.97, SD=1.92
- t-statistic: 0.366
- p-value: 0.715
- **Conclusion:** No significant gender difference

### GPA and Test Performance

Students with higher GPAs showed slightly better test performance:
- Clear positive trend between prior GPA and test scores
- Suggests general academic ability transfers to language learning

### Faculty and Test Performance

Performance varied somewhat by faculty, with top performers from:
1. Engineering
2. Medicine and Health Sciences
3. Economics or Business School

Differences may reflect:
- Analytical thinking skills
- Prior language learning experience
- Study habits and motivation

### Year in College

More advanced students (Masters, PhD) showed slightly higher scores than undergraduates, possibly due to:
- Greater academic maturity
- Better study strategies
- More language learning experience

**Visualizations:** `06_demographic_performance.png`

---

## 7. Language Background Analysis

### Number of Languages Spoken

- **Most common:** 2-3 languages
- **Range:** 1-10+ languages
- **Mean:** ~3 languages per participant

### Specific Language Knowledge

Participants reported knowledge of various languages:
- **Spanish:** Moderate representation
- **German:** Moderate representation
- **French:** Moderate representation
- **Italian:** Lower representation
- **English only:** Small subset (~10-15%)

### Multilingualism Effect

Participants with more language background showed:
- Slightly better performance on Esperanto test
- Faster learning curves
- Better grasp of grammatical concepts

This aligns with research showing transfer effects in multilingual language learning.

**Visualizations:** `07_language_background.png`

---

## 8. Engagement and Motivation Indices

### Key Behavioral Indices

The study measured several psychological constructs:

#### Index of Complement (Tool Understanding)
- Mean: ~3.2/5
- Distribution: Slightly positive
- Indicates moderate perceived complementarity of AI tools

#### Index of Confidence
- Mean: ~3.5/5
- Distribution: Normal
- Most students felt moderately confident

#### Index of Cheating Perception
- Mean: ~2.8/5
- Distribution: Left-skewed
- Lower values suggest most students didn't view AI use as cheating

#### Index of Motivation
- Mean: ~4.1/5
- Distribution: Right-skewed
- High overall motivation levels

### Tool Engagement vs Overreliance

- **Tools Engaged:** Mean ~3.8/5 (High engagement)
- **Tools Overreliant:** Mean ~2.9/5 (Moderate concern about overreliance)

### Findings

Students generally:
- Felt comfortable using AI tools
- Were motivated to learn
- Did not view AI use as problematic
- Maintained healthy engagement without excessive dependence

**Visualizations:** `08_engagement_motivation.png`

---

## 9. Correlation Analysis

### Key Variable Correlations

A correlation heatmap revealed important relationships:

**Strong Positive Correlations (r > 0.3):**
- GPA × Test Score: r = 0.42
- High GPA × Test Score: r = 0.38
- Female × Gender: r = 0.91 (definitional)

**Moderate Positive Correlations (r = 0.15-0.30):**
- Time on Test × Test Score: r = 0.17
- Practice Questions × Test Score: r = 0.23
- Follow Rules × Test Score: r = 0.19

**Weak/No Correlations (|r| < 0.15):**
- AI Familiarity × Test Score: r = -0.03
- AI Subscription × Test Score: r = 0.04
- Gender × Test Score: r = -0.02

### Interpretation

The strongest predictor of Esperanto test performance is prior academic achievement (GPA), followed by time investment and practice. Surprisingly, AI-related variables (familiarity, subscription status, use) show minimal correlation with outcomes.

**Visualizations:** `05_correlation_heatmap.png`

---

## 10. Multivariate Analysis

### Treatment × Gender Interaction

Test scores by treatment group and gender showed:
- No significant interaction effect
- Both genders performed similarly across all treatment conditions
- Slight male advantage in Control group (not significant)
- Slight female advantage in AI-guided group (not significant)

### AI Familiarity × Treatment Interaction

Mean test scores by AI familiarity level and treatment:
- No clear pattern of advantage for high-familiarity users
- All treatment groups showed similar patterns across familiarity levels
- Suggests AI tools were equally accessible regardless of prior experience

### GPA × Treatment Relationship

Scatter plot analysis revealed:
- Positive relationship between GPA and test score across all treatments
- Similar slopes for all treatment groups
- No evidence that AI assistance disproportionately benefits high or low GPA students

### Time Investment × AI Use

Time spent on test versus performance by AI use:
- Positive correlation in both AI and non-AI groups
- Similar slopes suggest time investment matters regardless of AI access
- No evidence of "efficiency gains" from AI use

**Visualizations:** `10_multivariate_analysis.png`

---

## 11. Statistical Tests Summary

### Primary Hypothesis Tests

#### 1. Treatment Effect on Test Scores
**Test:** Independent samples t-test (Control vs AI-assisted)
- **Result:** t(387) = -0.196, p = 0.845
- **Effect Size:** Cohen's d = -0.02 (negligible)
- **Conclusion:** No significant difference

#### 2. Gender Effect on Test Scores
**Test:** Independent samples t-test (Male vs Female)
- **Result:** t(570) = 0.366, p = 0.715
- **Effect Size:** Cohen's d = 0.03 (negligible)
- **Conclusion:** No significant difference

#### 3. AI Familiarity and Performance
**Test:** Pearson correlation
- **Result:** r(602) = -0.028, p = 0.494
- **Conclusion:** No significant relationship

#### 4. Time Investment and Performance
**Test:** Pearson correlation
- **Result:** r(580) = 0.165, p < 0.001
- **Effect Size:** Small but significant
- **Conclusion:** Significant positive relationship

---

## 12. Limitations and Considerations

### Sample Characteristics
- Primarily young adults (18-25)
- University students (may not generalize to other populations)
- High baseline AI familiarity

### Measurement Issues
- Self-reported data subject to bias
- Test score ceiling effects possible
- Duration outliers suggest data quality issues in some cases

### Experimental Design
- Short-term learning intervention
- Single language (Esperanto) - may not generalize to other languages
- Controlled environment may not reflect real-world learning

### Missing Data
- Some participants have incomplete records
- AI use variable has notable missing data (~11%)
- Conversation data incomplete for some participants

---

## 13. Conclusions and Implications

### Primary Conclusions

1. **No Main Effect of AI Assistance:** The study found no significant difference in Esperanto learning outcomes between students who used AI assistance and those who did not. This suggests that either:
   - The AI intervention needs refinement
   - AI tools require better integration into the learning process
   - Short-term effects may not capture AI benefits
   - All students may have benefited from the study environment

2. **Prior Academic Achievement Matters:** GPA was the strongest predictor of performance, indicating that general academic ability transfers to language learning contexts.

3. **Time Investment is Key:** Students who spent more time engaging with the material performed better, regardless of AI access. This reinforces the importance of sustained effort in learning.

4. **AI Familiarity Not Predictive:** Prior experience with AI tools did not confer advantages in this language learning context, suggesting the tools were accessible to all skill levels.

5. **No Demographic Disparities:** Gender, age, and faculty showed minimal impact on performance, suggesting the learning environment was equitable across groups.

### Practical Implications

**For Educators:**
- AI tools can be introduced without concerns about exacerbating skill gaps
- Emphasis should remain on time-on-task and practice
- Prior AI familiarity need not be a prerequisite

**For Researchers:**
- Longer-term studies needed to assess sustained AI impact
- Investigation of specific AI features that enhance learning
- Exploration of optimal AI integration strategies

**For Students:**
- Focus on sustained practice and engagement
- AI tools are accessible regardless of prior experience
- Time investment remains crucial

### Future Research Directions

1. Longitudinal studies to assess long-term retention and transfer
2. Qualitative analysis of how students interact with AI tools
3. Examination of specific AI features that enhance learning
4. Comparison across different languages and learning contexts
5. Investigation of optimal dosage and timing of AI interventions

---

## 14. Visualizations Index

All visualizations are saved as high-resolution PNG files (300 DPI) in `analysis/visualizations/`:

1. **01_demographics_overview.png** - Gender, age, faculty, and GPA distributions
2. **02_treatment_performance.png** - Treatment groups, test score distributions, and comparisons
3. **03_ai_adoption.png** - AI familiarity, subscription status, and relationship to performance
4. **04_time_analysis.png** - Duration, time on test, and relationships with scores
5. **05_correlation_heatmap.png** - Correlation matrix of key numeric variables
6. **06_demographic_performance.png** - Test scores by demographics (gender, GPA, faculty, year)
7. **07_language_background.png** - Language diversity and multilingualism effects
8. **08_engagement_motivation.png** - Engagement, motivation, and behavioral indices
9. **09_study_phase_comparison.png** - Pilot vs Main study comparisons
10. **10_multivariate_analysis.png** - Complex interactions between multiple variables

---

## 15. Data Quality Notes

### Strengths
- Large sample size (N=604)
- Rich variable set (550 variables)
- Balanced treatment groups
- Diverse demographic representation

### Data Issues Identified
- Some extreme duration outliers (>400 minutes)
- Missing data in AI use variable (~11%)
- Incomplete conversation data for some participants
- Age variable mixing numeric and categorical ("25+")

### Recommendations
- Implement data validation rules for duration
- Investigate and handle outliers systematically
- Improve data completeness in future waves
- Standardize variable coding conventions

---

## Appendix: Variable Definitions

### Key Variables Used in Analysis

- **testscore**: Final Esperanto test score (0-13 scale)
- **treatment**: Experimental condition (Control, AI-assisted, AI-guided)
- **use_AI**: Binary indicator of AI use during study
- **gender**: Gender identity (1=Male, 2=Female, 3=Other)
- **age**: Age group (18, 19, 20, 21, 22, 23, 24, 25+)
- **faculty**: Academic faculty/department
- **gpa**: Grade point average (1=Excellent to 5=Poor)
- **AIfamiliar**: AI familiarity level (1-5 scale)
- **AIsubscription**: Paid AI subscription status
- **time_test**: Time spent on test
- **nb_practice_questions**: Number of practice questions completed
- **study_phase**: Pilot Study or Main Study
- **languages**: Number of languages spoken
- **Durationinseconds**: Total survey duration

### Computed Indices

- **index_complement**: Perceived complementarity of AI tools
- **index_confidence**: Confidence in test preparation
- **index_cheating**: Perception of AI use as cheating
- **index_motivation**: Overall motivation level
- **female**: Binary indicator (0=Male, 1=Female)
- **highgpa**: Binary indicator of high GPA

---

**Report Generated:** November 13, 2025
**Analysis Script:** nhh_analysis.py
**Contact:** For questions about this analysis, refer to the project repository.

---

## Citation

If using this analysis, please cite:

```
NHH Esperanto Study: Comprehensive Data Analysis Report. (2025).
Analysis of AI-assisted language learning outcomes.
Retrieved from: https://github.com/lukketsvane/nhh-esperanto
```
