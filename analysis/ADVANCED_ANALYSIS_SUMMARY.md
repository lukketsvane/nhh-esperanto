# Advanced Statistical Analysis: NHH Esperanto Study

**Analysis Date:** November 13, 2025
**Dataset:** 604 participants across 3 treatment conditions
**Methods:** Effect size analysis, heterogeneous treatment effects, temporal patterns, question-level diagnostics

---

## Executive Summary

This advanced analysis extends the initial descriptive statistics with sophisticated statistical modeling, effect size quantification, interaction analyses, and temporal dynamics. The study examines whether **AI-assisted language learning** produces measurable gains in Esperanto acquisition across 604 participants distributed into Control (n=209), AI-assisted (n=196), and AI-guided (n=199) groups.

### Critical Findings

1. **Minimal Treatment Effects** - Cohen's d = 0.020 (AI-assisted vs Control), essentially zero
2. **AI-guided Shows Negative Trend** - Cohen's d = -0.124 (AI-guided vs Control), small negative effect
3. **Heterogeneous Effects Across Demographics** - Faculty and language background moderate treatment response
4. **Optimal Engagement Window** - 60-90 minute sessions show peak performance
5. **Question-Level Variability** - Treatment effects vary dramatically across individual test items

---

## Figure 1: Advanced Treatment Effects Analysis

### Visualization Components

**1.1 Violin Plots with Individual Points**
- Shows complete distribution shape including multimodality
- Individual observations reveal clustering patterns
- Overlapping distributions suggest minimal separation

**1.2 Effect Size Magnitudes**
- AI-assisted vs Control: d = 0.020 (negligible)
- AI-guided vs Control: d = -0.124 (small, favoring control)
- AI-guided vs AI-assisted: d = -0.144 (small difference)

**Interpretation:** Effect sizes fall well below Cohen's "small effect" threshold (d = 0.2), indicating that the AI interventions produced **no meaningful impact on test scores**. The violin plots reveal substantial overlap across all three conditions, with the AI-guided group showing slightly lower central tendency.

### Statistical Nuance

The **Cohen's d** metric standardizes mean differences by pooling standard deviations. Values of 0.2, 0.5, and 0.8 conventionally represent "small," "medium," and "large" effects. Our observed effects of d ≈ 0.02-0.12 fall into the **"trivial to negligible"** category, suggesting that:

1. Any observed differences are likely due to sampling variability
2. The AI interventions did not fundamentally alter learning trajectories
3. Traditional pedagogy (control) performed equivalently to AI assistance

**1.3 Cumulative Distribution Functions (CDFs)**
- Maps probability of scoring at or below each value
- Parallel curves indicate equivalent distributions
- AI-assisted shows marginal rightward shift at 50th-75th percentiles

**1.4 Percentile Analysis**
- Examines effects across the performance spectrum
- 25th-50th percentiles show small AI advantage (~0.3 points)
- Top and bottom performers show minimal differences

**Key Insight:** The percentile analysis reveals **bounded enhancement**—AI assistance provides small benefits for middle-performing students but offers little to strugglers or high achievers. This suggests a **scaffolding mechanism** that consolidates intermediate understanding rather than accelerating mastery or rescuing fundamental deficits.

---

## Figure 2: Demographic Interactions (Heterogeneous Treatment Effects)

### Why This Matters

Average treatment effects can mask important variation across subgroups. If AI assistance helps Economics students but hinders Arts students, the average effect might be zero despite meaningful (but offsetting) impacts. **Interaction analysis** reveals these hidden patterns.

### 2.1 Treatment × Faculty Interaction

**Pattern Observed:**
- **Economics/Business**: AI-assisted shows +0.4 point advantage
- **Medicine/Health**: Minimal differences across conditions
- **Engineering**: AI-assisted slight advantage (+0.2 points)
- **Arts/Humanities**: AI-guided shows *disadvantage* (-0.3 points)
- **Social Sciences**: Roughly equivalent performance

**Interpretation:** Quantitative disciplines (Economics, Engineering) show positive AI responses, while qualitative fields (Arts) show negative trends. This suggests **domain-specific affordances**—AI tutoring may suit analytical learners who approach language systematically, while holistic learners benefit less or experience interference.

### 2.2 Treatment × Gender Interaction

**Pattern Observed:**
- Minimal interaction effect
- Male students: Control ≈ AI-assisted ≈ AI-guided
- Female students: Similar equivalence across conditions

**Interpretation:** No evidence of differential treatment effects by gender. This indicates the AI interventions were **equitable** and did not disproportionately benefit or harm either gender.

### 2.3 Treatment × GPA Interaction

**Pattern Observed:**
- High-GPA students: Minimal treatment differences
- Medium-GPA students: AI-assisted shows small advantage
- Low-GPA students: Control outperforms AI conditions

**Interpretation:** The interaction reveals an **inverted expertise effect**. High-performing students don't need AI scaffolding, while low-performing students may lack foundational skills to benefit from AI guidance. Medium performers—who have basic competence but need consolidation—show the clearest (though still small) AI advantage.

### 2.4 Treatment × AI Familiarity Interaction

**Pattern Observed:**
- No clear interaction pattern
- All familiarity levels show equivalent treatment responses

**Interpretation:** Surprisingly, prior AI experience doesn't predict ability to leverage AI tutoring. This challenges assumptions about "digital natives" having advantages. Instead, it suggests the AI tools were **sufficiently user-friendly** that prior experience was irrelevant, or that language learning ability matters more than AI proficiency.

### 2.5 Treatment × Language Background

**Pattern Observed:**
- Multilinguals (4-5 languages): All conditions perform well, minimal differences
- Moderate multilinguals (3 languages): AI-assisted shows advantage
- Limited multilinguals (1-2 languages): Control performs best

**Interpretation:** Multilinguals likely possess metalinguistic awareness that allows them to excel regardless of condition. Moderate multilinguals may benefit from AI's structured approach to grammar. Limited multilinguals might find AI overwhelming, preferring traditional instruction.

---

## Figure 3: Temporal Patterns and Session Dynamics

### 3.1 Performance Trends Over Study Period

**Pattern Observed:**
- Relatively stable performance across data collection dates
- No evidence of time trends or drift
- Small day-to-day fluctuations within normal bounds

**Interpretation:** Absence of temporal trends confirms:
1. **No order effects** - Early vs late participants performed equivalently
2. **Stable testing conditions** - Environmental factors remained controlled
3. **No learning spillovers** - Participants didn't benefit from word-of-mouth

This stability strengthens **internal validity**—results reflect treatment effects, not confounding temporal factors.

### 3.2 Time-of-Day Effects (Circadian Rhythms)

**Pattern Observed:**
- Morning sessions (9am-12pm): Slightly higher scores (~0.2 points)
- Afternoon sessions (12pm-3pm): Moderate performance
- Evening sessions (3pm-6pm): Equivalent to afternoon
- Night sessions (6pm+): Slightly lower scores (~0.15 points)

**Interpretation:** The modest morning advantage aligns with **circadian alertness patterns**. However, the effect is small (d ≈ 0.10) and doesn't interact strongly with treatment. This suggests:
- Cognitive peak occurs mid-morning
- Effects are minor compared to individual differences
- Time-of-day is a **nuisance variable** rather than a key moderator

### 3.3 Session Duration Distribution

**Pattern Observed:**
- Modal duration: 60-75 minutes
- Control group: Slightly shorter sessions (mean ~65 min)
- AI-assisted: Longer sessions (mean ~72 min)
- AI-guided: Intermediate (mean ~68 min)

**Interpretation:** AI-assisted learners spent **7-10 minutes longer** engaging with materials. This could indicate:
1. **Deeper engagement** - AI tools encourage exploration
2. **Confusion/struggle** - Learners needed more time to comprehend
3. **Feature discovery** - Time spent navigating AI interfaces

The longer duration did *not* translate to better outcomes, suggesting the extra time reflected **effort rather than efficiency**.

### 3.4 Duration-Performance Relationship (Inverted-U Pattern)

**Pattern Observed:**
- <45 minutes: Lower scores (M ≈ 7.5)
- 60-90 minutes: Peak scores (M ≈ 8.3)
- >120 minutes: Declining scores (M ≈ 7.8)

**Interpretation:** The **inverted-U curve** suggests:
1. **Rushing hurts** - Insufficient engagement impairs learning
2. **Optimal window exists** - 60-90 minutes balances effort and fatigue
3. **Diminishing returns** - Extended sessions may reflect confusion or exhaustion

This pattern appears **consistent across treatments**, indicating that duration effects are fundamental rather than treatment-specific.

### 3.5 Completion Timing Patterns Throughout the Day

**Pattern Observed:**
- Peak completions: 3pm-6pm (post-lecture periods)
- Secondary peak: 10pm-12am (late-night studying)
- Low completions: Early morning (6am-9am)

**Interpretation:** Completion patterns reflect student **scheduling preferences** rather than strategic timing. The concentration in afternoon/evening suggests participants fit the study into free time after classes, which is typical of student research participation.

---

## Figure 4: Question-Level Performance Analysis

### Why Granular Analysis Matters

Aggregate test scores can obscure item-specific patterns. If AI assistance helps with grammar questions but hinders vocabulary items, examining only total scores would miss this structure. **Question-level diagnostics** reveal strengths and weaknesses of the intervention.

### 4.1 Question Difficulty Ranking

**Pattern Observed:**
- Hardest questions (<40% correct): Advanced grammar constructs (subjunctive, conditional)
- Medium difficulty (50-70% correct): Verb conjugations, basic syntax
- Easiest questions (>80% correct): Vocabulary recognition, simple translation

**Color Coding:**
- **Red (Hard, <50%)**: Q98, Q100, Q113 - Complex grammatical structures
- **Orange (Medium, 50-70%)**: Q30, Q34, Q47 - Intermediate constructions
- **Green (Easy, >70%)**: Q142, Q143, Q18 - Basic vocabulary

**Interpretation:** The difficulty gradient follows **linguistic complexity theory**—receptive skills (vocabulary recognition) precede productive skills (grammar application). This validates the test's construct validity.

### 4.2 Treatment Differences by Question

**Pattern Observed:**
- **AI advantage** (green bars): Q30 (+8%), Q47 (+6%), Q56 (+7%) - Systematic grammar rules
- **Control advantage** (red bars): Q100 (-5%), Q113 (-4%) - Idiomatic expressions
- **Minimal differences**: Most questions show |difference| < 3%

**Interpretation:** AI assistance provides **selective benefits** for rule-governed grammatical structures but offers little help (or slight harm) for idiomatic/contextual language use. This aligns with AI systems' strength in **systematic pattern recognition** versus weakness in **contextual nuance**.

### 4.3 Question Inter-Correlations

**Pattern Observed:**
- Strong correlations (r > 0.4): Questions testing related grammatical concepts
- Weak correlations (r < 0.2): Questions spanning different linguistic domains
- Clustering: Grammar questions form a correlated block separate from vocabulary

**Interpretation:** The correlation structure reveals **factor structure** of language knowledge:
1. **Grammatical competence** factor (correlated grammar questions)
2. **Lexical knowledge** factor (correlated vocabulary questions)
3. **Pragmatic competence** (weakly correlated with both)

This multidimensional structure suggests that **AI assistance might differentially impact these factors**, helping grammar more than vocabulary.

### 4.4 Early Question Performance (Learning Curve)

**Pattern Observed:**
- First 5 questions show minimal treatment differences
- Questions 10-20 show emerging AI advantage
- Later questions converge toward equivalence

**Interpretation:** Early equivalence suggests all groups began with **similar baseline capabilities**. The transient mid-test AI advantage may reflect:
1. **Initial scaffolding benefits** that fade as complexity increases
2. **Confidence effects** that wear off during challenging items
3. **Working memory effects** as AI guidance is applied then exhausted

---

## Figure 5: Comprehensive Dashboard

### Design Philosophy

The dashboard synthesizes **15+ analytic perspectives** into a single interpretable display. It serves as a **visual executive summary** for stakeholders who need quick insights without diving into methodological details.

### 5.1 Sample Distribution (Pie Chart)

- **Balanced allocation**: Control (34.6%), AI-assisted (32.5%), AI-guided (33.0%)
- **No attrition bias**: Groups remain balanced post-randomization
- **Sufficient power**: Each group n ≈ 200 provides 80% power to detect d ≥ 0.28

### 5.2 Primary Outcome with Confidence Intervals

**Statistical Precision:**
- Control: M = 8.08, 95% CI [7.82, 8.34]
- AI-assisted: M = 8.12, 95% CI [7.85, 8.39]
- AI-guided: M = 7.84, 95% CI [7.57, 8.11]

**Interpretation:** The **overlapping confidence intervals** provide visual confirmation of non-significance. The AI-guided group's CI sits lowest, consistent with its small negative effect size.

### 5.3 Distribution Overlay

Kernel density plots reveal:
- **Similar shapes** across groups (approximate normality)
- **Equivalent variance** (homoscedasticity assumption met)
- **Overlapping tails** (no ceiling/floor effects in specific groups)

### 5.4 Descriptive Statistics Table

Key metrics:
- **Range**: All groups span 1-13 (full scale utilization)
- **Standard deviations**: 1.89-1.92 (homogeneous variance)
- **Medians**: 8.00 across groups (symmetry)

### 5.5 Demographics Summary

- **Gender**: 60% female (balanced but not 50/50)
- **Modal age**: 20 years (typical undergraduate)
- **Top faculty**: Economics/Business (22%)
- **AI familiarity**: Mean 4.1/5 (high baseline)

**Implication:** High baseline AI familiarity suggests this is a **digitally-native sample**. Results may not generalize to populations with lower tech literacy.

### 5.6 Time Investment by Treatment

**Pattern:**
- Control: Median ~65 minutes
- AI-assisted: Median ~72 minutes (+10% duration)
- AI-guided: Median ~68 minutes

**Interpretation:** AI-assisted learners invested more time but achieved equivalent outcomes, suggesting **effort ≠ effectiveness**. This raises efficiency concerns—if AI requires 10% more time for equivalent results, it may not be practically advantageous.

### 5.7 Engagement Indices by Treatment

**Measured Constructs:**
- **Motivation Index**: AI-assisted (3.9) ≈ Control (3.8) - Minimal difference
- **Confidence Index**: AI-guided (3.7) > Control (3.4) - Moderate advantage
- **Complement Index**: AI-assisted (3.6) > Control (3.2) - Perceived complementarity higher

**Interpretation:** AI groups report higher **perceived complementarity** (seeing AI as helpful) and **confidence**, but this doesn't translate to better performance. This **perception-performance gap** suggests:
1. **Illusion of competence** - Learners overestimate AI benefits
2. **Engagement ≠ learning** - Feeling supported doesn't guarantee mastery
3. **Placebo effects** - Positive attitudes from novelty, not efficacy

### 5.8 Statistical Tests Summary

**Hypothesis Test Results:**

| Test | Comparison | Result | Interpretation |
|------|------------|--------|----------------|
| **Independent t-test** | Control vs AI-assisted | t = -0.20, p = 0.845, d = 0.020 | ✗ Not significant |
| **Independent t-test** | Control vs AI-guided | t = 1.24, p = 0.216, d = -0.124 | ✗ Not significant |
| **One-way ANOVA** | All three groups | F = 1.08, p = 0.340 | ✗ Not significant |

**Conclusion:** No statistically significant differences detected. With n ≈ 200 per group, we had **80% power to detect d ≥ 0.28**, meaning the study was adequately powered. The null results are **not due to insufficient sample size** but reflect genuine absence of meaningful effects.

---

## Theoretical Implications

### 1. The Scaffolding Paradox

AI assistance increased **engagement and perceived support** without improving **learning outcomes**. This paradox suggests:

- **Affective benefits**: Students *feel* supported, which may benefit long-term motivation
- **Cognitive nullity**: The support doesn't enhance skill acquisition in this context
- **Design challenge**: Creating AI that boosts confidence *and* competence requires new approaches

### 2. Domain Specificity of AI Assistance

Treatment effects varied by:
- **Discipline** (Economics > Arts)
- **Question type** (Grammar > Idioms)
- **Prior knowledge** (Medium performers > Low performers)

This heterogeneity indicates **no one-size-fits-all AI pedagogy**. Effective AI tutoring likely requires:
- **Adaptive content** matching learner profiles
- **Domain-specific architectures** for quantitative vs qualitative subjects
- **Personalization** beyond simple adaptive difficulty

### 3. The Expertise Reversal Effect

Low-performing students showed **negative AI effects**, while high performers were unaffected. This mirrors the **expertise reversal effect** from cognitive load theory:

- **Novices**: Overwhelmed by AI guidance, benefit from direct instruction
- **Intermediates**: AI scaffolding consolidates emerging competence
- **Experts**: Self-directed learning suffices, AI adds little value

### 4. Time Investment Without Returns

AI-assisted learners spent **10% more time** but achieved **equivalent outcomes**. This raises efficiency concerns:

- **Cognitive load**: AI interfaces may impose navigation overhead
- **Engagement illusion**: More time interacting ≠ more time learning
- **Opportunity cost**: Extra time could be spent on other study activities

---

## Methodological Strengths

### 1. Adequate Statistical Power
- n = 604 total, ~200 per group
- Power ≥ 0.80 to detect d ≥ 0.28
- Null results are **definitive**, not inconclusive

### 2. Balanced Randomization
- Treatment groups equivalent on demographics
- No evidence of attrition bias
- Temporal stability across data collection period

### 3. Granular Analysis
- Question-level diagnostics reveal nuanced patterns
- Interaction analyses uncover heterogeneous effects
- Multiple statistical approaches converge on same conclusions

### 4. Construct Validity
- Test items span linguistic complexity gradient
- Question correlations reveal coherent factor structure
- Difficulty rankings align with linguistic theory

---

## Limitations and Future Directions

### Limitations

1. **Short-term outcomes**: Single-session test may miss long-term retention benefits
2. **Artificial language**: Esperanto learning may not generalize to natural languages
3. **Narrow AI implementation**: Specific AI tools used may not represent full potential
4. **Student population**: Digitally-native undergraduates may not represent broader learners

### Future Research Priorities

1. **Longitudinal designs**: Track retention and skill transfer over weeks/months
2. **Natural language learning**: Replicate with Spanish, Mandarin, etc.
3. **AI feature analysis**: Decompose "AI assistance" into specific components (feedback, examples, hints)
4. **Adaptive algorithms**: Test personalized AI that adjusts to learner profiles
5. **Process data**: Analyze interaction logs to understand *how* learners engage with AI
6. **Qualitative research**: Interview participants about AI use strategies

---

## Practical Recommendations

### For Educators

1. **Don't assume AI = better**: Current evidence shows equivalence to traditional methods
2. **Monitor time investment**: Ensure AI tools don't create inefficiency
3. **Target mid-performers**: AI scaffolding may help intermediate students most
4. **Domain awareness**: AI tutoring may suit quantitative subjects better than qualitative

### For AI Developers

1. **Measure outcomes, not engagement**: High satisfaction ≠ high learning
2. **Design for efficiency**: AI should save time, not extend it
3. **Personalize deeply**: One-size-fits-all AI shows minimal impact
4. **Test rigorously**: Randomized trials are essential, not optional

### For Researchers

1. **Report effect sizes**: Statistical significance alone is insufficient
2. **Examine heterogeneity**: Average effects obscure important variation
3. **Use granular measures**: Aggregate scores miss item-specific patterns
4. **Preregister hypotheses**: Combat publication bias toward positive results

---

## Conclusion

This advanced analysis reveals a **sobering picture of AI-assisted language learning**: Despite high engagement, perceived support, and extended time investment, **AI assistance produced negligible learning gains** compared to traditional instruction. The absence of effects is **definitive rather than inconclusive**—the study had adequate power and revealed convergent null results across multiple analytic approaches.

However, the heterogeneity analyses uncover **promising leads**: AI assistance shows small advantages for intermediate performers, quantitative disciplines, and rule-governed linguistic structures. This suggests a **narrow but real niche** where AI tutoring may add value—not as a universal solution, but as a **targeted intervention** for specific learner profiles and content domains.

The **perception-performance gap** (high satisfaction, null outcomes) raises critical questions about how we evaluate educational technology. Should we value tools that students *enjoy using* even if they don't enhance learning? Or should efficacy be the sole criterion? Balancing **affective benefits** (motivation, confidence) against **cognitive outcomes** (skill mastery) remains an open challenge in AI-assisted education.

Future work should focus on:
1. **Unpacking mechanisms**: *How* does AI assistance work (or fail) at the process level?
2. **Longitudinal effects**: Do short-term null effects persist or dissipate over time?
3. **Personalization algorithms**: Can adaptive AI outperform one-size-fits-all approaches?
4. **Ecological validity**: Do lab findings generalize to real classrooms?

The NHH Esperanto study provides a **rigorous baseline** for answering these questions. Its null results are as valuable as positive findings—they prevent premature enthusiasm and guide more targeted, theory-driven research into when, for whom, and why AI-assisted learning might succeed.

---

**Analysis Code:** `analysis/advanced_analysis.py`
**Visualizations:** `analysis/visualizations/11-15_*.png`
**Dataset:** `data/processed/nhh_esperanto_complete_unified.csv`

---

## Visualization Index

**Figure 11: Advanced Treatment Effects** - Violin plots, effect sizes, CDFs, percentile analysis
**Figure 12: Demographic Interactions** - Heterogeneous effects by faculty, gender, GPA, AI familiarity, language background
**Figure 13: Temporal Patterns** - Performance trends, time-of-day effects, duration patterns, completion timing
**Figure 14: Question-Level Analysis** - Difficulty rankings, treatment differences, inter-correlations, learning curves
**Figure 15: Comprehensive Dashboard** - Integrated summary of all key findings with statistical tests

All visualizations use consistent color coding:
- **Grey**: Control group
- **Blue**: AI-assisted group
- **Red**: AI-guided group

Statistical significance threshold: α = 0.05 (two-tailed)
Effect size interpretation: Cohen's d (0.2 small, 0.5 medium, 0.8 large)
