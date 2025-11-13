#!/usr/bin/env python3
"""
Advanced Statistical Analysis and Sophisticated Visualizations
NHH Esperanto Study - Treatment Effects, Interactions, and Temporal Patterns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency, pearsonr, spearmanr
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Enhanced plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11

# Color palette for treatment groups
COLORS = {
    'Control': '#95a5a6',
    'AI-assisted': '#3498db',
    'AI-guided': '#e74c3c'
}

print("="*80)
print("ADVANCED ANALYSIS: NHH ESPERANTO STUDY")
print("="*80)

# Load data
print("\n📊 Loading dataset...")
df = pd.read_csv('data/processed/nhh_esperanto_complete_unified.csv', low_memory=False)

print(f"Dataset: {len(df)} participants, {len(df.columns)} variables")

# Clean and prepare data
df['testscore'] = pd.to_numeric(df['testscore'], errors='coerce')
df['treatment'] = df['treatment'].fillna('Unknown')

# Calculate effect sizes (Cohen's d)
def cohens_d(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std if pooled_std > 0 else 0

# ============================================================================
# FIGURE 1: ADVANCED TREATMENT EFFECTS ANALYSIS
# ============================================================================
print("\n📈 Creating Figure 1: Advanced Treatment Effects Analysis...")

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1.1 Violin plots with individual points
ax1 = fig.add_subplot(gs[0, :2])
treatment_data = df[df['treatment'].isin(['Control', 'AI-assisted', 'AI-guided'])].copy()
treatment_order = ['Control', 'AI-assisted', 'AI-guided']

parts = ax1.violinplot([treatment_data[treatment_data['treatment']==t]['testscore'].dropna()
                        for t in treatment_order],
                       positions=range(len(treatment_order)),
                       showmeans=True, showextrema=True, showmedians=True)

for i, (pc, treatment) in enumerate(zip(parts['bodies'], treatment_order)):
    pc.set_facecolor(COLORS[treatment])
    pc.set_alpha(0.6)

# Add individual points with jitter
for i, treatment in enumerate(treatment_order):
    scores = treatment_data[treatment_data['treatment']==treatment]['testscore'].dropna()
    y = scores.values
    x = np.random.normal(i, 0.04, size=len(y))
    ax1.scatter(x, y, alpha=0.3, s=20, color=COLORS[treatment])

ax1.set_xticks(range(len(treatment_order)))
ax1.set_xticklabels(treatment_order)
ax1.set_ylabel('Test Score (0-13)', fontweight='bold')
ax1.set_title('Test Score Distribution by Treatment Group\n(Violin plots with individual observations)',
              fontweight='bold', fontsize=14)
ax1.grid(axis='y', alpha=0.3)

# Add sample sizes and means
for i, treatment in enumerate(treatment_order):
    scores = treatment_data[treatment_data['treatment']==treatment]['testscore'].dropna()
    n = len(scores)
    mean = scores.mean()
    ax1.text(i, ax1.get_ylim()[1]*0.95, f'n={n}\nM={mean:.2f}',
             ha='center', va='top', fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

# 1.2 Effect sizes
ax2 = fig.add_subplot(gs[0, 2])
control_scores = treatment_data[treatment_data['treatment']=='Control']['testscore'].dropna()
ai_assisted_scores = treatment_data[treatment_data['treatment']=='AI-assisted']['testscore'].dropna()
ai_guided_scores = treatment_data[treatment_data['treatment']=='AI-guided']['testscore'].dropna()

effect_sizes = []
comparisons = []

if len(control_scores) > 0 and len(ai_assisted_scores) > 0:
    d1 = cohens_d(ai_assisted_scores, control_scores)
    effect_sizes.append(d1)
    comparisons.append('AI-assisted\nvs Control')

if len(control_scores) > 0 and len(ai_guided_scores) > 0:
    d2 = cohens_d(ai_guided_scores, control_scores)
    effect_sizes.append(d2)
    comparisons.append('AI-guided\nvs Control')

if len(ai_assisted_scores) > 0 and len(ai_guided_scores) > 0:
    d3 = cohens_d(ai_guided_scores, ai_assisted_scores)
    effect_sizes.append(d3)
    comparisons.append('AI-guided\nvs Assisted')

colors_bars = ['#3498db', '#e74c3c', '#9b59b6']
bars = ax2.barh(range(len(effect_sizes)), effect_sizes, color=colors_bars)
ax2.set_yticks(range(len(comparisons)))
ax2.set_yticklabels(comparisons, fontsize=10)
ax2.set_xlabel("Cohen's d", fontweight='bold')
ax2.set_title('Effect Sizes\n(Treatment Comparisons)', fontweight='bold', fontsize=12)
ax2.axvline(0, color='black', linewidth=1)
ax2.axvline(0.2, color='green', linewidth=1, linestyle='--', alpha=0.5, label='Small')
ax2.axvline(0.5, color='orange', linewidth=1, linestyle='--', alpha=0.5, label='Medium')
ax2.axvline(0.8, color='red', linewidth=1, linestyle='--', alpha=0.5, label='Large')
ax2.legend(fontsize=8, loc='lower right')
ax2.grid(axis='x', alpha=0.3)

# Add values on bars
for i, (bar, val) in enumerate(zip(bars, effect_sizes)):
    ax2.text(val + 0.02, bar.get_y() + bar.get_height()/2,
             f'd={val:.3f}', va='center', fontsize=9, fontweight='bold')

# 1.3 Cumulative Distribution Functions
ax3 = fig.add_subplot(gs[1, :])
for treatment in treatment_order:
    scores = treatment_data[treatment_data['treatment']==treatment]['testscore'].dropna().sort_values()
    cumulative = np.arange(1, len(scores)+1) / len(scores)
    ax3.plot(scores, cumulative, linewidth=2.5, label=treatment, color=COLORS[treatment], alpha=0.8)

ax3.set_xlabel('Test Score', fontweight='bold')
ax3.set_ylabel('Cumulative Probability', fontweight='bold')
ax3.set_title('Cumulative Distribution Functions by Treatment Group\n(Shows probability of scoring at or below each value)',
              fontweight='bold', fontsize=14)
ax3.legend(fontsize=11, framealpha=0.9)
ax3.grid(alpha=0.3)
ax3.set_xlim(0, 13)
ax3.set_ylim(0, 1)

# 1.4 Percentile analysis
ax4 = fig.add_subplot(gs[2, :])
percentiles = [10, 25, 50, 75, 90]
x_pos = np.arange(len(percentiles))
width = 0.25

for i, treatment in enumerate(treatment_order):
    scores = treatment_data[treatment_data['treatment']==treatment]['testscore'].dropna()
    if len(scores) > 0:
        perc_values = [np.percentile(scores, p) for p in percentiles]
        ax4.bar(x_pos + i*width, perc_values, width, label=treatment,
                color=COLORS[treatment], alpha=0.7)

ax4.set_xlabel('Percentile', fontweight='bold')
ax4.set_ylabel('Test Score', fontweight='bold')
ax4.set_title('Score Percentiles by Treatment Group\n(Examining effects across the performance distribution)',
              fontweight='bold', fontsize=14)
ax4.set_xticks(x_pos + width)
ax4.set_xticklabels([f'{p}th' for p in percentiles])
ax4.legend(fontsize=11)
ax4.grid(axis='y', alpha=0.3)

plt.savefig('analysis/visualizations/11_advanced_treatment_effects.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 11_advanced_treatment_effects.png")
plt.close()

# ============================================================================
# FIGURE 2: DEMOGRAPHIC INTERACTIONS AND HETEROGENEOUS TREATMENT EFFECTS
# ============================================================================
print("\n📊 Creating Figure 2: Demographic Interactions...")

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)

# 2.1 Treatment × Faculty interaction
ax1 = fig.add_subplot(gs[0, :])
if 'faculty' in df.columns:
    faculty_treat = df[df['treatment'].isin(treatment_order)].copy()
    top_faculties = faculty_treat['faculty'].value_counts().head(6).index

    faculty_means = []
    for faculty in top_faculties:
        means = []
        for treatment in treatment_order:
            scores = faculty_treat[(faculty_treat['faculty']==faculty) &
                                  (faculty_treat['treatment']==treatment)]['testscore'].dropna()
            means.append(scores.mean() if len(scores) > 0 else np.nan)
        faculty_means.append(means)

    x = np.arange(len(top_faculties))
    width = 0.25

    for i, treatment in enumerate(treatment_order):
        values = [faculty_means[j][i] for j in range(len(top_faculties))]
        ax1.bar(x + i*width, values, width, label=treatment, color=COLORS[treatment], alpha=0.7)

    ax1.set_xlabel('Faculty', fontweight='bold')
    ax1.set_ylabel('Mean Test Score', fontweight='bold')
    ax1.set_title('Treatment Effects by Faculty\n(Heterogeneous treatment effects across disciplines)',
                  fontweight='bold', fontsize=14)
    ax1.set_xticks(x + width)
    ax1.set_xticklabels(top_faculties, rotation=15, ha='right')
    ax1.legend(fontsize=10)
    ax1.grid(axis='y', alpha=0.3)

# 2.2 Treatment × Gender interaction
ax2 = fig.add_subplot(gs[1, 0])
if 'gender' in df.columns:
    gender_treat = df[df['treatment'].isin(treatment_order)].copy()
    gender_labels = {1: 'Male', 2: 'Female'}

    for treatment in treatment_order:
        means = []
        errors = []
        for gender_id in [1, 2]:
            scores = gender_treat[(gender_treat['gender']==gender_id) &
                                 (gender_treat['treatment']==treatment)]['testscore'].dropna()
            means.append(scores.mean() if len(scores) > 0 else np.nan)
            errors.append(scores.sem() if len(scores) > 0 else 0)

        x_pos = [0, 1]
        ax2.errorbar(x_pos, means, yerr=errors, marker='o', markersize=8,
                    linewidth=2, capsize=5, label=treatment, color=COLORS[treatment])

    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['Male', 'Female'])
    ax2.set_ylabel('Mean Test Score', fontweight='bold')
    ax2.set_title('Treatment × Gender\nInteraction', fontweight='bold', fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)

# 2.3 Treatment × GPA interaction
ax3 = fig.add_subplot(gs[1, 1])
if 'gpa' in df.columns:
    gpa_treat = df[df['treatment'].isin(treatment_order)].copy()

    for treatment in treatment_order:
        means = []
        for gpa in sorted(gpa_treat['gpa'].dropna().unique()):
            scores = gpa_treat[(gpa_treat['gpa']==gpa) &
                              (gpa_treat['treatment']==treatment)]['testscore'].dropna()
            means.append(scores.mean() if len(scores) > 5 else np.nan)

        x_pos = sorted(gpa_treat['gpa'].dropna().unique())
        ax3.plot(x_pos[:len(means)], means, marker='o', markersize=8,
                linewidth=2, label=treatment, color=COLORS[treatment])

    ax3.set_xlabel('GPA Level', fontweight='bold')
    ax3.set_ylabel('Mean Test Score', fontweight='bold')
    ax3.set_title('Treatment × GPA\nInteraction', fontweight='bold', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(alpha=0.3)

# 2.4 Treatment × AI Familiarity
ax4 = fig.add_subplot(gs[1, 2])
if 'AIfamiliar' in df.columns:
    ai_treat = df[df['treatment'].isin(treatment_order)].copy()

    for treatment in treatment_order:
        means = []
        for level in sorted(ai_treat['AIfamiliar'].dropna().unique()):
            scores = ai_treat[(ai_treat['AIfamiliar']==level) &
                             (ai_treat['treatment']==treatment)]['testscore'].dropna()
            means.append(scores.mean() if len(scores) > 5 else np.nan)

        x_pos = sorted(ai_treat['AIfamiliar'].dropna().unique())
        ax4.plot(x_pos[:len(means)], means, marker='o', markersize=8,
                linewidth=2, label=treatment, color=COLORS[treatment])

    ax4.set_xlabel('AI Familiarity Level', fontweight='bold')
    ax4.set_ylabel('Mean Test Score', fontweight='bold')
    ax4.set_title('Treatment × AI Familiarity\nInteraction', fontweight='bold', fontsize=12)
    ax4.legend(fontsize=9)
    ax4.grid(alpha=0.3)

# 2.5 Treatment × Language Background
ax5 = fig.add_subplot(gs[2, :])
if 'languages' in df.columns:
    lang_treat = df[df['treatment'].isin(treatment_order)].copy()
    lang_treat['languages_num'] = pd.to_numeric(lang_treat['languages'], errors='coerce')
    lang_treat = lang_treat.dropna(subset=['languages_num'])
    lang_treat['lang_group'] = pd.cut(lang_treat['languages_num'],
                                      bins=[0, 2, 3, 5, 20],
                                      labels=['1-2', '3', '4-5', '6+'])

    x_pos = np.arange(4)
    width = 0.25

    for i, treatment in enumerate(treatment_order):
        means = []
        for group in ['1-2', '3', '4-5', '6+']:
            scores = lang_treat[(lang_treat['lang_group']==group) &
                               (lang_treat['treatment']==treatment)]['testscore'].dropna()
            means.append(scores.mean() if len(scores) > 0 else np.nan)

        ax5.bar(x_pos + i*width, means, width, label=treatment,
               color=COLORS[treatment], alpha=0.7)

    ax5.set_xlabel('Number of Languages Spoken', fontweight='bold')
    ax5.set_ylabel('Mean Test Score', fontweight='bold')
    ax5.set_title('Treatment Effects by Language Background\n(Multilingual advantage across treatment conditions)',
                  fontweight='bold', fontsize=14)
    ax5.set_xticks(x_pos + width)
    ax5.set_xticklabels(['1-2', '3', '4-5', '6+'])
    ax5.legend(fontsize=11)
    ax5.grid(axis='y', alpha=0.3)

plt.savefig('analysis/visualizations/12_demographic_interactions.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 12_demographic_interactions.png")
plt.close()

# ============================================================================
# FIGURE 3: TEMPORAL PATTERNS AND SESSION DYNAMICS
# ============================================================================
print("\n⏰ Creating Figure 3: Temporal Patterns...")

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 3.1 Performance over time (by start date)
ax1 = fig.add_subplot(gs[0, :])
if 'StartDate' in df.columns:
    df['start_datetime'] = pd.to_datetime(df['StartDate'], errors='coerce')
    df['day_of_study'] = (df['start_datetime'] - df['start_datetime'].min()).dt.days

    temporal_data = df[df['treatment'].isin(treatment_order)].copy()

    for treatment in treatment_order:
        treatment_df = temporal_data[temporal_data['treatment']==treatment]
        if len(treatment_df) > 0:
            daily_means = treatment_df.groupby('day_of_study')['testscore'].agg(['mean', 'sem']).reset_index()
            ax1.errorbar(daily_means['day_of_study'], daily_means['mean'],
                        yerr=daily_means['sem'], marker='o', markersize=6,
                        linewidth=2, capsize=4, label=treatment, color=COLORS[treatment], alpha=0.7)

    ax1.set_xlabel('Days Since Study Start', fontweight='bold')
    ax1.set_ylabel('Mean Test Score', fontweight='bold')
    ax1.set_title('Performance Trends Over Study Period\n(Tracking stability across data collection)',
                  fontweight='bold', fontsize=14)
    ax1.legend(fontsize=11)
    ax1.grid(alpha=0.3)

# 3.2 Time of day effects
ax2 = fig.add_subplot(gs[1, 0])
if 'starthour' in df.columns:
    df['starthour_num'] = pd.to_numeric(df['starthour'], errors='coerce')
    time_data = df[df['treatment'].isin(treatment_order)].copy()
    time_data['time_period'] = pd.cut(time_data['starthour_num'],
                                      bins=[0, 9, 12, 15, 18, 24],
                                      labels=['Early\n(0-9)', 'Morning\n(9-12)',
                                             'Afternoon\n(12-15)', 'Evening\n(15-18)', 'Night\n(18-24)'])

    period_means = time_data.groupby(['time_period', 'treatment'])['testscore'].mean().unstack()
    period_means.plot(kind='bar', ax=ax2, color=[COLORS[t] for t in treatment_order], alpha=0.7)

    ax2.set_xlabel('Time of Day', fontweight='bold')
    ax2.set_ylabel('Mean Test Score', fontweight='bold')
    ax2.set_title('Performance by\nTime of Day', fontweight='bold', fontsize=12)
    ax2.legend(fontsize=9, title='Treatment')
    ax2.grid(axis='y', alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

# 3.3 Duration distribution by treatment
ax3 = fig.add_subplot(gs[1, 1])
if 'Durationinseconds' in df.columns:
    duration_data = df[df['treatment'].isin(treatment_order)].copy()
    duration_data['duration_minutes'] = duration_data['Durationinseconds'] / 60

    for treatment in treatment_order:
        durations = duration_data[duration_data['treatment']==treatment]['duration_minutes'].dropna()
        durations = durations[(durations > 5) & (durations < 200)]  # Remove outliers
        ax3.hist(durations, bins=30, alpha=0.5, label=treatment,
                color=COLORS[treatment], density=True)

    ax3.set_xlabel('Duration (minutes)', fontweight='bold')
    ax3.set_ylabel('Density', fontweight='bold')
    ax3.set_title('Session Duration\nDistribution', fontweight='bold', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(axis='y', alpha=0.3)

# 3.4 Duration vs Performance
ax4 = fig.add_subplot(gs[1, 2])
if 'Durationinseconds' in df.columns:
    duration_score = df[df['treatment'].isin(treatment_order)].copy()
    duration_score['duration_minutes'] = duration_score['Durationinseconds'] / 60
    duration_score = duration_score[(duration_score['duration_minutes'] > 5) &
                                   (duration_score['duration_minutes'] < 200)]

    for treatment in treatment_order:
        treat_data = duration_score[duration_score['treatment']==treatment]
        if len(treat_data) > 10:
            # Get clean data for both x and y
            clean_data = treat_data[['duration_minutes', 'testscore']].dropna()
            if len(clean_data) > 10:
                ax4.scatter(clean_data['duration_minutes'], clean_data['testscore'],
                           alpha=0.4, s=30, label=treatment, color=COLORS[treatment])

                # Add trend line
                z = np.polyfit(clean_data['duration_minutes'], clean_data['testscore'], 2)
                p = np.poly1d(z)
                x_smooth = np.linspace(clean_data['duration_minutes'].min(),
                                      clean_data['duration_minutes'].max(), 100)
                ax4.plot(x_smooth, p(x_smooth), linewidth=2, color=COLORS[treatment])

    ax4.set_xlabel('Duration (minutes)', fontweight='bold')
    ax4.set_ylabel('Test Score', fontweight='bold')
    ax4.set_title('Duration-Performance\nRelationship', fontweight='bold', fontsize=12)
    ax4.legend(fontsize=9)
    ax4.grid(alpha=0.3)

# 3.5 Completion timing patterns
ax5 = fig.add_subplot(gs[2, :])
if 'StartDate' in df.columns and 'EndDate' in df.columns:
    df['end_datetime'] = pd.to_datetime(df['EndDate'], errors='coerce')
    completion_data = df[df['treatment'].isin(treatment_order)].copy()
    completion_data['completion_hour'] = completion_data['end_datetime'].dt.hour

    for treatment in treatment_order:
        treat_comp = completion_data[completion_data['treatment']==treatment]
        hour_counts = treat_comp['completion_hour'].value_counts().sort_index()
        ax5.plot(hour_counts.index, hour_counts.values, marker='o', markersize=6,
                linewidth=2, label=treatment, color=COLORS[treatment])

    ax5.set_xlabel('Hour of Day (Completion Time)', fontweight='bold')
    ax5.set_ylabel('Number of Completions', fontweight='bold')
    ax5.set_title('Session Completion Patterns Throughout the Day\n(Identifying peak engagement periods)',
                  fontweight='bold', fontsize=14)
    ax5.legend(fontsize=11)
    ax5.grid(alpha=0.3)
    ax5.set_xlim(0, 23)

plt.savefig('analysis/visualizations/13_temporal_patterns.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 13_temporal_patterns.png")
plt.close()

# ============================================================================
# FIGURE 4: QUESTION-LEVEL PERFORMANCE ANALYSIS
# ============================================================================
print("\n📝 Creating Figure 4: Question-Level Analysis...")

# Find all question correctness columns
question_cols = [col for col in df.columns if col.endswith('_c') and col.startswith('Q')]
print(f"   Found {len(question_cols)} question-level variables")

if len(question_cols) > 20:
    question_cols = question_cols[:30]  # Take first 30 for visualization

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# 4.1 Question difficulty (overall)
ax1 = fig.add_subplot(gs[0, :])
question_means = []
question_labels = []
for col in question_cols[:20]:
    mean_correct = df[col].mean() * 100  # Convert to percentage
    if not np.isnan(mean_correct):
        question_means.append(mean_correct)
        question_labels.append(col.replace('_c', ''))

if len(question_means) > 0:
    sorted_idx = np.argsort(question_means)
    sorted_means = [question_means[i] for i in sorted_idx]
    sorted_labels = [question_labels[i] for i in sorted_idx]

    colors = ['#e74c3c' if m < 50 else '#f39c12' if m < 70 else '#2ecc71'
              for m in sorted_means]

    ax1.barh(range(len(sorted_means)), sorted_means, color=colors, alpha=0.7)
    ax1.set_yticks(range(len(sorted_labels)))
    ax1.set_yticklabels(sorted_labels, fontsize=9)
    ax1.set_xlabel('Correct Response Rate (%)', fontweight='bold')
    ax1.set_title('Question Difficulty Ranking\n(Red: Hard <50%, Orange: Medium 50-70%, Green: Easy >70%)',
                  fontweight='bold', fontsize=14)
    ax1.grid(axis='x', alpha=0.3)
    ax1.axvline(50, color='red', linestyle='--', alpha=0.5, linewidth=2)
    ax1.axvline(70, color='orange', linestyle='--', alpha=0.5, linewidth=2)

# 4.2 Treatment differences by question
ax2 = fig.add_subplot(gs[1, :])
treatment_diffs = []
question_names = []

for col in question_cols[:15]:
    control_correct = df[df['treatment']=='Control'][col].mean()
    ai_correct = df[df['treatment']=='AI-assisted'][col].mean()

    if not np.isnan(control_correct) and not np.isnan(ai_correct):
        diff = (ai_correct - control_correct) * 100
        treatment_diffs.append(diff)
        question_names.append(col.replace('_c', ''))

if len(treatment_diffs) > 0:
    colors = ['#2ecc71' if d > 0 else '#e74c3c' for d in treatment_diffs]

    ax2.barh(range(len(treatment_diffs)), treatment_diffs, color=colors, alpha=0.7)
    ax2.set_yticks(range(len(question_names)))
    ax2.set_yticklabels(question_names, fontsize=9)
    ax2.set_xlabel('AI-assisted Advantage (percentage points)', fontweight='bold')
    ax2.set_title('Question-Level Treatment Effects\n(Positive = AI advantage, Negative = Control advantage)',
                  fontweight='bold', fontsize=14)
    ax2.axvline(0, color='black', linewidth=2)
    ax2.grid(axis='x', alpha=0.3)

# 4.3 Correlation between questions
ax3 = fig.add_subplot(gs[2, 0])
if len(question_cols) >= 10:
    question_subset = question_cols[:10]
    corr_matrix = df[question_subset].corr()

    im = ax3.imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
    ax3.set_xticks(range(len(question_subset)))
    ax3.set_yticks(range(len(question_subset)))
    ax3.set_xticklabels([q.replace('_c', '') for q in question_subset], rotation=45, ha='right', fontsize=8)
    ax3.set_yticklabels([q.replace('_c', '') for q in question_subset], fontsize=8)
    ax3.set_title('Question Inter-correlations\n(First 10 questions)', fontweight='bold', fontsize=12)
    plt.colorbar(im, ax=ax3, label='Correlation')

# 4.4 Score composition by treatment
ax4 = fig.add_subplot(gs[2, 1])
if len(question_cols) >= 5:
    score_data = []
    for treatment in treatment_order:
        treat_df = df[df['treatment']==treatment]
        total = treat_df[question_cols[:5]].sum(axis=1).mean()
        score_data.append(total)

    ax4.bar(range(len(treatment_order)), score_data,
           color=[COLORS[t] for t in treatment_order], alpha=0.7)
    ax4.set_xticks(range(len(treatment_order)))
    ax4.set_xticklabels(treatment_order)
    ax4.set_ylabel('Mean Correct (first 5 questions)', fontweight='bold')
    ax4.set_title('Early Question Performance\nby Treatment', fontweight='bold', fontsize=12)
    ax4.grid(axis='y', alpha=0.3)

plt.savefig('analysis/visualizations/14_question_level_analysis.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 14_question_level_analysis.png")
plt.close()

# ============================================================================
# FIGURE 5: COMPREHENSIVE DASHBOARD
# ============================================================================
print("\n📋 Creating Figure 5: Comprehensive Dashboard...")

fig = plt.figure(figsize=(22, 14))
fig.suptitle('NHH Esperanto Study: Comprehensive Dashboard',
             fontsize=18, fontweight='bold', y=0.995)
gs = fig.add_gridspec(4, 4, hspace=0.4, wspace=0.4)

# 5.1 Sample sizes
ax1 = fig.add_subplot(gs[0, 0])
sample_sizes = [len(df[df['treatment']==t]) for t in treatment_order]
ax1.pie(sample_sizes, labels=treatment_order, autopct='%1.1f%%',
       colors=[COLORS[t] for t in treatment_order], startangle=90)
ax1.set_title('Sample Distribution', fontweight='bold', fontsize=11)

# 5.2 Mean scores with CI
ax2 = fig.add_subplot(gs[0, 1:3])
means = []
cis = []
for treatment in treatment_order:
    scores = df[df['treatment']==treatment]['testscore'].dropna()
    means.append(scores.mean())
    ci = 1.96 * scores.sem()  # 95% CI
    cis.append(ci)

x_pos = np.arange(len(treatment_order))
bars = ax2.bar(x_pos, means, yerr=cis, capsize=10,
              color=[COLORS[t] for t in treatment_order], alpha=0.7,
              error_kw={'linewidth': 2, 'elinewidth': 2})
ax2.set_xticks(x_pos)
ax2.set_xticklabels(treatment_order)
ax2.set_ylabel('Mean Test Score', fontweight='bold')
ax2.set_title('Primary Outcome: Mean Scores with 95% CI', fontweight='bold', fontsize=11)
ax2.grid(axis='y', alpha=0.3)

# Add values on bars
for bar, mean, ci in zip(bars, means, cis):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + ci + 0.1,
            f'{mean:.2f}', ha='center', va='bottom', fontweight='bold')

# 5.3 Distribution comparison
ax3 = fig.add_subplot(gs[0, 3])
for treatment in treatment_order:
    scores = df[df['treatment']==treatment]['testscore'].dropna()
    ax3.hist(scores, bins=13, alpha=0.5, label=treatment,
            color=COLORS[treatment], density=True)
ax3.set_xlabel('Test Score', fontweight='bold')
ax3.set_ylabel('Density', fontweight='bold')
ax3.set_title('Score Distributions', fontweight='bold', fontsize=11)
ax3.legend(fontsize=8)
ax3.grid(axis='y', alpha=0.3)

# 5.4 Key metrics table
ax4 = fig.add_subplot(gs[1, :2])
ax4.axis('tight')
ax4.axis('off')

table_data = []
table_data.append(['Metric', 'Control', 'AI-assisted', 'AI-guided'])

for metric_name, metric_func in [('N', len),
                                  ('Mean', lambda x: f"{x.mean():.2f}"),
                                  ('Median', lambda x: f"{x.median():.2f}"),
                                  ('SD', lambda x: f"{x.std():.2f}"),
                                  ('Min', lambda x: f"{x.min():.0f}"),
                                  ('Max', lambda x: f"{x.max():.0f}")]:
    row = [metric_name]
    for treatment in treatment_order:
        scores = df[df['treatment']==treatment]['testscore'].dropna()
        if len(scores) > 0:
            value = metric_func(scores)
            row.append(str(value))
        else:
            row.append('N/A')
    table_data.append(row)

table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                 colColours=['lightgray']*4,
                 cellColours=[['white']*4]*len(table_data))
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
ax4.set_title('Descriptive Statistics', fontweight='bold', fontsize=11, pad=20)

# 5.5 Demographics summary
ax5 = fig.add_subplot(gs[1, 2:])
ax5.axis('tight')
ax5.axis('off')

demo_data = [['Demographic', 'Distribution']]
if 'gender' in df.columns:
    female_pct = (df['gender']==2).sum() / len(df) * 100
    demo_data.append(['Gender', f'{female_pct:.1f}% Female'])
if 'age' in df.columns:
    modal_age = df['age'].mode()[0] if len(df['age'].mode()) > 0 else 'N/A'
    demo_data.append(['Modal Age', str(modal_age)])
if 'faculty' in df.columns:
    top_faculty = df['faculty'].value_counts().index[0]
    demo_data.append(['Top Faculty', str(top_faculty)[:30]])
if 'AIfamiliar' in df.columns:
    mean_fam = df['AIfamiliar'].mean()
    demo_data.append(['Mean AI Familiarity', f'{mean_fam:.1f}/5'])

table2 = ax5.table(cellText=demo_data, cellLoc='left', loc='center',
                  colColours=['lightgray']*2,
                  cellColours=[['white']*2]*len(demo_data))
table2.auto_set_font_size(False)
table2.set_fontsize(10)
table2.scale(1, 2)
ax5.set_title('Sample Characteristics', fontweight='bold', fontsize=11, pad=20)

# 5.6 Time investment
ax6 = fig.add_subplot(gs[2, :2])
if 'time_test' in df.columns:
    for treatment in treatment_order:
        times = df[df['treatment']==treatment]['time_test'].dropna()
        if len(times) > 0:
            ax6.boxplot([times], positions=[treatment_order.index(treatment)],
                       widths=0.6, patch_artist=True,
                       boxprops=dict(facecolor=COLORS[treatment], alpha=0.7),
                       medianprops=dict(color='red', linewidth=2))

    ax6.set_xticks(range(len(treatment_order)))
    ax6.set_xticklabels(treatment_order)
    ax6.set_ylabel('Time on Test', fontweight='bold')
    ax6.set_title('Time Investment by Treatment', fontweight='bold', fontsize=11)
    ax6.grid(axis='y', alpha=0.3)

# 5.7 Engagement indices
ax7 = fig.add_subplot(gs[2, 2:])
indices = ['index_motivation', 'index_confidence', 'index_complement']
available_indices = [idx for idx in indices if idx in df.columns]

if len(available_indices) > 0:
    index_means = []
    for treatment in treatment_order:
        treat_means = []
        for idx in available_indices:
            mean_val = df[df['treatment']==treatment][idx].mean()
            treat_means.append(mean_val if not np.isnan(mean_val) else 0)
        index_means.append(treat_means)

    x = np.arange(len(available_indices))
    width = 0.25

    for i, treatment in enumerate(treatment_order):
        ax7.bar(x + i*width, index_means[i], width, label=treatment,
               color=COLORS[treatment], alpha=0.7)

    ax7.set_xticks(x + width)
    ax7.set_xticklabels([idx.replace('index_', '').title() for idx in available_indices],
                        rotation=15, ha='right')
    ax7.set_ylabel('Mean Index Score', fontweight='bold')
    ax7.set_title('Engagement Indices by Treatment', fontweight='bold', fontsize=11)
    ax7.legend(fontsize=9)
    ax7.grid(axis='y', alpha=0.3)

# 5.8 Statistical tests summary
ax8 = fig.add_subplot(gs[3, :])
ax8.axis('tight')
ax8.axis('off')

test_results = [['Statistical Test', 'Comparison', 'Result', 'Interpretation']]

# T-test: Control vs AI-assisted
control_scores = df[df['treatment']=='Control']['testscore'].dropna()
ai_assisted_scores = df[df['treatment']=='AI-assisted']['testscore'].dropna()
if len(control_scores) > 0 and len(ai_assisted_scores) > 0:
    t_stat, p_val = stats.ttest_ind(control_scores, ai_assisted_scores)
    d = cohens_d(ai_assisted_scores, control_scores)
    sig = '✓ Significant' if p_val < 0.05 else '✗ Not significant'
    test_results.append(['Independent t-test', 'Control vs AI-assisted',
                        f't={t_stat:.2f}, p={p_val:.4f}, d={d:.2f}', sig])

# T-test: Control vs AI-guided
ai_guided_scores = df[df['treatment']=='AI-guided']['testscore'].dropna()
if len(control_scores) > 0 and len(ai_guided_scores) > 0:
    t_stat2, p_val2 = stats.ttest_ind(control_scores, ai_guided_scores)
    d2 = cohens_d(ai_guided_scores, control_scores)
    sig2 = '✓ Significant' if p_val2 < 0.05 else '✗ Not significant'
    test_results.append(['Independent t-test', 'Control vs AI-guided',
                        f't={t_stat2:.2f}, p={p_val2:.4f}, d={d2:.2f}', sig2])

# ANOVA
if len(control_scores) > 0 and len(ai_assisted_scores) > 0 and len(ai_guided_scores) > 0:
    f_stat, p_anova = stats.f_oneway(control_scores, ai_assisted_scores, ai_guided_scores)
    sig_anova = '✓ Significant' if p_anova < 0.05 else '✗ Not significant'
    test_results.append(['One-way ANOVA', 'All three groups',
                        f'F={f_stat:.2f}, p={p_anova:.4f}', sig_anova])

table3 = ax8.table(cellText=test_results, cellLoc='center', loc='center',
                  colColours=['lightgray']*4,
                  cellColours=[['white']*4]*len(test_results),
                  colWidths=[0.2, 0.25, 0.35, 0.2])
table3.auto_set_font_size(False)
table3.set_fontsize(9)
table3.scale(1, 2.5)
ax8.set_title('Statistical Hypothesis Tests (α = 0.05)', fontweight='bold', fontsize=11, pad=20)

plt.savefig('analysis/visualizations/15_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 15_comprehensive_dashboard.png")
plt.close()

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print("\n" + "="*80)
print("SUMMARY OF ADVANCED ANALYSIS")
print("="*80)

print(f"\n📊 Sample Size: {len(df)} participants")
print(f"   - Control: {len(df[df['treatment']=='Control'])}")
print(f"   - AI-assisted: {len(df[df['treatment']=='AI-assisted'])}")
print(f"   - AI-guided: {len(df[df['treatment']=='AI-guided'])}")

print(f"\n📈 Test Scores:")
for treatment in treatment_order:
    scores = df[df['treatment']==treatment]['testscore'].dropna()
    if len(scores) > 0:
        print(f"   {treatment}: M={scores.mean():.2f}, SD={scores.std():.2f}, n={len(scores)}")

print(f"\n📐 Effect Sizes (Cohen's d):")
if len(control_scores) > 0 and len(ai_assisted_scores) > 0:
    print(f"   AI-assisted vs Control: d={cohens_d(ai_assisted_scores, control_scores):.3f}")
if len(control_scores) > 0 and len(ai_guided_scores) > 0:
    print(f"   AI-guided vs Control: d={cohens_d(ai_guided_scores, control_scores):.3f}")

print("\n" + "="*80)
print("✅ ADVANCED ANALYSIS COMPLETE!")
print("="*80)
print("\nAll visualizations saved to: analysis/visualizations/")
print("\nNew visualizations created:")
print("  11. Advanced treatment effects with violin plots and effect sizes")
print("  12. Demographic interactions and heterogeneous treatment effects")
print("  13. Temporal patterns and session dynamics")
print("  14. Question-level performance analysis")
print("  15. Comprehensive dashboard with all key metrics")
