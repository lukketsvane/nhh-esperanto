#!/usr/bin/env python3
"""
Pre-Analysis Plan (PAP) Analysis Script
========================================
Based on: AI in the Classroom: Barrier or Gateway to Academic and Labor Market Success?
Authors: Catalina Franco, Natalie Irmert, Siri Isaksson
Date: December 4, 2024

This script implements the COMPLETE analysis plan specified in the PAP including:
1. Main treatment effects (Equation 1)
2. Gender heterogeneity (Equation 2)
3. GPA heterogeneity (similar to Equation 2)
4. Triple interactions (Equation 3: treatment × gender × GPA)
5. Top/low scorer analysis
6. Stage 2 performance (practice questions)
7. Mechanism analysis (4 categories with summary indices)
8. Comprehensive visualizations following PAP specifications
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")

# Create output directory
output_dir = Path(__file__).parent / 'visualizations'
output_dir.mkdir(parents=True, exist_ok=True)

print("="*80)
print("NHH ESPERANTO STUDY - COMPLETE PRE-ANALYSIS PLAN IMPLEMENTATION")
print("="*80)
print()

# Load data
print("Loading data...")
df = pd.read_csv('../data/processed/nhh_esperanto_complete_unified.csv')

# Filter to main study (exclude pilot if exists)
if 'pilot' in df.columns:
    df = df[df['pilot'] != 1]

# Remove observations that left during test
if 'lefttest' in df.columns:
    df = df[df['lefttest'] != 1]

print(f"Sample size: {len(df)}")
print(f"Treatment distribution:")
print(f"  Control: {(df['control'] == 1).sum()}")
print(f"  AI-Assisted: {(df['ai_assist'] == 1).sum()}")
print(f"  AI-Guided: {(df['ai_guided'] == 1).sum()}")
print()

# Define treatment labels for visualizations
treatments = ['Control', 'AI-Assisted', 'AI-Guided']
colors_main = ['#3498db', '#e74c3c', '#2ecc71']

# Main outcome variable
outcome = 'testscore'

# ============================================================================
# 1. MAIN TREATMENT EFFECTS (Equation 1)
# ============================================================================
print("\n" + "="*80)
print("1. MAIN TREATMENT EFFECTS (Equation 1)")
print("="*80)

# Main regression
model1 = smf.ols(f'{outcome} ~ ai_assist + ai_guided', data=df).fit(cov_type='HC3')
print(model1.summary())

# Calculate means for visualization
control_mean = df[df['control'] == 1][outcome].mean()
means = [
    control_mean,
    df[df['ai_assist'] == 1][outcome].mean(),
    df[df['ai_guided'] == 1][outcome].mean()
]
ses = [
    df[df['control'] == 1][outcome].std() / np.sqrt((df['control'] == 1).sum()),
    df[df['ai_assist'] == 1][outcome].std() / np.sqrt((df['ai_assist'] == 1).sum()),
    df[df['ai_guided'] == 1][outcome].std() / np.sqrt((df['ai_guided'] == 1).sum())
]

# Visualization 1: Main Treatment Effects
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(treatments, means, yerr=[1.96*se for se in ses], capsize=10,
               color=colors_main, alpha=0.7, edgecolor='black', linewidth=2)
ax.set_ylabel('Test Score', fontsize=14, fontweight='bold')
ax.set_xlabel('Treatment', fontsize=14, fontweight='bold')
ax.set_title('Main Treatment Effects on Test Score\n(PAP Equation 1)',
             fontsize=16, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_ylim(0, max(means) * 1.3)

for bar, mean, n in zip(bars, means, [(df['control'] == 1).sum(),
                                       (df['ai_assist'] == 1).sum(),
                                       (df['ai_guided'] == 1).sum()]):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{mean:.2f}\n(n={n})',
            ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig(output_dir / '01_main_treatment_effects.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: 01_main_treatment_effects.png")

# ============================================================================
# 2. GENDER HETEROGENEITY (Equation 2)
# ============================================================================
print("\n" + "="*80)
print("2. GENDER HETEROGENEITY (Equation 2)")
print("="*80)

model2 = smf.ols(f'{outcome} ~ ai_assist + ai_guided + female + ai_assist:female + ai_guided:female',
                 data=df).fit(cov_type='HC3')
print(model2.summary())

# Visualization 2: Treatment Effects by Gender
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(treatments))
width = 0.35

men_means = [
    df[(df['control'] == 1) & (df['female'] == 0)][outcome].mean(),
    df[(df['ai_assist'] == 1) & (df['female'] == 0)][outcome].mean(),
    df[(df['ai_guided'] == 1) & (df['female'] == 0)][outcome].mean()
]
men_ses = [
    df[(df['control'] == 1) & (df['female'] == 0)][outcome].std() / np.sqrt(((df['control'] == 1) & (df['female'] == 0)).sum()),
    df[(df['ai_assist'] == 1) & (df['female'] == 0)][outcome].std() / np.sqrt(((df['ai_assist'] == 1) & (df['female'] == 0)).sum()),
    df[(df['ai_guided'] == 1) & (df['female'] == 0)][outcome].std() / np.sqrt(((df['ai_guided'] == 1) & (df['female'] == 0)).sum())
]

women_means = [
    df[(df['control'] == 1) & (df['female'] == 1)][outcome].mean(),
    df[(df['ai_assist'] == 1) & (df['female'] == 1)][outcome].mean(),
    df[(df['ai_guided'] == 1) & (df['female'] == 1)][outcome].mean()
]
women_ses = [
    df[(df['control'] == 1) & (df['female'] == 1)][outcome].std() / np.sqrt(((df['control'] == 1) & (df['female'] == 1)).sum()),
    df[(df['ai_assist'] == 1) & (df['female'] == 1)][outcome].std() / np.sqrt(((df['ai_assist'] == 1) & (df['female'] == 1)).sum()),
    df[(df['ai_guided'] == 1) & (df['female'] == 1)][outcome].std() / np.sqrt(((df['ai_guided'] == 1) & (df['female'] == 1)).sum())
]

bars1 = ax.bar(x - width/2, men_means, width, yerr=[1.96*se for se in men_ses],
               capsize=5, label='Men', color='#3498db', alpha=0.7, edgecolor='black')
bars2 = ax.bar(x + width/2, women_means, width, yerr=[1.96*se for se in women_ses],
               capsize=5, label='Women', color='#e74c3c', alpha=0.7, edgecolor='black')

ax.set_ylabel('Test Score', fontsize=14, fontweight='bold')
ax.set_xlabel('Treatment', fontsize=14, fontweight='bold')
ax.set_title('Treatment Effects by Gender\n(PAP Equation 2)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(treatments)
ax.legend(fontsize=12, loc='best')
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(output_dir / '02_treatment_by_gender.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: 02_treatment_by_gender.png")

# ============================================================================
# 3. GPA HETEROGENEITY
# ============================================================================
print("\n" + "="*80)
print("3. GPA HETEROGENEITY")
print("="*80)

model3 = smf.ols(f'{outcome} ~ ai_assist + ai_guided + highgpa + ai_assist:highgpa + ai_guided:highgpa',
                 data=df).fit(cov_type='HC3')
print(model3.summary())

# Visualization 3: Treatment Effects by GPA
fig, ax = plt.subplots(figsize=(12, 6))

lowgpa_means = [
    df[(df['control'] == 1) & (df['highgpa'] == 0)][outcome].mean(),
    df[(df['ai_assist'] == 1) & (df['highgpa'] == 0)][outcome].mean(),
    df[(df['ai_guided'] == 1) & (df['highgpa'] == 0)][outcome].mean()
]
lowgpa_ses = [
    df[(df['control'] == 1) & (df['highgpa'] == 0)][outcome].std() / np.sqrt(((df['control'] == 1) & (df['highgpa'] == 0)).sum()),
    df[(df['ai_assist'] == 1) & (df['highgpa'] == 0)][outcome].std() / np.sqrt(((df['ai_assist'] == 1) & (df['highgpa'] == 0)).sum()),
    df[(df['ai_guided'] == 1) & (df['highgpa'] == 0)][outcome].std() / np.sqrt(((df['ai_guided'] == 1) & (df['highgpa'] == 0)).sum())
]

highgpa_means = [
    df[(df['control'] == 1) & (df['highgpa'] == 1)][outcome].mean(),
    df[(df['ai_assist'] == 1) & (df['highgpa'] == 1)][outcome].mean(),
    df[(df['ai_guided'] == 1) & (df['highgpa'] == 1)][outcome].mean()
]
highgpa_ses = [
    df[(df['control'] == 1) & (df['highgpa'] == 1)][outcome].std() / np.sqrt(((df['control'] == 1) & (df['highgpa'] == 1)).sum()),
    df[(df['ai_assist'] == 1) & (df['highgpa'] == 1)][outcome].std() / np.sqrt(((df['ai_assist'] == 1) & (df['highgpa'] == 1)).sum()),
    df[(df['ai_guided'] == 1) & (df['highgpa'] == 1)][outcome].std() / np.sqrt(((df['ai_guided'] == 1) & (df['highgpa'] == 1)).sum())
]

bars1 = ax.bar(x - width/2, lowgpa_means, width, yerr=[1.96*se for se in lowgpa_ses],
               capsize=5, label='Low GPA (<70%)', color='#95a5a6', alpha=0.7, edgecolor='black')
bars2 = ax.bar(x + width/2, highgpa_means, width, yerr=[1.96*se for se in highgpa_ses],
               capsize=5, label='High GPA (≥70%)', color='#f39c12', alpha=0.7, edgecolor='black')

ax.set_ylabel('Test Score', fontsize=14, fontweight='bold')
ax.set_xlabel('Treatment', fontsize=14, fontweight='bold')
ax.set_title('Treatment Effects by GPA\n(Similar to PAP Equation 2)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(treatments)
ax.legend(fontsize=12, loc='best')
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(output_dir / '03_treatment_by_gpa.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: 03_treatment_by_gpa.png")

# ============================================================================
# 4. TRIPLE INTERACTIONS (Equation 3)
# ============================================================================
print("\n" + "="*80)
print("4. TRIPLE INTERACTIONS (Equation 3)")
print("="*80)

model4 = smf.ols(f'''{outcome} ~ ai_assist + ai_guided + female + highgpa +
                      ai_assist:female + ai_assist:highgpa +
                      ai_guided:female + ai_guided:highgpa +
                      ai_assist:female:highgpa + ai_guided:female:highgpa''',
                 data=df).fit(cov_type='HC3')
print(model4.summary())

# Visualization 4: Treatment Effects by Gender and GPA
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Treatment Effects by Gender and GPA\n(PAP Equation 3 - Triple Interactions)',
             fontsize=16, fontweight='bold', y=0.98)

subgroups = [
    ('Low GPA Men', (df['female'] == 0) & (df['highgpa'] == 0)),
    ('Low GPA Women', (df['female'] == 1) & (df['highgpa'] == 0)),
    ('High GPA Men', (df['female'] == 0) & (df['highgpa'] == 1)),
    ('High GPA Women', (df['female'] == 1) & (df['highgpa'] == 1))
]

colors_sub = ['#3498db', '#e74c3c', '#95a5a6', '#f39c12']

for idx, ((label, mask), color, ax) in enumerate(zip(subgroups, colors_sub, axes.flat)):
    means = [
        df[(df['control'] == 1) & mask][outcome].mean(),
        df[(df['ai_assist'] == 1) & mask][outcome].mean(),
        df[(df['ai_guided'] == 1) & mask][outcome].mean()
    ]
    ses = [
        df[(df['control'] == 1) & mask][outcome].std() / np.sqrt(((df['control'] == 1) & mask).sum()),
        df[(df['ai_assist'] == 1) & mask][outcome].std() / np.sqrt(((df['ai_assist'] == 1) & mask).sum()),
        df[(df['ai_guided'] == 1) & mask][outcome].std() / np.sqrt(((df['ai_guided'] == 1) & mask).sum())
    ]

    bars = ax.bar(treatments, means, yerr=[1.96*se for se in ses], capsize=5,
                  color=color, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Test Score', fontsize=11, fontweight='bold')
    ax.set_xlabel('Treatment', fontsize=11, fontweight='bold')
    ax.set_title(label, fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    n_vals = [((df['control'] == 1) & mask).sum(),
              ((df['ai_assist'] == 1) & mask).sum(),
              ((df['ai_guided'] == 1) & mask).sum()]
    for bar, n, mean in zip(bars, n_vals, means):
        ax.text(bar.get_x() + bar.get_width()/2., 0.5,
                f'n={n}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig(output_dir / '04_triple_interactions.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: 04_triple_interactions.png")

# ============================================================================
# 5. TOP/LOW SCORER ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("5. TOP/LOW SCORER ANALYSIS")
print("="*80)

print("\nTop Scorer Analysis (>10 correct):")
model_top = smf.ols('topscore ~ ai_assist + ai_guided', data=df).fit(cov_type='HC3')
print(model_top.summary())

print("\nLow Scorer Analysis (<5 correct):")
model_low = smf.ols('lowscore ~ ai_assist + ai_guided', data=df).fit(cov_type='HC3')
print(model_low.summary())

# Visualization 5: Top/Low Scorer Proportions
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Top scorers
top_props = [
    df[df['control'] == 1]['topscore'].mean(),
    df[df['ai_assist'] == 1]['topscore'].mean(),
    df[df['ai_guided'] == 1]['topscore'].mean()
]
top_ses = [
    np.sqrt(top_props[0] * (1 - top_props[0]) / (df['control'] == 1).sum()),
    np.sqrt(top_props[1] * (1 - top_props[1]) / (df['ai_assist'] == 1).sum()),
    np.sqrt(top_props[2] * (1 - top_props[2]) / (df['ai_guided'] == 1).sum())
]

bars1 = ax1.bar(treatments, top_props, yerr=[1.96*se for se in top_ses], capsize=10,
                color=['#2ecc71', '#27ae60', '#229954'], alpha=0.7, edgecolor='black')
ax1.set_ylabel('Proportion Top Scorers', fontsize=13, fontweight='bold')
ax1.set_xlabel('Treatment', fontsize=13, fontweight='bold')
ax1.set_title('Top Scorers (>10 correct)', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_ylim(0, 1)

for bar, prop in zip(bars1, top_props):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
             f'{prop:.2%}', ha='center', va='bottom', fontweight='bold')

# Low scorers
low_props = [
    df[df['control'] == 1]['lowscore'].mean(),
    df[df['ai_assist'] == 1]['lowscore'].mean(),
    df[df['ai_guided'] == 1]['lowscore'].mean()
]
low_ses = [
    np.sqrt(low_props[0] * (1 - low_props[0]) / (df['control'] == 1).sum()),
    np.sqrt(low_props[1] * (1 - low_props[1]) / (df['ai_assist'] == 1).sum()),
    np.sqrt(low_props[2] * (1 - low_props[2]) / (df['ai_guided'] == 1).sum())
]

bars2 = ax2.bar(treatments, low_props, yerr=[1.96*se for se in low_ses], capsize=10,
                color=['#e74c3c', '#c0392b', '#a93226'], alpha=0.7, edgecolor='black')
ax2.set_ylabel('Proportion Low Scorers', fontsize=13, fontweight='bold')
ax2.set_xlabel('Treatment', fontsize=13, fontweight='bold')
ax2.set_title('Low Scorers (<5 correct)', fontsize=14, fontweight='bold')
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.set_ylim(0, 1)

for bar, prop in zip(bars2, low_props):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
             f'{prop:.2%}', ha='center', va='bottom', fontweight='bold')

plt.suptitle('Distribution of Performance Extremes by Treatment',
             fontsize=15, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig(output_dir / '05_top_low_scorers.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: 05_top_low_scorers.png")

# ============================================================================
# 6. STAGE 2 PERFORMANCE
# ============================================================================
print("\n" + "="*80)
print("6. STAGE 2 PERFORMANCE")
print("="*80)

print("\nNumber of Practice Questions:")
model_npq = smf.ols('nb_practice_questions ~ ai_assist + ai_guided', data=df).fit(cov_type='HC3')
print(model_npq.summary())

print("\nNumber Correct in Practice:")
model_correct = smf.ols('co_practice_questions ~ ai_assist + ai_guided', data=df).fit(cov_type='HC3')
print(model_correct.summary())

# Visualization 6: Stage 2 Performance
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

npq_means = [
    df[df['control'] == 1]['nb_practice_questions'].mean(),
    df[df['ai_assist'] == 1]['nb_practice_questions'].mean(),
    df[df['ai_guided'] == 1]['nb_practice_questions'].mean()
]
npq_ses = [
    df[df['control'] == 1]['nb_practice_questions'].std() / np.sqrt((df['control'] == 1).sum()),
    df[df['ai_assist'] == 1]['nb_practice_questions'].std() / np.sqrt((df['ai_assist'] == 1).sum()),
    df[df['ai_guided'] == 1]['nb_practice_questions'].std() / np.sqrt((df['ai_guided'] == 1).sum())
]

bars1 = axes[0].bar(treatments, npq_means, yerr=[1.96*se for se in npq_ses], capsize=10,
                     color=['#9b59b6', '#8e44ad', '#7d3c98'], alpha=0.7, edgecolor='black')
axes[0].set_ylabel('Number of Questions', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Treatment', fontsize=13, fontweight='bold')
axes[0].set_title('Practice Questions Attempted', fontsize=14, fontweight='bold')
axes[0].grid(axis='y', alpha=0.3, linestyle='--')

for bar, mean in zip(bars1, npq_means):
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{mean:.1f}', ha='center', va='bottom', fontweight='bold')

correct_means = [
    df[df['control'] == 1]['co_practice_questions'].mean(),
    df[df['ai_assist'] == 1]['co_practice_questions'].mean(),
    df[df['ai_guided'] == 1]['co_practice_questions'].mean()
]
correct_ses = [
    df[df['control'] == 1]['co_practice_questions'].std() / np.sqrt((df['control'] == 1).sum()),
    df[df['ai_assist'] == 1]['co_practice_questions'].std() / np.sqrt((df['ai_assist'] == 1).sum()),
    df[df['ai_guided'] == 1]['co_practice_questions'].std() / np.sqrt((df['ai_guided'] == 1).sum())
]

bars2 = axes[1].bar(treatments, correct_means, yerr=[1.96*se for se in correct_ses], capsize=10,
                     color=['#16a085', '#138d75', '#117a65'], alpha=0.7, edgecolor='black')
axes[1].set_ylabel('Number Correct', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Treatment', fontsize=13, fontweight='bold')
axes[1].set_title('Practice Questions Correct', fontsize=14, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3, linestyle='--')

for bar, mean in zip(bars2, correct_means):
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{mean:.1f}', ha='center', va='bottom', fontweight='bold')

plt.suptitle('Stage 2 Performance: Practice Questions',
             fontsize=15, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig(output_dir / '06_stage2_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: 06_stage2_performance.png")

# ============================================================================
# 7. MECHANISM ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("7. MECHANISM ANALYSIS")
print("="*80)

mechanisms = {
    'Complement vs. Substitute': 'index_complement',
    'Confidence': 'index_confidence',
    'Cheating Perceptions': 'index_cheating',
    'Motivation': 'index_motivation'
}

for name, var in mechanisms.items():
    if var in df.columns:
        print(f"\n{name}:")
        model = smf.ols(f'{var} ~ ai_assist + ai_guided', data=df).fit(cov_type='HC3')
        print(model.summary())

# Visualization 7: Mechanism Indices
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle('Mechanism Analysis: Summary Indices by Treatment\n(PAP Section 6)',
             fontsize=16, fontweight='bold', y=0.995)

colors_mech = ['#3498db', '#e74c3c', '#2ecc71']

for idx, (name, var) in enumerate(mechanisms.items()):
    if var not in df.columns:
        continue

    ax = axes.flat[idx]

    means = [
        df[df['control'] == 1][var].mean(),
        df[df['ai_assist'] == 1][var].mean(),
        df[df['ai_guided'] == 1][var].mean()
    ]
    ses = [
        df[df['control'] == 1][var].std() / np.sqrt((df['control'] == 1).sum()),
        df[df['ai_assist'] == 1][var].std() / np.sqrt((df['ai_assist'] == 1).sum()),
        df[df['ai_guided'] == 1][var].std() / np.sqrt((df['ai_guided'] == 1).sum())
    ]

    bars = ax.bar(treatments, means, yerr=[1.96*se for se in ses], capsize=8,
                  color=colors_mech, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Index Value', fontsize=12, fontweight='bold')
    ax.set_xlabel('Treatment', fontsize=12, fontweight='bold')
    ax.set_title(name, fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    for bar, mean in zip(bars, means):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{mean:.3f}', ha='center',
                va='bottom' if height > 0 else 'top', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig(output_dir / '07_mechanism_indices.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: 07_mechanism_indices.png")

# ============================================================================
# 8. TEST SCORE DISTRIBUTIONS
# ============================================================================
print("\n" + "="*80)
print("8. TEST SCORE DISTRIBUTIONS")
print("="*80)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for idx, (treatment, label, color) in enumerate(zip(['control', 'ai_assist', 'ai_guided'],
                                                     treatments,
                                                     colors_main)):
    data = df[df[treatment] == 1][outcome]
    axes[idx].hist(data, bins=15, color=color, alpha=0.7, edgecolor='black')
    axes[idx].axvline(data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {data.mean():.2f}')
    axes[idx].set_xlabel('Test Score', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('Frequency', fontsize=12, fontweight='bold')
    axes[idx].set_title(label, fontsize=13, fontweight='bold')
    axes[idx].legend()
    axes[idx].grid(axis='y', alpha=0.3, linestyle='--')

plt.suptitle('Distribution of Test Scores by Treatment', fontsize=15, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig(output_dir / '08_score_distributions.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: 08_score_distributions.png")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"\nAll visualizations saved to: {output_dir}")
print("\nGenerated visualizations:")
viz_files = sorted(output_dir.glob('*.png'))
for i, f in enumerate(viz_files, 1):
    print(f"  {i}. {f.name}")
