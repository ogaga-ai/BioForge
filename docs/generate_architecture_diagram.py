"""
BioForge System Architecture Diagram Generator
-----------------------------------------------
Generates a publication-quality block diagram of the BioForge platform
architecture for use in technical documentation and NIW petition exhibits.

Run: python docs/generate_architecture_diagram.py
Output: outputs/figures/BioForge_Architecture.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

BLUE      = '#1a4d8f'
LIGHTBLUE = '#4a90d9'
GREEN     = '#2e7d32'
LIGHTGR   = '#66bb6a'
ORANGE    = '#e65100'
LIGHTOR   = '#ffa726'
GRAY      = '#455a64'
LIGHTGRAY = '#eceff1'
WHITE     = '#ffffff'


def draw_box(ax, x, y, w, h, label, sublabel='', color=BLUE, text_color=WHITE, fontsize=9):
    box = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle='round,pad=0.02',
        facecolor=color, edgecolor=WHITE, linewidth=1.5, zorder=3
    )
    ax.add_patch(box)
    if sublabel:
        ax.text(x, y + 0.025, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=text_color, zorder=4)
        ax.text(x, y - 0.035, sublabel, ha='center', va='center',
                fontsize=fontsize - 1.5, color=text_color, zorder=4, style='italic')
    else:
        ax.text(x, y, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=text_color, zorder=4)


def draw_arrow(ax, x1, y1, x2, y2, label='', color=GRAY):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5), zorder=2)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.01, my, label, fontsize=7, color=GRAY, ha='left', va='center')


fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
fig.patch.set_facecolor(LIGHTGRAY)
ax.set_facecolor(LIGHTGRAY)

# ── Title ──────────────────────────────────────────────────────────────
ax.text(0.5, 0.97, 'BioForge Platform Architecture', ha='center', va='top',
        fontsize=16, fontweight='bold', color=BLUE)
ax.text(0.5, 0.935, 'Integrated DOE + ML Bioprocess Optimization Framework  |  v0.1',
        ha='center', va='top', fontsize=10, color=GRAY)

# ── Layer 1: Input ─────────────────────────────────────────────────────
ax.text(0.08, 0.875, 'INPUT LAYER', fontsize=8, color=GRAY, fontweight='bold', va='center')
inputs = [
    (0.20, 0.835, 'Waste Stream\nComposition'),
    (0.38, 0.835, 'Target Product\n& Constraints'),
    (0.56, 0.835, 'Operating\nBoundaries'),
    (0.74, 0.835, 'Scale Target\n(lab/pilot/plant)'),
]
for x, y, lbl in inputs:
    draw_box(ax, x, y, 0.155, 0.07, lbl, color=LIGHTBLUE, fontsize=8)

# ── Layer 2: DOE Engine ────────────────────────────────────────────────
ax.text(0.08, 0.735, 'MODULE 1', fontsize=8, color=GRAY, fontweight='bold', va='center')
draw_box(ax, 0.47, 0.72, 0.72, 0.075,
         'DOE ENGINE', 'Box-Behnken Design  |  Central Composite Design  |  Factorial Design',
         color=BLUE, fontsize=9)

for x, _, _ in inputs:
    draw_arrow(ax, x, 0.80, 0.47, 0.757, color=LIGHTBLUE)

# ── Layer 3: ML Modeling ───────────────────────────────────────────────
ax.text(0.08, 0.635, 'MODULE 2', fontsize=8, color=GRAY, fontweight='bold', va='center')
ml_models = [
    (0.20, 0.615, 'ANN', '(tanh, MFFF-IBP)'),
    (0.38, 0.615, 'Random Forest', '(n=200)'),
    (0.56, 0.615, 'Gradient\nBoosting', ''),
    (0.74, 0.615, 'SVR (RBF)', ''),
]
for x, y, lbl, sub in ml_models:
    draw_box(ax, x, y, 0.155, 0.07, lbl, sub, color=GREEN, fontsize=8)

draw_arrow(ax, 0.47, 0.682, 0.47, 0.650, color=BLUE)
for x, _, _, _ in ml_models[1:]:
    draw_arrow(ax, 0.47, 0.682, x, 0.650, color=BLUE)

# ── Layer 4: Sensitivity + Optimisation ───────────────────────────────
ax.text(0.08, 0.520, 'MODULE 2\n(cont.)', fontsize=8, color=GRAY, fontweight='bold', va='center')
draw_box(ax, 0.32, 0.505, 0.35, 0.07,
         'SENSITIVITY ANALYSIS', 'Sobol / Permutation Importance', color=GREEN, fontsize=8)
draw_box(ax, 0.68, 0.505, 0.35, 0.07,
         'YIELD OPTIMISATION', 'Grid Search | Genetic Algorithm', color=GREEN, fontsize=8)

for x, _, _, _ in ml_models:
    draw_arrow(ax, x, 0.58, 0.32 if x < 0.5 else 0.68, 0.542, color=LIGHTGR)

# ── Layer 5: Separation Module ────────────────────────────────────────
ax.text(0.08, 0.410, 'MODULE 3', fontsize=8, color=GRAY, fontweight='bold', va='center')
draw_box(ax, 0.47, 0.395, 0.72, 0.075,
         'SEPARATION FEASIBILITY MODULE',
         'Yang-Cussler Hollow-Fiber Contactor Model  |  Membrane area  |  Recovery curves  |  Bottleneck flags',
         color=ORANGE, fontsize=9)

draw_arrow(ax, 0.32, 0.470, 0.47, 0.432, color=GREEN)
draw_arrow(ax, 0.68, 0.470, 0.47, 0.432, color=GREEN)

# ── Layer 6: Scale-up Assessment ──────────────────────────────────────
ax.text(0.08, 0.295, 'MODULE 4', fontsize=8, color=GRAY, fontweight='bold', va='center')
draw_box(ax, 0.47, 0.285, 0.72, 0.075,
         'SCALE-UP & FEASIBILITY ASSESSMENT',
         'Mass transfer limits  |  Heat removal  |  Fouling risk  |  Scale Readiness Score  |  Pilot validation checklist',
         color=ORANGE, fontsize=9)

draw_arrow(ax, 0.47, 0.357, 0.47, 0.322, color=ORANGE)

# ── Layer 7: Outputs ──────────────────────────────────────────────────
ax.text(0.08, 0.175, 'OUTPUTS', fontsize=8, color=GRAY, fontweight='bold', va='center')
outputs = [
    (0.175, 0.16, 'Optimization\nProtocol Card'),
    (0.365, 0.16, 'ML Model\n& Dataset'),
    (0.555, 0.16, 'Scale-Up\nDesign Template'),
    (0.745, 0.16, 'PDF Technical\nReport'),
]
for x, y, lbl in outputs:
    draw_box(ax, x, y, 0.165, 0.07, lbl, color=LIGHTOR, text_color='#1a1a1a', fontsize=8)

draw_arrow(ax, 0.47, 0.247, 0.175, 0.195, color=ORANGE)
draw_arrow(ax, 0.47, 0.247, 0.365, 0.195, color=ORANGE)
draw_arrow(ax, 0.47, 0.247, 0.555, 0.195, color=ORANGE)
draw_arrow(ax, 0.47, 0.247, 0.745, 0.195, color=ORANGE)

# ── Bottom label ───────────────────────────────────────────────────────
ax.text(0.5, 0.045,
        'Any U.S. lab or manufacturer can run any waste stream through BioForge '
        'and receive actionable optimization results — independently, without access to the developer.',
        ha='center', va='center', fontsize=8.5, color=GRAY, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=WHITE, edgecolor=LIGHTBLUE, alpha=0.7))

ax.text(0.5, 0.015, 'BioForge v0.1  |  Ogaga Maxwell Okedi  |  github.com/ogaga-ai/BioForge',
        ha='center', fontsize=7.5, color=GRAY)

plt.tight_layout()
out_path = '../outputs/figures/BioForge_Architecture.png'
plt.savefig(out_path, dpi=180, bbox_inches='tight', facecolor=LIGHTGRAY)
print(f'Architecture diagram saved to: {out_path}')
plt.show()
