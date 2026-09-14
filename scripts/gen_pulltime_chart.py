import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ── Data (means and standard deviations, outliers removed) ──
labels = ['Node Single Stage', 'Node-Alpine Multi', 'Alpine Multi']
means  = [20990.66, 5421.79, 4921.00]
stds   = [980.20, 263.98, 125.37]

# ── IEEE-compliant styling ──
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 8,
    'axes.linewidth': 0.6,
    'figure.dpi': 600,
})

# Single-column IEEE width ~3.5 inches
fig, ax = plt.subplots(figsize=(3.5, 2.2))

y_pos = np.arange(len(labels))

# Grayscale-safe shades (print B&W friendly)
colors = ['#4d4d4d', '#999999', '#cccccc']

bars = ax.barh(
    y_pos, means, xerr=stds,
    color=colors, edgecolor='black', linewidth=0.6,
    error_kw={'elinewidth': 0.8, 'capsize': 3, 'capthick': 0.8},
    height=0.6
)

# Value labels at end of each bar
for i, (m, s) in enumerate(zip(means, stds)):
    ax.text(m + s + 600, i, f'{m:,.0f}',
            va='center', ha='left', fontsize=7)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=8)
ax.invert_yaxis()  # first item on top
ax.set_xlabel('Mean Pull Time (ms)', fontsize=8)
ax.set_xlim(0, 25000)

# Clean spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=7, length=3, width=0.6)

# Light x grid only
ax.xaxis.grid(True, linestyle=':', linewidth=0.4, color='gray', alpha=0.6)
ax.set_axisbelow(True)

plt.tight_layout(pad=0.3)
plt.savefig('fig1_pull_time.png', dpi=600, bbox_inches='tight')
plt.savefig('fig1_pull_time.pdf', bbox_inches='tight')
print("Saved fig1_pull_time.png and fig1_pull_time.pdf")
