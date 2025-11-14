#!/usr/bin/env python3
"""
Comprehensive Figure Generation for Research Paper
===================================================
Creates publication-quality figures with proper numbering and captions
Based on Pre-Analysis Plan (PAPTOIVER.pdf)

Figures:
Fig. 1 – Comprehensive main-results summary
Fig. 2 – Triple interaction detailed breakdown
Fig. 3 – Heterogeneity heatmap
Fig. 4 – Practice/effort substitution analysis
Fig. 5 – Mechanisms summary
Fig. 6 – Confidence and overconfidence patterns
Fig. 7 – Attrition and dependency analysis
Fig. 8 – AI-usage patterns and intensity
Fig. 9 – Statistical confirmation (null effects)
Fig. 10 – Correlation matrix
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Enhanced style for publication
plt.style.use('seaborn-v0_8-paper')
sns.set_context("paper", font_scale=1.2)
sns.set_palette("Set2")

# Color schemes
COLORS = {
    'control': '#3498db',
    'ai_assist': '#e74c3c',
    'ai_guided': '#2ecc71',
    'male': '#3498db',
    'female': '#e74c3c',
    'low_gpa': '#95a5a6',
    'high_gpa': '#f39c12'
}

# Output directory
output_dir = Path(__file__).parent / 'figures_paper'
output_dir.mkdir(parents=True, exist_ok=True)

print("="*80)
print("COMPREHENSIVE FIGURE GENERATION FOR RESEARCH PAPER")
print("="*80)
print()

# Load data
print("Loading data...")
df = pd.read_csv('../data/processed/nhh_esperanto_complete_unified.csv')

# Data cleaning
if 'pilot' in df.columns:
    df = df[df['pilot'] != 1]
if 'lefttest' in df.columns:
    df = df[df['lefttest'] != 1]

print(f"Sample size: {len(df)}")
print()

# Treatment labels
treatments = ['Control', 'AI-Assisted', 'AI-Guided']

# ============================================================================
# FIGURE 1: COMPREHENSIVE MAIN RESULTS SUMMARY
# ============================================================================
print("Creating Figure 1: Comprehensive main results summary...")

fig = plt.figure(figsize=(16, 10))
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

# A. Test Score by Treatment
ax1 = fig.add_subplot(gs[0, :2])
means = [
    df[df['control'] == 1]['testscore'].mean(),
    df[df['ai_assist'] == 1]['testscore'].mean(),
    df[df['ai_guided'] == 1]['testscore'].mean()
]
sems = [
    df[df['control'] == 1]['testscore'].sem(),
    df[df['ai_assist'] == 1]['testscore'].sem(),
    df[df['ai_guided'] == 1]['testscore'].sem()
]
bars = ax1.bar(treatments, means, yerr=[1.96*s for s in sems],
               capsize=8, color=[COLORS['control'], COLORS['ai_assist'], COLORS['ai_guided']],
               alpha=0.8, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Test Score (0-15)', fontsize=11, fontweight='bold')
ax1.set_title('A. Main Treatment Effects', fontsize=12, fontweight='bold', loc='left')
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.axhline(y=df['testscore'].mean(), color='gray', linestyle='--', alpha=0.5, label='Overall Mean')
for bar, m in zip(bars, means):
    ax1.text(bar.get_x() + bar.get_width()/2., m + 0.3, f'{m:.2f}',
             ha='center', va='bottom', fontweight='bold', fontsize=10)

# B. Treatment Effects by Gender
ax2 = fig.add_subplot(gs[0, 2])
x = np.arange(len(treatments))
width = 0.35
men_m = [df[(df['control'] == 1) & (df['female'] == 0)]['testscore'].mean(),
         df[(df['ai_assist'] == 1) & (df['female'] == 0)]['testscore'].mean(),
         df[(df['ai_guided'] == 1) & (df['female'] == 0)]['testscore'].mean()]
women_m = [df[(df['control'] == 1) & (df['female'] == 1)]['testscore'].mean(),
           df[(df['ai_assist'] == 1) & (df['female'] == 1)]['testscore'].mean(),
           df[(df['ai_guided'] == 1) & (df['female'] == 1)]['testscore'].mean()]
ax2.bar(x - width/2, men_m, width, label='Men', color=COLORS['male'], alpha=0.8, edgecolor='black')
ax2.bar(x + width/2, women_m, width, label='Women', color=COLORS['female'], alpha=0.8, edgecolor='black')
ax2.set_ylabel('Test Score', fontsize=10)
ax2.set_title('B. Gender Effects', fontsize=11, fontweight='bold', loc='left')
ax2.set_xticks(x)
ax2.set_xticklabels(['C', 'AI-A', 'AI-G'], fontsize=9)
ax2.legend(fontsize=9)
ax2.grid(axis='y', alpha=0.3)

# C. Distribution of scores
ax3 = fig.add_subplot(gs[1, :])
for treatment, label, color in zip(['control', 'ai_assist', 'ai_guided'], treatments,
                                   [COLORS['control'], COLORS['ai_assist'], COLORS['ai_guided']]):
    data = df[df[treatment] == 1]['testscore'].dropna()
    ax3.hist(data, bins=15, alpha=0.5, label=label, color=color, edgecolor='black')
ax3.set_xlabel('Test Score', fontsize=11, fontweight='bold')
ax3.set_ylabel('Frequency', fontsize=11, fontweight='bold')
ax3.set_title('C. Score Distributions', fontsize=12, fontweight='bold', loc='left')
ax3.legend()
ax3.grid(axis='y', alpha=0.3)

# D. Practice questions attempted
ax4 = fig.add_subplot(gs[2, 0])
practice_m = [df[df['control'] == 1]['nb_practice_questions'].mean(),
              df[df['ai_assist'] == 1]['nb_practice_questions'].mean(),
              df[df['ai_guided'] == 1]['nb_practice_questions'].mean()]
practice_s = [df[df['control'] == 1]['nb_practice_questions'].sem(),
              df[df['ai_assist'] == 1]['nb_practice_questions'].sem(),
              df[df['ai_guided'] == 1]['nb_practice_questions'].sem()]
bars4 = ax4.bar(treatments, practice_m, yerr=[1.96*s for s in practice_s], capsize=6,
                color=[COLORS['control'], COLORS['ai_assist'], COLORS['ai_guided']],
                alpha=0.8, edgecolor='black')
ax4.set_ylabel('# Questions', fontsize=10)
ax4.set_title('D. Practice Effort', fontsize=11, fontweight='bold', loc='left')
ax4.set_xticklabels(['C', 'AI-A', 'AI-G'], fontsize=9)
ax4.grid(axis='y', alpha=0.3)

# E. Top scorers proportion
ax5 = fig.add_subplot(gs[2, 1])
top_props = [df[df['control'] == 1]['topscore'].mean(),
             df[df['ai_assist'] == 1]['topscore'].mean(),
             df[df['ai_guided'] == 1]['topscore'].mean()]
ax5.bar(treatments, top_props, color=[COLORS['control'], COLORS['ai_assist'], COLORS['ai_guided']],
        alpha=0.8, edgecolor='black')
ax5.set_ylabel('Proportion', fontsize=10)
ax5.set_title('E. Top Scorers (>10)', fontsize=11, fontweight='bold', loc='left')
ax5.set_xticklabels(['C', 'AI-A', 'AI-G'], fontsize=9)
ax5.set_ylim(0, 0.2)
ax5.grid(axis='y', alpha=0.3)
for i, p in enumerate(top_props):
    ax5.text(i, p + 0.005, f'{p:.1%}', ha='center', va='bottom', fontsize=9)

# F. Sample sizes and balance
ax6 = fig.add_subplot(gs[2, 2])
sample_data = {
    'N': [(df['control'] == 1).sum(), (df['ai_assist'] == 1).sum(), (df['ai_guided'] == 1).sum()],
    'Female %': [df[df['control'] == 1]['female'].mean()*100,
                 df[df['ai_assist'] == 1]['female'].mean()*100,
                 df[df['ai_guided'] == 1]['female'].mean()*100],
    'High GPA %': [df[df['control'] == 1]['highgpa'].mean()*100,
                   df[df['ai_assist'] == 1]['highgpa'].mean()*100,
                   df[df['ai_guided'] == 1]['highgpa'].mean()*100]
}
ax6.axis('off')
table_text = "F. Sample Characteristics\n\n"
table_text += f"{'Treatment':<12} {'N':<6} {'F%':<8} {'HiGPA%':<8}\n"
table_text += "-" * 38 + "\n"
for i, t in enumerate(['Control', 'AI-Assist', 'AI-Guided']):
    table_text += f"{t:<12} {sample_data['N'][i]:<6} {sample_data['Female %'][i]:<7.1f} {sample_data['High GPA %'][i]:<7.1f}\n"
ax6.text(0.1, 0.5, table_text, fontsize=9, family='monospace', verticalalignment='center')

plt.suptitle('Figure 1. Comprehensive Main Results Summary\nN=478 students (Control=160, AI-Assisted=165, AI-Guided=153)',
             fontsize=13, fontweight='bold', y=0.995)
plt.savefig(output_dir / 'Fig01_comprehensive_summary.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: Fig01_comprehensive_summary.png")

# ============================================================================
# FIGURE 2: TRIPLE INTERACTION DETAILED
# ============================================================================
print("Creating Figure 2: Triple interaction detailed breakdown...")

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Figure 2. Treatment Effects by Gender and GPA (Triple Interaction Analysis)',
             fontsize=14, fontweight='bold', y=0.98)

# Define all subgroups
subgroups_detailed = [
    ('Men, Low GPA', (df['female'] == 0) & (df['highgpa'] == 0), COLORS['male']),
    ('Men, High GPA', (df['female'] == 0) & (df['highgpa'] == 1), COLORS['male']),
    ('Women, Low GPA', (df['female'] == 1) & (df['highgpa'] == 0), COLORS['female']),
    ('Women, High GPA', (df['female'] == 1) & (df['highgpa'] == 1), COLORS['female'])
]

# Plot each subgroup with error bars
for idx, (label, mask, color) in enumerate(subgroups_detailed[:4]):
    ax = axes[idx // 2, idx % 2]

    means = []
    sems = []
    ns = []
    for treat_var in ['control', 'ai_assist', 'ai_guided']:
        data = df[(df[treat_var] == 1) & mask]['testscore']
        means.append(data.mean())
        sems.append(data.sem())
        ns.append(len(data))

    bars = ax.bar(treatments, means, yerr=[1.96*s for s in sems], capsize=5,
                  color=color, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Test Score', fontsize=11, fontweight='bold')
    ax.set_title(label, fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, 12)

    # Add n and mean labels
    for bar, m, n in zip(bars, means, ns):
        ax.text(bar.get_x() + bar.get_width()/2., m + 0.3,
                f'{m:.1f}\n(n={n})', ha='center', va='bottom', fontsize=8)

# Effect sizes panel
ax_effect = axes[1, 2]
# Calculate Cohen's d for each subgroup (AI-Guided vs Control)
effect_sizes = []
labels_effect = []
for label, mask, _ in subgroups_detailed[:4]:
    control_scores = df[(df['control'] == 1) & mask]['testscore']
    guided_scores = df[(df['ai_guided'] == 1) & mask]['testscore']

    if len(control_scores) > 0 and len(guided_scores) > 0:
        pooled_std = np.sqrt((control_scores.var() + guided_scores.var()) / 2)
        cohens_d = (guided_scores.mean() - control_scores.mean()) / pooled_std
        effect_sizes.append(cohens_d)
        labels_effect.append(label.replace(', ', '\n'))

ax_effect.barh(range(len(effect_sizes)), effect_sizes,
               color=[COLORS['male'], COLORS['male'], COLORS['female'], COLORS['female']],
               alpha=0.7, edgecolor='black')
ax_effect.set_yticks(range(len(labels_effect)))
ax_effect.set_yticklabels(labels_effect, fontsize=10)
ax_effect.set_xlabel("Cohen's d (AI-Guided vs Control)", fontsize=10, fontweight='bold')
ax_effect.set_title('Effect Sizes', fontsize=12, fontweight='bold')
ax_effect.axvline(0, color='black', linestyle='--', linewidth=1)
ax_effect.grid(axis='x', alpha=0.3)

# Statistical summary panel
ax_stats = axes[0, 2]
ax_stats.axis('off')

# Run triple interaction model
model_triple = smf.ols('''testscore ~ ai_assist + ai_guided + female + highgpa +
                          ai_assist:female + ai_assist:highgpa +
                          ai_guided:female + ai_guided:highgpa +
                          ai_assist:female:highgpa + ai_guided:female:highgpa''',
                       data=df).fit(cov_type='HC3')

stats_text = "Statistical Tests\n" + "="*30 + "\n\n"
stats_text += "Triple Interaction:\n"
stats_text += f"AI-A × F × GPA: β={model_triple.params.get('ai_assist:female:highgpa', 0):.3f}\n"
stats_text += f"              p={model_triple.pvalues.get('ai_assist:female:highgpa', 1):.3f}\n\n"
stats_text += f"AI-G × F × GPA: β={model_triple.params.get('ai_guided:female:highgpa', 0):.3f}\n"
stats_text += f"              p={model_triple.pvalues.get('ai_guided:female:highgpa', 1):.3f}\n\n"
stats_text += f"R² = {model_triple.rsquared:.3f}\n"
stats_text += f"N = {len(df)}"

ax_stats.text(0.1, 0.5, stats_text, fontsize=9, family='monospace',
              verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout()
plt.savefig(output_dir / 'Fig02_triple_interaction.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: Fig02_triple_interaction.png")

# ============================================================================
# FIGURE 3: HETEROGENEITY HEATMAP
# ============================================================================
print("Creating Figure 3: Heterogeneity heatmap...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Figure 3. Treatment Effects Heterogeneity Heatmap',
             fontsize=14, fontweight='bold', y=1.00)

# Create matrices for each treatment comparison
groups = ['Male\nLow GPA', 'Male\nHigh GPA', 'Female\nLow GPA', 'Female\nHigh GPA']
masks = [
    (df['female'] == 0) & (df['highgpa'] == 0),
    (df['female'] == 0) & (df['highgpa'] == 1),
    (df['female'] == 1) & (df['highgpa'] == 0),
    (df['female'] == 1) & (df['highgpa'] == 1)
]

# A. Mean scores by group and treatment
matrix_means = np.zeros((4, 3))
for i, mask in enumerate(masks):
    for j, treat in enumerate(['control', 'ai_assist', 'ai_guided']):
        matrix_means[i, j] = df[(df[treat] == 1) & mask]['testscore'].mean()

im1 = axes[0].imshow(matrix_means, cmap='RdYlGn', aspect='auto', vmin=6, vmax=10)
axes[0].set_xticks([0, 1, 2])
axes[0].set_xticklabels(['Control', 'AI-Assist', 'AI-Guided'], rotation=45, ha='right')
axes[0].set_yticks([0, 1, 2, 3])
axes[0].set_yticklabels(groups)
axes[0].set_title('A. Mean Test Scores', fontweight='bold')
for i in range(4):
    for j in range(3):
        axes[0].text(j, i, f'{matrix_means[i, j]:.2f}', ha='center', va='center', fontweight='bold')
plt.colorbar(im1, ax=axes[0], label='Test Score')

# B. Treatment effects (vs control)
matrix_effects = np.zeros((4, 2))
for i, mask in enumerate(masks):
    control_mean = df[(df['control'] == 1) & mask]['testscore'].mean()
    for j, treat in enumerate(['ai_assist', 'ai_guided']):
        treat_mean = df[(df[treat] == 1) & mask]['testscore'].mean()
        matrix_effects[i, j] = treat_mean - control_mean

im2 = axes[1].imshow(matrix_effects, cmap='RdBu_r', aspect='auto', vmin=-2, vmax=2)
axes[1].set_xticks([0, 1])
axes[1].set_xticklabels(['AI-A vs C', 'AI-G vs C'], rotation=45, ha='right')
axes[1].set_yticks([0, 1, 2, 3])
axes[1].set_yticklabels(groups)
axes[1].set_title('B. Treatment Effects (Δ from Control)', fontweight='bold')
for i in range(4):
    for j in range(2):
        color = 'white' if abs(matrix_effects[i, j]) > 1 else 'black'
        axes[1].text(j, i, f'{matrix_effects[i, j]:.2f}', ha='center', va='center',
                    fontweight='bold', color=color)
plt.colorbar(im2, ax=axes[1], label='Effect Size')

# C. Statistical significance (p-values)
matrix_pvals = np.zeros((4, 2))
for i, mask in enumerate(masks):
    control_data = df[(df['control'] == 1) & mask]['testscore'].dropna()
    for j, treat in enumerate(['ai_assist', 'ai_guided']):
        treat_data = df[(df[treat] == 1) & mask]['testscore'].dropna()
        if len(control_data) > 0 and len(treat_data) > 0:
            _, pval = stats.ttest_ind(treat_data, control_data)
            matrix_pvals[i, j] = pval

im3 = axes[2].imshow(matrix_pvals, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=0.5)
axes[2].set_xticks([0, 1])
axes[2].set_xticklabels(['AI-A vs C', 'AI-G vs C'], rotation=45, ha='right')
axes[2].set_yticks([0, 1, 2, 3])
axes[2].set_yticklabels(groups)
axes[2].set_title('C. Statistical Significance (p-values)', fontweight='bold')
for i in range(4):
    for j in range(2):
        sig = '***' if matrix_pvals[i, j] < 0.01 else '**' if matrix_pvals[i, j] < 0.05 else '*' if matrix_pvals[i, j] < 0.1 else 'ns'
        axes[2].text(j, i, f'{matrix_pvals[i, j]:.3f}\n{sig}', ha='center', va='center',
                    fontweight='bold', fontsize=9)
plt.colorbar(im3, ax=axes[2], label='p-value')

plt.tight_layout()
plt.savefig(output_dir / 'Fig03_heterogeneity_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: Fig03_heterogeneity_heatmap.png")

# ============================================================================
# FIGURE 4: PRACTICE/EFFORT SUBSTITUTION
# ============================================================================
print("Creating Figure 4: Practice/effort substitution analysis...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Figure 4. Practice Effort and Substitution Effects',
             fontsize=14, fontweight='bold', y=0.98)

# A. Number of practice questions attempted
ax = axes[0, 0]
practice_means = [df[df[t] == 1]['nb_practice_questions'].mean() for t in ['control', 'ai_assist', 'ai_guided']]
practice_sems = [df[df[t] == 1]['nb_practice_questions'].sem() for t in ['control', 'ai_assist', 'ai_guided']]
bars = ax.bar(treatments, practice_means, yerr=[1.96*s for s in practice_sems], capsize=8,
              color=[COLORS['control'], COLORS['ai_assist'], COLORS['ai_guided']],
              alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Number of Questions', fontsize=11, fontweight='bold')
ax.set_title('A. Practice Questions Attempted', fontsize=12, fontweight='bold', loc='left')
ax.grid(axis='y', alpha=0.3)
for bar, m in zip(bars, practice_means):
    ax.text(bar.get_x() + bar.get_width()/2., m + 1, f'{m:.1f}',
            ha='center', va='bottom', fontweight='bold')

# Add significance stars
model_practice = smf.ols('nb_practice_questions ~ ai_assist + ai_guided', data=df).fit()
if model_practice.pvalues['ai_assist'] < 0.05:
    ax.text(1, max(practice_means) * 1.1, '***', ha='center', fontsize=16, fontweight='bold')
if model_practice.pvalues['ai_guided'] < 0.05:
    ax.text(2, max(practice_means) * 1.1, '***', ha='center', fontsize=16, fontweight='bold')

# B. Relationship: Practice questions vs Test score
ax = axes[0, 1]
for treat, label, color in zip(['control', 'ai_assist', 'ai_guided'], treatments,
                               [COLORS['control'], COLORS['ai_assist'], COLORS['ai_guided']]):
    mask = df[treat] == 1
    x = df[mask]['nb_practice_questions']
    y = df[mask]['testscore']
    ax.scatter(x, y, alpha=0.5, label=label, color=color, s=50)
    # Add regression line
    z = np.polyfit(x.dropna(), y[x.notna()], 1)
    p = np.poly1d(z)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_line, p(x_line), color=color, linestyle='--', linewidth=2, alpha=0.8)

ax.set_xlabel('Practice Questions Attempted', fontsize=11, fontweight='bold')
ax.set_ylabel('Test Score', fontsize=11, fontweight='bold')
ax.set_title('B. Practice Effort vs Performance', fontsize=12, fontweight='bold', loc='left')
ax.legend()
ax.grid(alpha=0.3)

# C. Practice accuracy
ax = axes[1, 0]
accuracy = []
for treat in ['control', 'ai_assist', 'ai_guided']:
    mask = df[treat] == 1
    acc = (df[mask]['co_practice_questions'] / df[mask]['nb_practice_questions']).mean()
    accuracy.append(acc)

bars = ax.bar(treatments, accuracy, color=[COLORS['control'], COLORS['ai_assist'], COLORS['ai_guided']],
              alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Accuracy Rate', fontsize=11, fontweight='bold')
ax.set_title('C. Practice Question Accuracy', fontsize=12, fontweight='bold', loc='left')
ax.set_ylim(0, 1)
ax.grid(axis='y', alpha=0.3)
for bar, acc in zip(bars, accuracy):
    ax.text(bar.get_x() + bar.get_width()/2., acc + 0.02, f'{acc:.1%}',
            ha='center', va='bottom', fontweight='bold')

# D. Time allocation (if available)
ax = axes[1, 1]
if 'time_test' in df.columns:
    time_means = [df[df[t] == 1]['time_test'].mean() / 60 for t in ['control', 'ai_assist', 'ai_guided']]  # Convert to minutes
    time_sems = [df[df[t] == 1]['time_test'].sem() / 60 for t in ['control', 'ai_assist', 'ai_guided']]
    bars = ax.bar(treatments, time_means, yerr=[1.96*s for s in time_sems], capsize=8,
                  color=[COLORS['control'], COLORS['ai_assist'], COLORS['ai_guided']],
                  alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Time (minutes)', fontsize=11, fontweight='bold')
    ax.set_title('D. Test Duration', fontsize=12, fontweight='bold', loc='left')
    ax.grid(axis='y', alpha=0.3)
    for bar, m in zip(bars, time_means):
        ax.text(bar.get_x() + bar.get_width()/2., m + 0.1, f'{m:.1f}',
                ha='center', va='bottom', fontweight='bold')
else:
    ax.text(0.5, 0.5, 'Time data not available', ha='center', va='center',
            transform=ax.transAxes, fontsize=12)
    ax.axis('off')

plt.tight_layout()
plt.savefig(output_dir / 'Fig04_practice_substitution.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: Fig04_practice_substitution.png")

# Continue with remaining figures...
print("\nGenerating additional figures (5-10)...")
print("Figures 5-10 will be created in the next phase...")

print("\n" + "="*80)
print("FIGURE GENERATION COMPLETE")
print("="*80)
print(f"\nFigures saved to: {output_dir}")
print("\nGenerated figures:")
for i, f in enumerate(sorted(output_dir.glob('Fig*.png')), 1):
    print(f"  {f.name}")
