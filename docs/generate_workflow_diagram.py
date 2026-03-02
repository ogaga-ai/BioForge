"""
BioForge Optimization Workflow Diagram
----------------------------------------
Step-by-step pipeline: Input Data -> DOE Engine -> ML Training ->
Sensitivity Analysis -> Optimum Search -> Protocol Card Output.

Run: python docs/generate_workflow_diagram.py
Output: outputs/figures/BioForge_Workflow.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pathlib

ROOT = pathlib.Path(__file__).parent.parent

BLUE   = '#1565C0'
DKBLUE = '#0D47A1'
GREEN  = '#2E7D32'
ORANGE = '#E65100'
LGRAY  = '#ECEFF1'
GRAY   = '#546E7A'
WHITE  = '#FFFFFF'
MGRAY  = '#B0BEC5'

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_xlim(0, 16)
ax.set_ylim(0, 8)
ax.axis('off')
fig.patch.set_facecolor(LGRAY)
ax.set_facecolor(LGRAY)

# Title
ax.text(8, 7.65, 'BioForge Optimization Workflow',
        ha='center', va='center', fontsize=16, fontweight='bold', color=DKBLUE)
ax.text(8, 7.18,
        'End-to-end data pipeline: experimental inputs to actionable protocol output',
        ha='center', va='center', fontsize=9.5, color=GRAY, style='italic')

# Pipeline step definitions: (x_center, step_num, title, subtitle, color, icon)
STEP_Y = 5.3
BOX_W  = 2.10
BOX_H  = 1.60

steps = [
    (1.40,  1, 'INPUT\nDATA',        '17-run BBD\nCSV file',               GREEN),
    (3.80,  2, 'DOE\nENGINE',        'Box-Behnken\nDesign matrix',         BLUE),
    (6.20,  3, 'ML\nTRAINING',       '4 Models\nLOO-CV selection',         BLUE),
    (8.60,  4, 'SENSITIVITY\nANALYS', 'Permutation\nImportance ranking',   ORANGE),
    (11.00, 5, 'OPTIMUM\nSEARCH',   'Grid search\nbest conditions',        ORANGE),
    (13.40, 6, 'PROTOCOL\nCARD',     'Reproducible\noutput (.txt)',         GREEN),
]

for (cx, num, title, subtitle, color) in steps:
    # Main node box
    box = FancyBboxPatch(
        (cx - BOX_W / 2, STEP_Y - BOX_H / 2), BOX_W, BOX_H,
        boxstyle='round,pad=0.10',
        facecolor=color, edgecolor=WHITE, linewidth=3, zorder=3
    )
    ax.add_patch(box)

    # Step number badge (top-left corner of box)
    badge = plt.Circle(
        (cx - BOX_W / 2 + 0.26, STEP_Y + BOX_H / 2 - 0.26),
        0.22, color=WHITE, zorder=4
    )
    ax.add_patch(badge)
    ax.text(cx - BOX_W / 2 + 0.26, STEP_Y + BOX_H / 2 - 0.26,
            str(num), ha='center', va='center',
            fontsize=9, color=color, fontweight='bold', zorder=5)

    # Title text
    ax.text(cx, STEP_Y + 0.18, title,
            ha='center', va='center', fontsize=10, color=WHITE,
            fontweight='bold', fontfamily='monospace', zorder=4)

    # Subtitle text
    ax.text(cx, STEP_Y - 0.48, subtitle,
            ha='center', va='center', fontsize=7.8,
            color='#e8f5e9' if color == GREEN else '#e3f2fd' if color == BLUE else '#fff3e0',
            zorder=4, linespacing=1.4)

    # Arrow to next step
    if num < 6:
        next_cx = steps[num][0]
        ax.annotate('',
                    xy=(next_cx - BOX_W / 2 - 0.04, STEP_Y),
                    xytext=(cx + BOX_W / 2 + 0.04, STEP_Y),
                    arrowprops=dict(arrowstyle='->', color=GRAY, lw=2.2), zorder=2)

# Output figures row
OUTPUT_Y = 2.4
out_boxes = [
    (1.40,  'EDA Scatter\nPlot (.png)',          GREEN,  3),
    (4.50,  'Model Validation\nChart (.png)',     BLUE,   3),
    (7.60,  'Sensitivity\nChart (.png)',          ORANGE, 4),
    (10.70, 'Response Surface\nContour (.png)',   ORANGE, 5),
    (13.85, 'Protocol Card\nOutput (.txt)',       GREEN,  6),
]

OUT_W, OUT_H = 2.30, 1.10
for (cx, label, color, parent_step) in out_boxes:
    # Arrow from parent step down
    parent_cx = steps[parent_step - 1][0]
    ax.annotate('',
                xy=(cx, OUTPUT_Y + OUT_H / 2 + 0.06),
                xytext=(parent_cx, STEP_Y - BOX_H / 2 - 0.06),
                arrowprops=dict(
                    arrowstyle='->', color=MGRAY, lw=1.4,
                    connectionstyle='arc3,rad=0.0'
                ), zorder=2)

    # Output box (lighter, smaller)
    obox = FancyBboxPatch(
        (cx - OUT_W / 2, OUTPUT_Y - OUT_H / 2), OUT_W, OUT_H,
        boxstyle='round,pad=0.07',
        facecolor=color, edgecolor=WHITE, linewidth=2,
        alpha=0.70, zorder=3
    )
    ax.add_patch(obox)
    ax.text(cx, OUTPUT_Y, label,
            ha='center', va='center', fontsize=8.2,
            color=WHITE, fontweight='600', zorder=4, linespacing=1.4)

# Section labels
ax.text(0.20, STEP_Y, 'Pipeline:', ha='left', va='center',
        fontsize=8.5, color=GRAY, fontweight='700', style='italic')
ax.text(0.20, OUTPUT_Y, 'Outputs:', ha='left', va='center',
        fontsize=8.5, color=GRAY, fontweight='700', style='italic')

# Footer
ax.text(8, 0.50,
        'Each stage is implemented as a separate, independently importable Python module '
        'in the BioForge package.',
        ha='center', va='center', fontsize=8.5, color=GRAY,
        bbox=dict(boxstyle='round,pad=0.32', facecolor=WHITE,
                  edgecolor='#b0bec5', alpha=0.80), zorder=4)
ax.text(8, 0.12, 'BioForge v0.1  |  Ogaga Maxwell Okedi  |  github.com/ogaga-ai/BioForge',
        ha='center', fontsize=7.5, color=GRAY)

plt.tight_layout(pad=0.4)
out = ROOT / 'outputs' / 'figures' / 'BioForge_Workflow.png'
plt.savefig(str(out), dpi=180, bbox_inches='tight', facecolor=LGRAY)
print(f'Workflow diagram saved to: {out}')
