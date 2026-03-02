"""
BioForge System Architecture Diagram - AWS-Style
-------------------------------------------------
Generates a professional block diagram using the AWS-architecture
visual language: colored icon boxes, grid background, labeled arrows,
and dashed group boundaries.

Run: python docs/generate_architecture_diagram.py
Output: outputs/figures/BioForge_Architecture.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# --- Palette ---
BLUE   = '#1565C0'   # primary compute / pipeline
DKBLUE = '#0D47A1'   # dark blue (git, version control)
PURPLE = '#6A1B9A'   # orchestration / interface
ORANGE = '#E65100'   # analysis / processing
GREEN  = '#2E7D32'   # storage / outputs
DGRAY  = '#37474F'   # client / user node
GRAY   = '#546E7A'   # arrows, labels
LGRAY  = '#ECEFF1'   # page background
GRID   = '#DDE1E8'   # grid lines
WHITE  = '#FFFFFF'

# --- Figure ---
fig, ax = plt.subplots(figsize=(16, 10))
W, H = 16, 10
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis('off')
fig.patch.set_facecolor(LGRAY)
ax.set_facecolor(LGRAY)

# Grid
for x in np.arange(0, W + 0.5, 0.5):
    ax.axvline(x, color=GRID, lw=0.5, zorder=0)
for y in np.arange(0, H + 0.5, 0.5):
    ax.axhline(y, color=GRID, lw=0.5, zorder=0)

# --- Helpers ---
SZ = 0.78   # default node square size


def node(cx, cy, icon, label, color, sz=SZ, fsz=10.5, lfsz=7.8):
    """AWS-style icon box: colored square + white icon + label below."""
    half = sz / 2
    box = FancyBboxPatch(
        (cx - half, cy - half), sz, sz,
        boxstyle='round,pad=0.07',
        facecolor=color, edgecolor=WHITE, linewidth=2.5, zorder=3
    )
    ax.add_patch(box)
    ax.text(cx, cy, icon, ha='center', va='center',
            fontsize=fsz, color=WHITE, fontweight='bold',
            fontfamily='monospace', zorder=4)
    for i, ln in enumerate(label.split('\n')):
        ax.text(cx, cy - half - 0.10 - i * 0.21, ln,
                ha='center', va='top', fontsize=lfsz,
                color='#1a1a1a', fontweight='600', zorder=4)


def arrow(x1, y1, x2, y2, label='', color=GRAY, lw=1.6,
          rad=0.0, label_offset=(0, 0)):
    """Draw a labeled directional arrow."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->', color=color, lw=lw,
                    connectionstyle=f'arc3,rad={rad}'
                ), zorder=2)
    if label:
        mx = (x1 + x2) / 2 + label_offset[0]
        my = (y1 + y2) / 2 + label_offset[1]
        ax.text(mx, my, label, ha='center', va='center',
                fontsize=6.6, color=GRAY, style='italic',
                bbox=dict(boxstyle='round,pad=0.18', facecolor=LGRAY,
                          edgecolor='none', alpha=0.85), zorder=5)


def group_box(x0, y0, x1, y1, label='', color=BLUE):
    """Dashed group boundary rectangle."""
    rect = FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0,
        boxstyle='round,pad=0.05',
        facecolor='none', edgecolor=color,
        linewidth=1.6, linestyle='--', zorder=1
    )
    ax.add_patch(rect)
    if label:
        ax.text((x0 + x1) / 2, y1 + 0.10, label,
                ha='center', va='bottom', fontsize=8.5,
                color=color, fontweight='700', zorder=4)


# =============================================================================
# TITLE
# =============================================================================
ax.text(W / 2, H - 0.25, 'BioForge Platform Architecture',
        ha='center', va='top', fontsize=17, fontweight='bold', color=DKBLUE)
ax.text(W / 2, H - 0.72,
        'Integrated DOE + ML Bioprocess Optimization Framework  |  v0.1',
        ha='center', va='top', fontsize=9.5, color=GRAY)

# =============================================================================
# ROW 1 (y = 8.0) - BioForge Development CI/CD Stack
# =============================================================================
Y1 = 8.0
group_box(2.4, 7.45, 12.6, 8.55, 'BioForge Development & Version Control', BLUE)

node(1.1,  Y1, '< >',   'VS Code /\nCloud IDE',    DGRAY)
node(3.5,  Y1, 'GIT',   'GitHub\nRepository',      DKBLUE)
node(5.9,  Y1, 'CI',    'CI / Code\nReview',       BLUE)
node(8.3,  Y1, 'BUILD', 'Build &\nUnit Tests',     BLUE)
node(10.7, Y1, 'REL',   'Release\nBuild',          ORANGE)
node(13.2, Y1, 'DOCS',  'README &\nDocumentation', GREEN)

arrow(1.49,  Y1, 3.11,  Y1, 'Push code')
arrow(3.89,  Y1, 5.51,  Y1, 'Pull / review')
arrow(6.29,  Y1, 7.91,  Y1, 'Trigger CI')
arrow(8.69,  Y1, 10.31, Y1, 'Pass tests')
arrow(11.09, Y1, 12.81, Y1, 'Publish')

# Release Deploy arrow down to BioForge Interface (Row 3)
arrow(10.7, 7.61, 10.7, 6.39, 'Deploy', ORANGE, label_offset=(0.30, 0))

# =============================================================================
# ROW 2 (y = 5.8) - Core Optimization Pipeline
# =============================================================================
Y2 = 5.8

node(1.1, Y2, 'DATA', 'Experimental\nData (CSV)', GREEN)
node(3.5, Y2, 'DOE',  'DOE Engine\n(BBD/CCD/PBD)', PURPLE, sz=0.90, fsz=10)

# ML Pipeline dashed group
group_box(5.05, 4.90, 8.55, 6.70, 'ML Pipeline', BLUE)
node(5.65, 6.20, 'ANN', 'ANN\n(tanh)',        BLUE, sz=0.70, fsz=9.5)
node(7.10, 6.20, 'RF',  'Random\nForest',     BLUE, sz=0.70, fsz=9.5)
node(5.65, 5.30, 'GBR', 'Gradient\nBoost',    BLUE, sz=0.70, fsz=9.5)
node(7.10, 5.30, 'SVR', 'SVR\n(RBF)',         BLUE, sz=0.70, fsz=9.5)
ax.text(6.38, 4.96, 'LOO-CV model selection', ha='center', va='bottom',
        fontsize=6.3, color=BLUE, style='italic')

node(10.0, Y2, 'S/A', 'Sensitivity\nAnalysis', ORANGE)
node(12.0, Y2, 'OPT', 'Yield\nOptimizer',      ORANGE)
node(14.4, Y2, 'DB',  'Results\nStore',        GREEN)

arrow(1.49, Y2, 3.05, Y2, 'Input data')
arrow(3.95, Y2, 5.05, Y2, 'DOE matrix')
arrow(4.00, 6.05, 5.30, 6.20, '')
arrow(4.00, 5.55, 5.30, 5.30, '')
arrow(8.55, Y2,   9.61, Y2,  'Predictions')
arrow(10.39, Y2,  11.61, Y2, 'Rankings')
arrow(12.39, Y2,  14.01, Y2, 'Store')

# =============================================================================
# LEFT COLUMN - Researcher (Client equivalent)
# =============================================================================
Y3 = 3.5
node(1.1, Y3, 'USER', 'Researcher /\nManufacturer', DGRAY)

arrow(1.1, 3.89, 1.1, 5.41, 'Provides\ndata', DGRAY, label_offset=(-0.50, 0))
arrow(1.49, Y3, 3.11, Y3, 'Configure &\nrun analysis')

# =============================================================================
# ROW 3 (y = 3.5) - BioForge Interface + Output Generators
# =============================================================================
node(3.5,  Y3, 'CLI',  'BioForge\nInterface', PURPLE)
node(6.2,  Y3, 'P.C.', 'Protocol Card\nGenerator', ORANGE)
node(9.0,  Y3, 'FIG',  'Figure\nGenerator',   ORANGE)
node(12.0, Y3, 'PUB',  'GitHub\nRelease',     GREEN)

arrow(3.89, Y3, 5.81, Y3, 'Optimal conditions')
arrow(6.59, Y3, 8.61, Y3, 'Trigger plots')
arrow(9.39, Y3, 11.61, Y3, 'Commit outputs')

# BioForge Interface -> DOE Engine (configure run)
arrow(3.5, 3.89, 3.5, 5.35, 'Configure\nDOE run', PURPLE, label_offset=(0.52, 0))

# Sensitivity -> Protocol Card Gen (diagonal)
arrow(10.0, 5.41, 6.60, 3.89,
      'Sobol rankings\n& optimum', ORANGE, rad=-0.2, label_offset=(0.6, 0.25))

# Results -> Figure Gen (diagonal)
arrow(14.4, 5.41, 9.40, 3.89,
      'Get results', GREEN, rad=0.15, label_offset=(0.5, 0.35))

# Release Deploy -> BioForge Interface
arrow(10.7, 6.39, 3.89, 3.72, 'Updated\nplatform', ORANGE,
      rad=0.25, label_offset=(0.4, 0.32))

# =============================================================================
# ROW 4 (y = 1.55) - Final output artifacts
# =============================================================================
Y4 = 1.55
node(3.5,  Y4, '.TXT', 'Protocol Card\nOutput (.txt)', GREEN)
node(6.5,  Y4, '.PNG', 'Output Figures\n(4 x PNG)',    GREEN)
node(9.5,  Y4, 'TPL',  'Scale-Up\nTemplate',          GREEN)
node(12.5, Y4, 'REPO', 'Public GitHub\nRepository',   DKBLUE)

arrow(3.5,  3.11, 3.5,  1.94, '', GREEN)
arrow(6.2,  3.11, 6.5,  1.94, '', ORANGE)
arrow(9.0,  3.11, 9.5,  1.94, '', ORANGE)
arrow(12.0, 3.11, 12.5, 1.94, '', GREEN)

# =============================================================================
# FOOTER
# =============================================================================
ax.text(
    W / 2, 0.42,
    '"Any U.S. lab or manufacturer can run any waste stream through BioForge '
    'and receive actionable optimization results - independently."',
    ha='center', va='center', fontsize=8.5, color=GRAY, style='italic',
    bbox=dict(boxstyle='round,pad=0.32', facecolor=WHITE,
              edgecolor='#b0bec5', alpha=0.75), zorder=4
)
ax.text(W / 2, 0.12,
        'BioForge v0.1  |  Ogaga Maxwell Okedi  |  github.com/ogaga-ai/BioForge',
        ha='center', fontsize=7.8, color=GRAY)

plt.tight_layout(pad=0.3)
out = '../outputs/figures/BioForge_Architecture.png'
plt.savefig(out, dpi=180, bbox_inches='tight', facecolor=LGRAY)
print(f'Architecture diagram saved to: {out}')
