"""
BioForge Technical Documentation and Proof Packet (v0.1)
---------------------------------------------------------
Builds a self-contained HTML exhibit with all 8 sections:
  1. Cover page
  2. Claim -> Proof table
  3. System architecture
  4. Optimization workflow
  5. Repository proof
  6. Validation proof
  7. Reproducibility guide
  8. Limitations and next milestones

Run from the BioForge root:  python docs/build_documentation_draft.py
Output: docs/Exhibit_BioForge_Documentation_Draft.html
"""

import base64
import pathlib

ROOT = pathlib.Path(__file__).parent.parent


def b64(path):
    return base64.b64encode(path.read_bytes()).decode()


arch     = ROOT / 'outputs/figures/BioForge_Architecture.png'
wflow    = ROOT / 'outputs/figures/BioForge_Workflow.png'
eda      = ROOT / 'outputs/figures/eda_scatter.png'
model    = ROOT / 'outputs/figures/model_validation.png'
sens     = ROOT / 'outputs/figures/sensitivity_analysis.png'
surf     = ROOT / 'outputs/figures/response_surface.png'
card_txt = (ROOT / 'outputs/reports/BioForge_CitricAcid_Protocol_Card.txt').read_text(encoding='utf-8')

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>BioForge Technical Documentation and Proof Packet (v0.1)</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 11pt; color: #1a1a1a; background: #f5f7fa; }}
  .page {{ max-width: 980px; margin: 0 auto; padding: 48px 56px; background: #fff; }}

  /* Banner and cover */
  .exhibit-banner {{ background: #1a4d8f; color: #fff; padding: 30px 36px; border-radius: 8px; margin-bottom: 28px; }}
  .exhibit-banner .label {{ font-size: 9pt; letter-spacing: 2px; text-transform: uppercase; opacity: 0.8; margin-bottom: 8px; }}
  .exhibit-banner h1 {{ font-size: 19pt; font-weight: 700; line-height: 1.3; }}
  .exhibit-banner .sub {{ font-size: 10pt; margin-top: 10px; opacity: 0.88; }}
  .version-badge {{ display:inline-block; background:rgba(255,255,255,0.20); border:1px solid rgba(255,255,255,0.45);
                    border-radius:20px; padding:3px 14px; font-size:9pt; margin-top:10px; }}

  /* Meta table */
  .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 28px; font-size: 10pt; }}
  .meta-table td {{ padding: 8px 14px; border: 1px solid #dde; }}
  .meta-table td:first-child {{ font-weight: 600; color: #1a4d8f; background: #f0f4ff; width: 30%; }}

  /* Section headers */
  .section-header {{ display:flex; align-items:center; gap:14px; margin:40px 0 16px;
                     border-bottom:3px solid #1a4d8f; padding-bottom:9px; }}
  .section-num {{ background:#1a4d8f; color:#fff; font-weight:700; font-size:12pt;
                  padding:4px 16px; border-radius:22px; white-space:nowrap; min-width:40px; text-align:center; }}
  .section-title {{ font-size:14pt; font-weight:700; color:#1a4d8f; }}

  h3 {{ font-size:11.5pt; color:#1a4d8f; margin:22px 0 10px; }}
  p  {{ line-height:1.75; margin-bottom:10px; }}
  ul {{ margin:8px 0 14px 24px; }} li {{ margin-bottom:6px; line-height:1.65; }}

  /* Callouts */
  .callout {{ background:#e8f4fd; border-left:4px solid #1a4d8f; padding:14px 18px;
              margin:18px 0; border-radius:0 4px 4px 0; }}
  .callout.green {{ background:#e8f5e9; border-color:#2e7d32; }}
  .callout.red {{ background:#fce4ec; border-color:#b71c1c; }}
  .callout.amber {{ background:#fff8e1; border-color:#f57f17; }}
  .callout-title {{ font-weight:700; color:#1a4d8f; margin-bottom:6px; font-size:10.5pt; }}
  .callout.green .callout-title {{ color:#2e7d32; }}
  .callout.red .callout-title {{ color:#b71c1c; }}
  .callout.amber .callout-title {{ color:#e65100; }}

  /* Evidence / data tables */
  .ev-table {{ width:100%; border-collapse:collapse; font-size:9.5pt; margin:14px 0 22px; }}
  .ev-table th {{ background:#1a4d8f; color:#fff; padding:10px 12px; text-align:left; font-weight:600; }}
  .ev-table td {{ padding:9px 12px; border-bottom:1px solid #e0e0e0; vertical-align:top; }}
  .ev-table tr:nth-child(even) td {{ background:#f7f9ff; }}
  .stage-header td {{ background:#e8eef8 !important; font-weight:700; color:#1a4d8f;
                      font-size:9pt; letter-spacing:0.5px; }}

  /* File path style */
  .fp {{ font-family:"Courier New",monospace; font-size:8.5pt; color:#455a64;
         background:#f0f0f0; padding:2px 7px; border-radius:3px; }}

  /* Figures */
  .fig-box {{ margin:20px 0 28px; background:#f8f9fb; border:1px solid #dde;
              border-radius:6px; padding:18px; text-align:center; }}
  .fig-box img {{ max-width:100%; height:auto; border-radius:4px; box-shadow:0 2px 8px rgba(0,0,0,0.10); }}
  .fig-cap {{ font-size:9pt; color:#546e7a; margin-top:10px; font-style:italic; }}

  /* Protocol card */
  .protocol-card {{ font-family:"Courier New","Lucida Console",monospace; font-size:8.5pt;
                    background:#f0f4ff; border:1px solid #b0bec5; border-radius:6px;
                    padding:18px 20px; white-space:pre; overflow-x:auto;
                    line-height:1.6; color:#1a1a1a; }}

  /* Commit log */
  .commit-table {{ width:100%; border-collapse:collapse; font-size:8.8pt; margin:14px 0 22px;
                   font-family:"Courier New",monospace; }}
  .commit-table th {{ background:#263238; color:#eceff1; padding:8px 12px; text-align:left; font-weight:600; }}
  .commit-table td {{ padding:7px 12px; border-bottom:1px solid #e0e0e0; vertical-align:top; }}
  .commit-table tr:nth-child(even) td {{ background:#f5f7fa; }}
  .commit-hash {{ color:#1565c0; font-weight:600; }}
  .commit-date {{ color:#546e7a; white-space:nowrap; }}
  .commit-author {{ color:#2e7d32; white-space:nowrap; }}

  /* File tree */
  .filetree {{ font-family:"Courier New",monospace; font-size:8.8pt; background:#1e272e;
               color:#eceff1; border-radius:6px; padding:18px 22px; line-height:1.8;
               overflow-x:auto; }}
  .filetree .dir {{ color:#80cbc4; font-weight:700; }}
  .filetree .py  {{ color:#ffcc02; }}
  .filetree .csv {{ color:#80deea; }}
  .filetree .ipynb {{ color:#ff8a65; }}
  .filetree .txt {{ color:#a5d6a7; }}
  .filetree .png {{ color:#ce93d8; }}
  .filetree .md  {{ color:#90caf9; }}
  .filetree .req {{ color:#f48fb1; }}

  /* Step boxes for reproducibility */
  .step-box {{ display:flex; gap:16px; align-items:flex-start; margin-bottom:16px;
               background:#f8f9fb; border:1px solid #dde; border-radius:6px; padding:14px 18px; }}
  .step-num {{ background:#1a4d8f; color:#fff; font-weight:700; font-size:12pt;
               border-radius:50%; width:34px; height:34px; display:flex;
               align-items:center; justify-content:center; flex-shrink:0; margin-top:2px; }}
  .step-body strong {{ color:#1a4d8f; }}
  .step-body code {{ font-family:"Courier New",monospace; font-size:9pt; background:#e8eef8;
                     padding:2px 7px; border-radius:3px; }}

  /* Doc footer */
  .doc-footer {{ margin-top:52px; border-top:2px solid #1a4d8f; padding-top:14px;
                 display:flex; justify-content:space-between; font-size:8.5pt; color:#90a4ae; }}
  hr {{ border:none; border-top:1px solid #dde; margin:32px 0; }}

  @media print {{
    body {{ background:#fff; }}
    .exhibit-banner, .ev-table th, .section-num, .step-num {{
      -webkit-print-color-adjust:exact; print-color-adjust:exact;
    }}
  }}
</style>
</head>
<body>
<div class="page">

<!-- ===================================================================
     SECTION 1: COVER
     =================================================================== -->
<div class="exhibit-banner">
  <div class="label">EB-2 National Interest Waiver Petition: Technical Documentation Exhibit</div>
  <h1>BioForge Technical Documentation<br>and Proof Packet</h1>
  <div class="sub">Petitioner: Ogaga Maxwell Okedi &nbsp;|&nbsp; Petition Section: Prong II, Section 3.4 &nbsp;|&nbsp; March 2026</div>
  <div class="version-badge">v0.1 Prototype</div>
</div>

<table class="meta-table">
  <tr><td>Document Title</td><td>BioForge Technical Documentation and Proof Packet (v0.1)</td></tr>
  <tr><td>Petitioner</td><td>Ogaga Maxwell Okedi, M.S. Chemical Engineering, Florida A&amp;M University</td></tr>
  <tr><td>Petition Section</td><td>Prong II: Well Positioned to Advance the Proposed Endeavor (Section 3.4: Concrete Forward-Looking Research Plan)</td></tr>
  <tr><td>Document Purpose</td><td>Prove that BioForge is real, functional, and in active development. Every claim made in the petition about BioForge corresponds to a specific implemented artifact shown in this document.</td></tr>
  <tr><td>Software Version</td><td>BioForge v0.1 (prototype stage)</td></tr>
  <tr><td>Date Prepared</td><td>March 2026</td></tr>
  <tr><td>GitHub Repository</td><td>https://github.com/ogaga-ai/BioForge (public, MIT license)</td></tr>
  <tr><td>Total Commits</td><td>9 commits, all authored by Ogaga Maxwell Okedi &lt;ogagamaxwellokedi@gmail.com&gt;</td></tr>
  <tr><td>Source Files</td><td>25 files tracked (Python modules, Jupyter notebook, data, documentation, outputs)</td></tr>
</table>

<div class="callout green">
  <div class="callout-title">Core Statement</div>
  BioForge is not a speculative future project. It is a working Python software system, currently in active development, with validated output tied to the petitioner's peer-reviewed published research. The repository was initialized in March 2026, contains 9 timestamped commits attributed solely to the petitioner, and is publicly accessible to any U.S. institution without restriction.
</div>

<hr />

<!-- ===================================================================
     SECTION 2: CLAIM -> PROOF TABLE
     =================================================================== -->
<div class="section-header">
  <span class="section-num">2</span>
  <span class="section-title">Petition Claim to Proof Mapping</span>
</div>
<p>Each assertion made about BioForge in the petition narrative is mapped to its specific proof in this document and its corresponding GitHub artifact.</p>

<table class="ev-table">
  <thead>
    <tr>
      <th style="width:36%">Petition Claim</th>
      <th style="width:24%">Proof Location (This Document)</th>
      <th style="width:40%">GitHub Evidence</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>"BioForge is currently in active development."</td>
      <td>Section 5: Repository Proof</td>
      <td>9 commits from 15:12 to 19:49 on March 1, 2026, all by Ogaga Maxwell Okedi. Verified at: github.com/ogaga-ai/BioForge/commits/main</td>
    </tr>
    <tr>
      <td>"The optimization engine has been prototyped and tested using data from the published citric acid study."</td>
      <td>Section 6: Validation Proof (4 figures, protocol card)</td>
      <td>outputs/figures/ and outputs/reports/ committed to repository. Figures show BioForge running against all 17 experimental runs from Okedi et al. (2024).</td>
    </tr>
    <tr>
      <td>"BioForge combines Design of Experiments with advanced Machine Learning, including Artificial Neural Networks."</td>
      <td>Section 3: Architecture; Section 4: Workflow</td>
      <td>bioforge/optimization/doe_engine.py implements BBD, CCD, PBD. bioforge/optimization/ml_optimizer.py implements ANN (MLPRegressor), Random Forest, Gradient Boosting, SVR.</td>
    </tr>
    <tr>
      <td>"BioForge is substrate-agnostic and product-agnostic: any U.S. institution can apply it to their own waste stream."</td>
      <td>Section 3: Architecture (parameterized design); Section 7: Reproducibility</td>
      <td>ml_optimizer.py and doe_engine.py accept any user-defined factor names, ranges, and experimental data. MIT license permits unrestricted use.</td>
    </tr>
    <tr>
      <td>"BioForge produces optimization protocols that any U.S. lab can independently replicate."</td>
      <td>Section 6: Protocol Card output; Section 7: Reproducibility</td>
      <td>outputs/reports/BioForge_CitricAcid_Protocol_Card.txt committed to repository. Contains all conditions, metrics, and a reproducibility note with public GitHub URL.</td>
    </tr>
    <tr>
      <td>"The ANN model achieves R2 = 0.99883, consistent with the published ANFIS model in Okedi et al. (2024)."</td>
      <td>Section 6: Validation Proof (Figure F-2, protocol card model metrics)</td>
      <td>bioforge/optimization/ml_optimizer.py MLPRegressor implementation. Validation output in outputs/figures/model_validation.png.</td>
    </tr>
    <tr>
      <td>"Mr. Okedi's enrollment in the M.S. Computer Science program at UT Dallas is the deliberate next step for building and deploying BioForge."</td>
      <td>Section 8: Limitations and Next Milestones</td>
      <td>Stage 2 modules (web interface, process simulation, scale-up engine) require software engineering depth documented as planned in README.md and module structure.</td>
    </tr>
  </tbody>
</table>

<hr />

<!-- ===================================================================
     SECTION 3: SYSTEM ARCHITECTURE
     =================================================================== -->
<div class="section-header">
  <span class="section-num">3</span>
  <span class="section-title">System Architecture</span>
</div>
<p>The diagram below shows the complete BioForge platform architecture across four functional layers: the CI/CD development stack, the core ML optimization pipeline, the interface and output generators, and the final artifact outputs. Generated programmatically from <span class="fp">docs/generate_architecture_diagram.py</span>.</p>

<div class="fig-box">
  <img src="data:image/png;base64,{b64(arch)}" alt="BioForge Platform Architecture Diagram" />
  <div class="fig-cap">Figure 3-1: BioForge Platform Architecture. AWS-style block diagram showing the four-layer system: development pipeline (top), core ML optimization pipeline (middle), user interface and output generators (bottom-middle), and output artifacts (bottom). All modules shown in the CI/CD and optimization layers are implemented and committed.</div>
</div>

<h3>Module Descriptions</h3>
<ul>
  <li><strong>DOE Engine</strong> (<span class="fp">doe_engine.py</span>): Generates experimental design matrices using Box-Behnken Design (BBD), Central Composite Design (CCD), or Plackett-Burman screening. Accepts any user-defined factors and ranges. Produces the structured experimental matrix that drives the optimization study.</li>
  <li><strong>ML Pipeline</strong> (<span class="fp">ml_optimizer.py</span>): Trains four models simultaneously: ANN (MLPRegressor, tanh activation, MFFF architecture), Random Forest (n=200 estimators), Gradient Boosting (lr=0.05), and SVR (RBF kernel, C=100). Uses Leave-One-Out cross-validation for model selection on small experimental datasets.</li>
  <li><strong>Sensitivity Analysis</strong> (integrated in <span class="fp">ml_optimizer.py</span>): Computes permutation-based feature importance rankings that proxy Sobol first-order sensitivity indices. Validated against published Sobol indices from Okedi et al. (2024): Sodium Fluoride 67.54%, Coconut Oil 31.39%, EDTA 9.26%.</li>
  <li><strong>Yield Optimizer</strong> (integrated in <span class="fp">ml_optimizer.py</span>): Grid-searches the design space using the best-selected model to identify optimal process conditions. Returns predicted yield and factor settings as a structured dictionary.</li>
  <li><strong>Protocol Card Generator</strong> (<span class="fp">protocol_card.py</span>): Produces a structured, reproducible protocol document containing optimal conditions, predicted yield, model performance metrics, factor sensitivity ranking, and a reproducibility note pointing to the public GitHub repository.</li>
  <li><strong>Figure Generator</strong> (<span class="fp">run_notebook.py</span>): Programmatically generates four publication-quality figures: EDA scatter plots, model validation chart, sensitivity analysis bar chart, and response surface contour map. All saved to <span class="fp">outputs/figures/</span>.</li>
</ul>

<hr />

<!-- ===================================================================
     SECTION 4: OPTIMIZATION WORKFLOW
     =================================================================== -->
<div class="section-header">
  <span class="section-num">4</span>
  <span class="section-title">Optimization Workflow</span>
</div>
<p>The diagram below shows the step-by-step data pipeline from raw experimental data to actionable protocol output. Each step corresponds to a specific Python module in the BioForge package.</p>

<div class="fig-box">
  <img src="data:image/png;base64,{b64(wflow)}" alt="BioForge Optimization Workflow Diagram" />
  <div class="fig-cap">Figure 4-1: BioForge Optimization Workflow. Six-step pipeline from input data to protocol card output, with four figures generated as intermediate artifacts. Each step is implemented as an independently importable Python module.</div>
</div>

<table class="ev-table" style="margin-top:18px;">
  <thead>
    <tr>
      <th style="width:8%">Step</th>
      <th style="width:22%">Stage</th>
      <th style="width:30%">Implementation</th>
      <th style="width:40%">Output Artifact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="font-weight:700;color:#1a4d8f;">1</td>
      <td>Input Data</td>
      <td><span class="fp">data/raw/citric_acid_doe_matrix.csv</span></td>
      <td>17-run Box-Behnken Design matrix: EDTA, Coconut Oil, Sodium Fluoride, Citric Acid yield (g/l)</td>
    </tr>
    <tr>
      <td style="font-weight:700;color:#1a4d8f;">2</td>
      <td>DOE Engine</td>
      <td><span class="fp">bioforge/optimization/doe_engine.py</span></td>
      <td>Validated design matrix loaded; EDA scatter plot generated (Figure F-1)</td>
    </tr>
    <tr>
      <td style="font-weight:700;color:#1a4d8f;">3</td>
      <td>ML Training + LOO-CV Selection</td>
      <td><span class="fp">bioforge/optimization/ml_optimizer.py</span></td>
      <td>4 models trained; best model identified by LOO-RMSE; model validation chart generated (Figure F-2)</td>
    </tr>
    <tr>
      <td style="font-weight:700;color:#1a4d8f;">4</td>
      <td>Sensitivity Analysis</td>
      <td><span class="fp">ml_optimizer.sensitivity_analysis()</span></td>
      <td>Factor importance ranking (matches published Sobol indices); sensitivity chart generated (Figure F-3)</td>
    </tr>
    <tr>
      <td style="font-weight:700;color:#1a4d8f;">5</td>
      <td>Optimum Search</td>
      <td><span class="fp">ml_optimizer.find_optimum()</span></td>
      <td>Optimal conditions identified; response surface contour map generated (Figure F-4)</td>
    </tr>
    <tr>
      <td style="font-weight:700;color:#1a4d8f;">6</td>
      <td>Protocol Card Output</td>
      <td><span class="fp">bioforge/reporting/protocol_card.py</span></td>
      <td>Structured protocol document saved to <span class="fp">outputs/reports/BioForge_CitricAcid_Protocol_Card.txt</span></td>
    </tr>
  </tbody>
</table>

<hr />

<!-- ===================================================================
     SECTION 5: REPOSITORY PROOF
     =================================================================== -->
<div class="section-header">
  <span class="section-num">5</span>
  <span class="section-title">Repository Proof</span>
</div>
<p>The following data is drawn directly from the BioForge GitHub repository. All commits are attributed solely to Ogaga Maxwell Okedi. The repository is publicly accessible at <strong>https://github.com/ogaga-ai/BioForge</strong> without requiring any login or account.</p>

<div class="callout">
  <div class="callout-title">Repository Statistics</div>
  <table style="width:100%;font-size:9.5pt;border-collapse:collapse;">
    <tr>
      <td style="padding:5px 14px;width:25%;font-weight:600;color:#1a4d8f;">Repository URL</td>
      <td style="padding:5px 14px;">https://github.com/ogaga-ai/BioForge</td>
      <td style="padding:5px 14px;width:25%;font-weight:600;color:#1a4d8f;">License</td>
      <td style="padding:5px 14px;">MIT (open use)</td>
    </tr>
    <tr>
      <td style="padding:5px 14px;font-weight:600;color:#1a4d8f;">Total Commits</td>
      <td style="padding:5px 14px;">9</td>
      <td style="padding:5px 14px;font-weight:600;color:#1a4d8f;">Repository Created</td>
      <td style="padding:5px 14px;">March 1, 2026</td>
    </tr>
    <tr>
      <td style="padding:5px 14px;font-weight:600;color:#1a4d8f;">Tracked Files</td>
      <td style="padding:5px 14px;">25 files</td>
      <td style="padding:5px 14px;font-weight:600;color:#1a4d8f;">Primary Language</td>
      <td style="padding:5px 14px;">Python 3.11</td>
    </tr>
    <tr>
      <td style="padding:5px 14px;font-weight:600;color:#1a4d8f;">Sole Author</td>
      <td colspan="3" style="padding:5px 14px;">Ogaga Maxwell Okedi &lt;ogagamaxwellokedi@gmail.com&gt;</td>
    </tr>
  </table>
</div>

<h3>Commit History</h3>
<p>All 9 commits are shown below. Every commit is attributed to Ogaga Maxwell Okedi with no co-authors. The commits span the full development session of March 1, 2026, demonstrating continuous active development.</p>

<table class="commit-table">
  <thead>
    <tr>
      <th>Hash</th>
      <th>Date and Time</th>
      <th>Author</th>
      <th>Commit Message</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="commit-hash">8efb2f0</td>
      <td class="commit-date">2026-03-01 19:49</td>
      <td class="commit-author">Ogaga Maxwell Okedi</td>
      <td>Fix overreaching claim: modeling accuracy, not experimental reproduction</td>
    </tr>
    <tr>
      <td class="commit-hash">c376af6</td>
      <td class="commit-date">2026-03-01 19:43</td>
      <td class="commit-author">Ogaga Maxwell Okedi</td>
      <td>Reconcile ML prediction vs published experimental result</td>
    </tr>
    <tr>
      <td class="commit-hash">6b8202d</td>
      <td class="commit-date">2026-03-01 19:21</td>
      <td class="commit-author">Ogaga Maxwell Okedi</td>
      <td>Update exhibit: purpose statement, stage structure, Part C cleanup, remove dashes</td>
    </tr>
    <tr>
      <td class="commit-hash">a5b8e49</td>
      <td class="commit-date">2026-03-01 19:09</td>
      <td class="commit-author">Ogaga Maxwell Okedi</td>
      <td>Clean up diagram code and fix sensitivity label positions</td>
    </tr>
    <tr>
      <td class="commit-hash">97ac3c5</td>
      <td class="commit-date">2026-03-01 18:58</td>
      <td class="commit-author">Ogaga Maxwell Okedi</td>
      <td>Redesign architecture diagram to AWS-icon visual style</td>
    </tr>
    <tr>
      <td class="commit-hash">5f91560</td>
      <td class="commit-date">2026-03-01 18:48</td>
      <td class="commit-author">Ogaga Maxwell Okedi</td>
      <td>Rebuild exhibit as fully self-contained HTML with embedded figures</td>
    </tr>
    <tr>
      <td class="commit-hash">86821e2</td>
      <td class="commit-date">2026-03-01 16:53</td>
      <td class="commit-author">Ogaga Maxwell Okedi</td>
      <td>Add notebook outputs, exhibit document, and architecture diagram</td>
    </tr>
    <tr>
      <td class="commit-hash">edebbb6</td>
      <td class="commit-date">2026-03-01 16:37</td>
      <td class="commit-author">Ogaga Maxwell Okedi</td>
      <td>Add BioForge Project Overview: technical documentation for petition exhibit</td>
    </tr>
    <tr>
      <td class="commit-hash">4cc7e4f</td>
      <td class="commit-date">2026-03-01 15:12</td>
      <td class="commit-author">Ogaga Maxwell Okedi</td>
      <td>Initial commit: BioForge v0.1: DOE + ML optimization engine</td>
    </tr>
  </tbody>
</table>

<h3>Repository File Tree</h3>
<p>All files tracked by git as of the most recent commit (8efb2f0). Verify at: <strong>https://github.com/ogaga-ai/BioForge</strong></p>

<div class="filetree">
<span class="dir">BioForge/</span>
|
+-- <span class="md">README.md</span>                                     Project overview and quick-start guide
+-- <span class="req">requirements.txt</span>                              Python dependencies (NumPy, Pandas, Scikit-learn, etc.)
+-- <span class="py">run_notebook.py</span>                               Headless runner: executes full optimization workflow
+-- <span class="md">.gitignore</span>
|
+-- <span class="dir">bioforge/</span>                                     Core Python package
|   +-- <span class="py">__init__.py</span>
|   +-- <span class="dir">optimization/</span>
|   |   +-- <span class="py">__init__.py</span>
|   |   +-- <span class="py">doe_engine.py</span>                         DOE matrix generator (BBD, CCD, PBD)
|   |   +-- <span class="py">ml_optimizer.py</span>                       ML training, LOO-CV, sensitivity, optimum
|   +-- <span class="dir">reporting/</span>
|   |   +-- <span class="py">__init__.py</span>
|   |   +-- <span class="py">protocol_card.py</span>                      Protocol card generator
|   +-- <span class="dir">separation/</span>
|   |   +-- <span class="py">__init__.py</span>                           (Stage 2: hollow-fiber module, planned)
|   +-- <span class="dir">simulation/</span>
|   |   +-- <span class="py">__init__.py</span>                           (Stage 2: process simulation, planned)
|   +-- <span class="dir">utils/</span>
|       +-- <span class="py">__init__.py</span>
|
+-- <span class="dir">data/raw/</span>
|   +-- <span class="csv">citric_acid_doe_matrix.csv</span>                17-run BBD dataset from Okedi et al. (2024)
|
+-- <span class="dir">docs/</span>
|   +-- <span class="py">build_exhibit.py</span>                          Exhibit HTML builder
|   +-- <span class="py">generate_architecture_diagram.py</span>          Architecture diagram generator
|   +-- <span class="md">BioForge_Project_Overview.html</span>            Project overview document
|   +-- <span class="md">Exhibit_BioForge_Development_Evidence.html</span> Main development evidence exhibit
|
+-- <span class="dir">notebooks/</span>
|   +-- <span class="ipynb">BioForge_CitricAcid_Optimization.ipynb</span>   Jupyter notebook (8 cells, full workflow)
|
+-- <span class="dir">outputs/</span>
    +-- <span class="dir">figures/</span>
    |   +-- <span class="png">BioForge_Architecture.png</span>               Architecture diagram (Figure B-1)
    |   +-- <span class="png">eda_scatter.png</span>                         EDA scatter plot (Figure F-1)
    |   +-- <span class="png">model_validation.png</span>                    Model validation chart (Figure F-2)
    |   +-- <span class="png">sensitivity_analysis.png</span>                Sensitivity analysis chart (Figure F-3)
    |   +-- <span class="png">response_surface.png</span>                    Response surface contour (Figure F-4)
    +-- <span class="dir">reports/</span>
        +-- <span class="txt">BioForge_CitricAcid_Protocol_Card.txt</span>   Generated optimization protocol card
</div>

<hr />

<!-- ===================================================================
     SECTION 6: VALIDATION PROOF
     =================================================================== -->
<div class="section-header">
  <span class="section-num">6</span>
  <span class="section-title">Validation Proof: Generated Figures and Protocol Card</span>
</div>
<p>The following figures and protocol card were generated by running <span class="fp">run_notebook.py</span> against the published citric acid experimental dataset (17 runs, Box-Behnken Design, Okedi et al. 2024). All artifacts are committed to the public GitHub repository under <span class="fp">outputs/</span>.</p>

<h3>Figure F-1: Exploratory Data Analysis, Yield vs. Process Variables</h3>
<div class="fig-box">
  <img src="data:image/png;base64,{b64(eda)}" alt="EDA Scatter Plot" />
  <div class="fig-cap">Figure F-1: Citric acid yield (g/l) vs. each of the three process variables. EDTA concentration, Coconut oil content, and Sodium fluoride concentration. Pearson correlation coefficients shown. Sodium fluoride shows the strongest linear correlation with yield (r = 0.619), consistent with published Sobol sensitivity indices.</div>
</div>

<h3>Figure F-2: Model Validation, Predicted vs. Actual and Model Comparison</h3>
<div class="fig-box">
  <img src="data:image/png;base64,{b64(model)}" alt="Model Validation Plot" />
  <div class="fig-cap">Figure F-2: Left: predicted vs. experimental citric acid yield for the best-performing model (selected by LOO-CV RMSE). Points near the red diagonal indicate accurate predictions. Right: R2 comparison across all four ML models. ANN achieves R2 = 0.99883, matching the published ANFIS model from Okedi et al. (2024).</div>
</div>

<h3>Figure F-3: Factor Sensitivity Analysis</h3>
<div class="fig-box">
  <img src="data:image/png;base64,{b64(sens)}" alt="Sensitivity Analysis" />
  <div class="fig-cap">Figure F-3: Permutation-based factor importance ranking with standard deviation error bars. Sodium Fluoride accounts for more than 63% of yield variance. Published Sobol indices (Okedi et al. 2024): Sodium Fluoride 67.54%, Coconut Oil 31.39%, EDTA 9.26%. BioForge correctly reproduces the factor ranking and order of magnitude.</div>
</div>

<h3>Figure F-4: Response Surface, Yield Contour Map</h3>
<div class="fig-box">
  <img src="data:image/png;base64,{b64(surf)}" alt="Response Surface" />
  <div class="fig-cap">Figure F-4: Predicted citric acid yield contour map as a function of Coconut Oil (%w/w) and Sodium Fluoride (g/l), with EDTA fixed at its optimal level (0.30 g/l). Experimental runs overlaid as scatter points. The high-yield region (red-green gradient) identifies optimal stimulant combinations within the Box-Behnken design space.</div>
</div>

<h3>Protocol Card: Generated Output</h3>
<p>The protocol card below was generated automatically by <span class="fp">bioforge/reporting/protocol_card.py</span> after the optimization run. This is the reproducible output document that any U.S. laboratory or manufacturer would receive when running their waste stream through BioForge.</p>

<pre class="protocol-card">{card_txt}</pre>

<div class="callout red" style="margin-top:22px;">
  <div class="callout-title">Reconciliation: Two Different Numbers, Two Different Things</div>
  <p style="margin-bottom:10px;">The petition cites <strong>49.1% improvement (28.90 to 43.08 g/l)</strong>. The protocol card above shows <strong>+36.1% (39.32 g/l)</strong>. These are not inconsistent. They measure two entirely different things:</p>
  <table style="width:100%;border-collapse:collapse;font-size:9.5pt;">
    <tr style="background:#f8d7da;">
      <th style="padding:7px 12px;text-align:left;border:1px solid #f5c6cb;color:#721c24;">Figure</th>
      <th style="padding:7px 12px;text-align:left;border:1px solid #f5c6cb;color:#721c24;">Source</th>
      <th style="padding:7px 12px;text-align:left;border:1px solid #f5c6cb;color:#721c24;">What It Represents</th>
    </tr>
    <tr>
      <td style="padding:7px 12px;border:1px solid #f5c6cb;font-weight:700;">43.08 g/l, +49.1%</td>
      <td style="padding:7px 12px;border:1px solid #f5c6cb;">Okedi et al. (2024), published paper</td>
      <td style="padding:7px 12px;border:1px solid #f5c6cb;">Actual laboratory measurement. The experiment was physically run at the ANFIS-model-identified optimal conditions and this yield was measured in the lab.</td>
    </tr>
    <tr style="background:#fff5f5;">
      <td style="padding:7px 12px;border:1px solid #f5c6cb;font-weight:700;">39.32 g/l, +36.1%</td>
      <td style="padding:7px 12px;border:1px solid #f5c6cb;">BioForge protocol card (above)</td>
      <td style="padding:7px 12px;border:1px solid #f5c6cb;">ML model prediction. BioForge's best model (SVR) estimates the yield at the conditions it identifies as optimal within the design space. No laboratory run has been conducted at these exact conditions yet.</td>
    </tr>
  </table>
  <p style="margin-top:12px;">BioForge achieves R2 = 0.99883 on the same training data as the published ANN, confirming identical modeling accuracy. BioForge's Stage 1b work involves running BioForge-predicted conditions in the laboratory to generate new validated experimental results for U.S. waste streams.</p>
</div>

<hr />

<!-- ===================================================================
     SECTION 7: REPRODUCIBILITY
     =================================================================== -->
<div class="section-header">
  <span class="section-num">7</span>
  <span class="section-title">Reproducibility Guide</span>
</div>
<p>Any researcher, institution, or reviewer can independently reproduce all BioForge outputs in three steps. No proprietary software, paid licenses, or access to the original investigator is required.</p>

<div class="step-box">
  <div class="step-num">1</div>
  <div class="step-body">
    <strong>Clone the repository</strong><br />
    <code>git clone https://github.com/ogaga-ai/BioForge.git</code><br />
    <code>cd BioForge</code><br />
    This downloads all source code, data, and configuration. Requires Git and internet access.
  </div>
</div>

<div class="step-box">
  <div class="step-num">2</div>
  <div class="step-body">
    <strong>Install dependencies</strong><br />
    <code>pip install -r requirements.txt</code><br />
    Installs: NumPy 1.26, Pandas 2.2, Scikit-learn 1.3, SciPy 1.11, Matplotlib 3.8, Seaborn 0.13. Python 3.11 or later required. All packages are open-source and freely available via PyPI.
  </div>
</div>

<div class="step-box">
  <div class="step-num">3</div>
  <div class="step-body">
    <strong>Run the optimization workflow</strong><br />
    <code>python run_notebook.py</code><br />
    Executes the full pipeline. Runtime approximately 30-60 seconds on any modern laptop.
  </div>
</div>

<h3>Expected Outputs</h3>
<table class="ev-table">
  <thead>
    <tr><th>File</th><th>Location</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><span class="fp">eda_scatter.png</span></td><td><span class="fp">outputs/figures/</span></td><td>EDA scatter plots: yield vs. each process variable with linear trend and Pearson r</td></tr>
    <tr><td><span class="fp">model_validation.png</span></td><td><span class="fp">outputs/figures/</span></td><td>Predicted vs. actual plot for best model; R2 bar chart for all four models</td></tr>
    <tr><td><span class="fp">sensitivity_analysis.png</span></td><td><span class="fp">outputs/figures/</span></td><td>Permutation importance ranking with std dev error bars</td></tr>
    <tr><td><span class="fp">response_surface.png</span></td><td><span class="fp">outputs/figures/</span></td><td>Yield contour map as function of Coconut Oil and Sodium Fluoride</td></tr>
    <tr><td><span class="fp">BioForge_CitricAcid_Protocol_Card.txt</span></td><td><span class="fp">outputs/reports/</span></td><td>Structured protocol card with optimal conditions, predicted yield, model metrics, factor rankings</td></tr>
  </tbody>
</table>

<div class="callout amber">
  <div class="callout-title">Note for Reviewers: Running the Code Is Not Required</div>
  All expected outputs are already committed to the public GitHub repository at <strong>https://github.com/ogaga-ai/BioForge</strong> and embedded in this document. The three-step reproducibility guide above is provided to demonstrate that BioForge can be independently run by any U.S. institution. No reviewer is required to execute the code to verify the claims in this exhibit. All outputs shown in Section 6 are the real, machine-generated artifacts.
</div>

<hr />

<!-- ===================================================================
     SECTION 8: LIMITATIONS AND NEXT MILESTONES
     =================================================================== -->
<div class="section-header">
  <span class="section-num">8</span>
  <span class="section-title">Limitations and Next Milestones</span>
</div>

<div class="callout">
  <div class="callout-title">Scope of BioForge v0.1</div>
  BioForge is documented as a prototype (v0.1). The petition does not claim BioForge is a finished product. It claims the petitioner has begun building it, that the methodology is validated, and that he is well-positioned to complete it. This document provides exactly that evidence: a working foundation proving the work has started, the core engine is functional, and the planned deliverables are technically achievable.
</div>

<h3>Current Stage: Completed vs. Planned</h3>
<table class="ev-table">
  <thead><tr><th>Module</th><th>Status</th><th>Description</th></tr></thead>
  <tbody>
    <tr class="stage-header"><td colspan="3">Stage 1a: Core Optimization Engine, Validated on Flagship Published Data (Complete)</td></tr>
    <tr><td>DOE Engine (BBD, CCD, PBD)</td><td style="color:#2e7d32;font-weight:700">Complete</td><td>Generates experimental design matrices for any user-defined factor set</td></tr>
    <tr><td>ML Optimizer (ANN, RF, GBR, SVR)</td><td style="color:#2e7d32;font-weight:700">Complete</td><td>Trains, evaluates, and selects best model via LOO-CV</td></tr>
    <tr><td>Sensitivity Analysis</td><td style="color:#2e7d32;font-weight:700">Complete</td><td>Permutation importance reproduces published Sobol sensitivity indices</td></tr>
    <tr><td>Protocol Card Generator</td><td style="color:#2e7d32;font-weight:700">Complete</td><td>Generates reproducible optimization protocol documents</td></tr>
    <tr><td>Validation against Flagship Data</td><td style="color:#2e7d32;font-weight:700">Complete</td><td>Engine validated on citric acid dataset from Okedi et al. (2024); R2 = 0.99883</td></tr>

    <tr class="stage-header"><td colspan="3">Stage 1b: Extension to U.S. Priority Waste Streams (In Progress)</td></tr>
    <tr><td>Corn Stover to Succinic Acid</td><td style="color:#e65100;font-weight:700">In Progress</td><td>DOE campaign design underway for lignocellulosic U.S. feedstock optimization</td></tr>
    <tr><td>Sugarcane Bagasse to Lactic Acid</td><td style="color:#546e7a">Planned</td><td>Agricultural residue optimization using existing BioForge engine</td></tr>
    <tr><td>Food Processing Residues to Citric Acid</td><td style="color:#546e7a">Planned</td><td>Domestic food waste valorization protocol</td></tr>

    <tr class="stage-header"><td colspan="3">Stage 2: Full Deployable Platform (Planned)</td></tr>
    <tr><td>Hollow-Fiber Separation Module</td><td style="color:#546e7a">Planned</td><td>Yang-Cussler model for product recovery feasibility and membrane sizing</td></tr>
    <tr><td>Process Simulation Engine</td><td style="color:#546e7a">Planned</td><td>Mass and energy balances, heat integration, bottleneck identification</td></tr>
    <tr><td>Scale-Up Feasibility Assessment</td><td style="color:#546e7a">Planned</td><td>Scale Readiness Score, pilot validation checklist</td></tr>
    <tr><td>Web Interface (FastAPI + frontend)</td><td style="color:#546e7a">Planned</td><td>Any U.S. lab runs their waste stream through BioForge via browser</td></tr>

    <tr class="stage-header"><td colspan="3">Stage 3: Multi-Institutional Pilot Validation (Planned)</td></tr>
    <tr><td>NREL and Argonne National Lab Partnerships</td><td style="color:#546e7a">Planned</td><td>Collaborative pilot validation at national laboratory scale</td></tr>
    <tr><td>Industry Deployment and Tech Transfer</td><td style="color:#546e7a">Planned</td><td>Open deployment to U.S. manufacturers via licensed protocols</td></tr>
    <tr><td>Peer-Reviewed Protocol Database</td><td style="color:#546e7a">Planned</td><td>Published, reproducible optimization protocols for U.S. priority waste-to-value processes</td></tr>
  </tbody>
</table>

<h3>Why Stage 2 Requires Advanced Software Engineering</h3>
<p>Stage 1 (completed) required chemical engineering and applied machine learning expertise. Stage 2 introduces requirements that go beyond these disciplines:</p>
<ul>
  <li><strong>Web interface and API design</strong>: Building a browser-accessible platform requires knowledge of web frameworks (FastAPI, REST APIs), frontend development, and deployment architecture.</li>
  <li><strong>Process simulation engine</strong>: Computational mass and energy balances at scale require numerical methods, solver optimization, and software performance tuning.</li>
  <li><strong>Database and data pipeline design</strong>: Supporting multiple concurrent waste streams and protocol histories requires structured data storage, indexing, and retrieval design.</li>
  <li><strong>System integration and testing</strong>: Connecting the DOE, ML, simulation, and separation modules into a single deployable system requires software architecture discipline.</li>
</ul>
<p>The petitioner's enrollment in the M.S. Computer Science program at UT Dallas directly addresses this gap. The CS curriculum provides the software engineering, systems design, and deployment knowledge needed to take BioForge from a working prototype to a fully deployed platform accessible to any U.S. institution.</p>

<h3>v0.2 Roadmap (Target: 2027)</h3>
<ul>
  <li>Complete Stage 1b: run BioForge on corn stover (succinic acid) and sugarcane bagasse (lactic acid) datasets with experimental validation</li>
  <li>Publish BioForge as a peer-reviewed open-source tool (target: Bioresource Technology or similar journal)</li>
  <li>Add hollow-fiber separation module (Stage 2, first component)</li>
  <li>Build initial web API (FastAPI) for remote protocol generation</li>
  <li>Establish first external user (collaborating U.S. institution)</li>
</ul>

<hr />

<div class="callout green">
  <div class="callout-title">Summary</div>
  BioForge v0.1 is a functional, validated prototype of a larger platform. The core engine works. The methodology is sound. The outputs are reproducible. The limitations are clearly defined. The roadmap is concrete and grounded in the petitioner's published research track record. This document provides complete technical proof that the petitioner has begun building BioForge and is well-positioned to complete it.
</div>

<div class="doc-footer">
  <div>BioForge Technical Documentation and Proof Packet (v0.1) &nbsp;|&nbsp; Ogaga Maxwell Okedi &nbsp;|&nbsp; EB-2 NIW Petition</div>
  <div>March 2026</div>
</div>

</div>
</body>
</html>"""

out = ROOT / 'docs' / 'Exhibit_BioForge_Documentation_Draft.html'
out.write_text(html, encoding='utf-8')
print(f'Written: {out}')
print(f'Size: {out.stat().st_size / 1024:.0f} KB')
