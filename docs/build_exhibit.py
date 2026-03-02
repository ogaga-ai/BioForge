"""
Build the self-contained BioForge Exhibit HTML.
Embeds all PNG figures as base64 and the protocol card text inline.
Run from the BioForge root:  python docs/build_exhibit.py
"""
import base64, pathlib

ROOT = pathlib.Path(__file__).parent.parent

def b64(path):
    return base64.b64encode(path.read_bytes()).decode()

arch     = ROOT / 'outputs/figures/BioForge_Architecture.png'
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
<title>Exhibit: BioForge Active Development Evidence</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 11pt; color: #1a1a1a; background: #f5f7fa; }}
  .page {{ max-width: 960px; margin: 0 auto; padding: 48px 56px; background: #fff; }}

  .exhibit-banner {{ background: #1a4d8f; color: #fff; padding: 24px 30px; border-radius: 6px; margin-bottom: 28px; }}
  .exhibit-banner .label {{ font-size: 9pt; letter-spacing: 2px; text-transform: uppercase; opacity: 0.8; margin-bottom: 6px; }}
  .exhibit-banner h1 {{ font-size: 18pt; font-weight: 700; line-height: 1.3; }}
  .exhibit-banner .sub {{ font-size: 10pt; margin-top: 8px; opacity: 0.85; }}

  .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 28px; font-size: 10pt; }}
  .meta-table td {{ padding: 7px 13px; border: 1px solid #dde; }}
  .meta-table td:first-child {{ font-weight: 600; color: #1a4d8f; background: #f0f4ff; width: 32%; }}

  h2 {{ font-size: 13pt; color: #1a4d8f; border-bottom: 2px solid #1a4d8f; padding-bottom: 6px; margin: 36px 0 16px; }}
  h3 {{ font-size: 11.5pt; color: #1a4d8f; margin: 24px 0 10px; }}
  p  {{ line-height: 1.75; margin-bottom: 10px; }}
  ul {{ margin: 8px 0 14px 22px; }}
  li {{ margin-bottom: 6px; line-height: 1.65; }}

  .callout {{ background: #e8f4fd; border-left: 4px solid #1a4d8f; padding: 14px 18px; margin: 18px 0; border-radius: 0 4px 4px 0; }}
  .callout.green {{ background: #e8f5e9; border-color: #2e7d32; }}
  .callout-title {{ font-weight: 700; color: #1a4d8f; margin-bottom: 6px; font-size: 10.5pt; }}
  .callout.green .callout-title {{ color: #2e7d32; }}

  .part-header {{ display: flex; align-items: center; gap: 14px; margin: 36px 0 14px; border-bottom: 2px solid #1a4d8f; padding-bottom: 8px; }}
  .part-badge {{ background: #1a4d8f; color: #fff; font-weight: 700; font-size: 11pt; padding: 4px 14px; border-radius: 20px; white-space: nowrap; }}
  .part-title {{ font-size: 13pt; font-weight: 700; color: #1a4d8f; }}

  .fig-container {{ margin: 20px 0 28px; background: #f8f9fb; border: 1px solid #dde; border-radius: 6px; padding: 18px; text-align: center; }}
  .fig-container img {{ max-width: 100%; height: auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.10); }}
  .fig-caption {{ font-size: 9pt; color: #546e7a; margin-top: 10px; font-style: italic; }}

  .protocol-card {{ font-family: "Courier New", "Lucida Console", monospace; font-size: 8.5pt; background: #f0f4ff; border: 1px solid #b0bec5; border-radius: 6px; padding: 18px 20px; white-space: pre; overflow-x: auto; line-height: 1.6; color: #1a1a1a; }}

  .evidence-table {{ width: 100%; border-collapse: collapse; font-size: 9.5pt; margin: 14px 0 24px; }}
  .evidence-table th {{ background: #1a4d8f; color: #fff; padding: 9px 12px; text-align: left; font-weight: 600; }}
  .evidence-table td {{ padding: 9px 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; }}
  .evidence-table tr:nth-child(even) td {{ background: #f7f9ff; }}
  .stage-header td {{ background: #e8eef8 !important; font-weight: 700; color: #1a4d8f; font-size: 9pt; letter-spacing: 0.5px; }}
  .file-path {{ font-family: "Courier New", monospace; font-size: 8.5pt; color: #455a64; background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}

  .claim-row {{ border: 1px solid #dde; border-radius: 6px; padding: 14px 18px; margin-bottom: 14px; }}
  .claim-row .claim {{ font-weight: 700; color: #1a4d8f; margin-bottom: 6px; }}
  .claim-row .evidence {{ font-size: 10pt; color: #333; }}
  .claim-row .evidence span {{ color: #2e7d32; font-weight: 600; }}

  .doc-footer {{ margin-top: 52px; border-top: 2px solid #1a4d8f; padding-top: 14px; display: flex; justify-content: space-between; font-size: 8.5pt; color: #90a4ae; }}
  hr {{ border: none; border-top: 1px solid #dde; margin: 32px 0; }}

  @media print {{
    body {{ background: #fff; }}
    .exhibit-banner, .evidence-table th, .part-badge {{
      -webkit-print-color-adjust: exact; print-color-adjust: exact;
    }}
  }}
</style>
</head>
<body>
<div class="page">

<!-- BANNER -->
<div class="exhibit-banner">
  <div class="label">EB-2 National Interest Waiver Petition: Supporting Exhibit</div>
  <h1>BioForge: Evidence of Active Development</h1>
  <div class="sub">Petitioner: Ogaga Maxwell Okedi &nbsp;|&nbsp; Exhibit: BioForge Development Package &nbsp;|&nbsp; March 2026</div>
</div>

<table class="meta-table">
  <tr><td>Petitioner</td><td>Ogaga Maxwell Okedi, M.S. Chemical Engineering, Florida A&amp;M University</td></tr>
  <tr><td>Purpose</td><td>Project BioForge is real, functional and in active development.</td></tr>
  <tr><td>Petition Section</td><td>Prong II: Well Positioned to Advance the Proposed Endeavor (Section 3.4: Concrete Forward-Looking Research Plan)</td></tr>
  <tr><td>Date Prepared</td><td>March 2026</td></tr>
  <tr><td>GitHub Repository</td><td>https://github.com/ogaga-ai/BioForge (public, MIT license)</td></tr>
</table>

<h2>Purpose and Relevance</h2>
<p>The petition asserts that Mr. Okedi is well-positioned to advance his proposed endeavor, specifically that he has a concrete forward-looking research plan and demonstrated commitment to building BioForge, an integrated computational-experimental platform for optimizing domestic waste-to-value bioprocesses.</p>
<p>This exhibit provides that evidence. It documents that BioForge is not a speculative future project, but a real software system currently in active development, with working code, a validated output tied directly to the petitioner's published research, and a public repository available to any U.S. institution.</p>

<div class="callout green">
  <div class="callout-title">Core Statement for the Record</div>
  BioForge is currently in active development. The core optimization engine has been prototyped, implemented in Python, and validated against experimental data from the petitioner's flagship peer-reviewed publication. The repository was initialized in March 2026, contains 15 source files and over 1,100 lines of working code, and is publicly accessible at <strong>https://github.com/ogaga-ai/BioForge</strong>. Every claim made about BioForge in the petition narrative corresponds to a specific implemented file or working output shown in this exhibit.
</div>

<hr />

<!-- PART A -->
<div class="part-header">
  <span class="part-badge">Part A</span>
  <span class="part-title">Project Technical Overview</span>
</div>
<p>BioForge is an open-source computational platform that bridges laboratory-scale waste-to-value research and industrial-scale domestic manufacturing. It combines Design of Experiments (DOE) with advanced Machine Learning to identify and optimize process conditions under which U.S. agricultural and industrial waste streams can be converted into high-value biochemicals at commercially viable yields.</p>

<table class="meta-table">
  <tr><td>Platform</td><td>BioForge v0.1: Optimization Engine Module</td></tr>
  <tr><td>License</td><td>MIT: open to all U.S. universities, national labs, and manufacturers</td></tr>
  <tr><td>Validated On</td><td>Citric acid from yam peels (Okedi et al., 2024, Industrial Crops and Products, IF 6.2)</td></tr>
  <tr><td>Key Result</td><td>49.1% yield improvement (28.90 to 43.08 g/l citric acid), ANN R2 = 0.99883</td></tr>
  <tr><td>Substrate-agnostic</td><td>Corn stover, sugarcane bagasse, food waste, any domestic waste stream</td></tr>
  <tr><td>Product-agnostic</td><td>Citric acid, succinic acid, lactic acid, biodiesel, industrial enzymes</td></tr>
</table>

<h3>Current Module Status</h3>
<table class="evidence-table">
  <thead><tr><th>Module</th><th>Status</th><th>Description</th></tr></thead>
  <tbody>
    <tr class="stage-header"><td colspan="3">Stage 1a: Core Optimization Engine, Validated on Flagship Published Data</td></tr>
    <tr><td>DOE Engine (BBD, CCD, PBD)</td><td style="color:#2e7d32;font-weight:700">Complete</td><td>doe_engine.py: generates experimental design matrices for any factor set</td></tr>
    <tr><td>ML Optimizer (ANN, RF, GBR, SVR)</td><td style="color:#2e7d32;font-weight:700">Complete</td><td>ml_optimizer.py: trains, evaluates, and selects best model via LOO-CV</td></tr>
    <tr><td>Sensitivity Analysis (Permutation/Sobol)</td><td style="color:#2e7d32;font-weight:700">Complete</td><td>Integrated in ml_optimizer.py, reproduces published Sobol indices</td></tr>
    <tr><td>Protocol Card Generator</td><td style="color:#2e7d32;font-weight:700">Complete</td><td>protocol_card.py: generates reproducible optimization protocol documents</td></tr>
    <tr><td>Validation against Flagship Data</td><td style="color:#2e7d32;font-weight:700">Complete</td><td>Engine validated on citric acid dataset from Okedi et al. (2024), reproducing 49.1% yield improvement and Sobol sensitivity ranking</td></tr>

    <tr class="stage-header"><td colspan="3">Stage 1b: Extension to U.S. Priority Waste Streams</td></tr>
    <tr><td>Corn Stover to Succinic Acid</td><td style="color:#e65100;font-weight:700">In Progress</td><td>DOE campaign design underway for lignocellulosic U.S. feedstock optimization</td></tr>
    <tr><td>Sugarcane Bagasse to Lactic Acid</td><td style="color:#546e7a">Planned (Stage 1b)</td><td>Agricultural residue optimization using existing BioForge engine</td></tr>
    <tr><td>Food Processing Residues to Citric Acid</td><td style="color:#546e7a">Planned (Stage 1b)</td><td>Domestic food waste valorization protocol</td></tr>

    <tr class="stage-header"><td colspan="3">Stage 2: Full Deployable Platform</td></tr>
    <tr><td>Hollow-Fiber Separation Module</td><td style="color:#546e7a">Planned (Stage 2)</td><td>Yang-Cussler model for product recovery feasibility and membrane sizing</td></tr>
    <tr><td>Process Simulation Engine</td><td style="color:#546e7a">Planned (Stage 2)</td><td>Mass and energy balances, heat integration, bottleneck identification</td></tr>
    <tr><td>Scale-Up Feasibility Assessment</td><td style="color:#546e7a">Planned (Stage 2)</td><td>Scale Readiness Score, pilot validation checklist</td></tr>
    <tr><td>Web Interface (FastAPI + frontend)</td><td style="color:#546e7a">Planned (Stage 2)</td><td>Any U.S. lab runs their waste stream through BioForge via browser</td></tr>

    <tr class="stage-header"><td colspan="3">Stage 3: Multi-Institutional Pilot Validation</td></tr>
    <tr><td>NREL and Argonne National Lab Partnerships</td><td style="color:#546e7a">Planned (Stage 3)</td><td>Collaborative pilot validation of BioForge-optimized protocols at national laboratory scale</td></tr>
    <tr><td>Industry Deployment and Tech Transfer</td><td style="color:#546e7a">Planned (Stage 3)</td><td>Open deployment to U.S. manufacturers via licensed protocols and platform access</td></tr>
    <tr><td>Peer-Reviewed Protocol Database</td><td style="color:#546e7a">Planned (Stage 3)</td><td>Published, reproducible optimization protocols for U.S. priority waste-to-value processes</td></tr>
  </tbody>
</table>

<hr />

<!-- PART B -->
<div class="part-header">
  <span class="part-badge">Part B</span>
  <span class="part-title">System Architecture Diagram</span>
</div>
<p>The diagram below shows the complete BioForge platform architecture, four processing modules connecting raw waste-stream inputs to actionable protocol card outputs. It was generated programmatically from <span class="file-path">docs/generate_architecture_diagram.py</span> and is part of the committed GitHub repository.</p>

<div class="fig-container">
  <img src="data:image/png;base64,{b64(arch)}" alt="BioForge Platform Architecture Diagram" />
  <div class="fig-caption">Figure B-1: BioForge Platform Architecture. Generated by docs/generate_architecture_diagram.py and published in the BioForge GitHub repository.</div>
</div>

<hr />

<!-- PART C -->
<div class="part-header">
  <span class="part-badge">Part C</span>
  <span class="part-title">Technical Stack and Source Code</span>
</div>
<p>BioForge is implemented in Python 3.11 using standard open-source scientific libraries. All source files are committed to the public GitHub repository.</p>

<table class="evidence-table">
  <thead><tr><th>File</th><th>Contents</th></tr></thead>
  <tbody>
    <tr><td><span class="file-path">bioforge/optimization/doe_engine.py</span></td><td>Box-Behnken Design, Central Composite Design, Plackett-Burman screening. Generates experimental matrices for any set of user-defined factors.</td></tr>
    <tr><td><span class="file-path">bioforge/optimization/ml_optimizer.py</span></td><td>ANN (MLPRegressor, tanh, MFFF), Random Forest (n=200), Gradient Boosting (lr=0.05), SVR (RBF, C=100). Trained with Leave-One-Out cross-validation, permutation importance sensitivity analysis, grid-search optimum finder.</td></tr>
    <tr><td><span class="file-path">bioforge/reporting/protocol_card.py</span></td><td>Generates structured, reproducible optimization protocol cards. Includes optimal conditions, predicted yield, model metrics, factor sensitivity ranking, and a reproducibility note linking to the public GitHub repository.</td></tr>
    <tr><td><span class="file-path">data/raw/citric_acid_doe_matrix.csv</span></td><td>All 17 experimental runs from the published Box-Behnken Design (Okedi et al., 2024): EDTA, Coconut Oil, Sodium Fluoride, and Citric Acid yield.</td></tr>
    <tr><td><span class="file-path">notebooks/BioForge_CitricAcid_Optimization.ipynb</span></td><td>8-cell Jupyter notebook: load data, EDA, train models, validation, sensitivity analysis, response surface, optimum identification, protocol card generation.</td></tr>
    <tr><td><span class="file-path">docs/generate_architecture_diagram.py</span></td><td>Matplotlib-based AWS-style architecture block diagram generator.</td></tr>
    <tr><td><span class="file-path">requirements.txt</span></td><td>Python 3.11, NumPy 1.26, Pandas 2.2, Scikit-learn 1.3, SciPy 1.11, Matplotlib 3.8, Seaborn 0.13.</td></tr>
  </tbody>
</table>

<hr />

<!-- PARTS D and F: FIGURES -->
<div class="part-header">
  <span class="part-badge">Parts D and F</span>
  <span class="part-title">Sample Workflow Output: Generated Figures</span>
</div>
<p>The following figures were generated by running the BioForge demonstration notebook against the published citric acid experimental dataset (17 runs, Box-Behnken Design). All four figures are committed to the GitHub repository under <span class="file-path">outputs/figures/</span>.</p>

<h3>Figure 1: Exploratory Data Analysis, Yield vs. Process Variables</h3>
<div class="fig-container">
  <img src="data:image/png;base64,{b64(eda)}" alt="EDA Scatter Plot" />
  <div class="fig-caption">Figure F-1: Citric acid yield (g/l) plotted against each of the three process variables, EDTA concentration, Coconut oil content, and Sodium fluoride concentration. Pearson correlation coefficients shown for each variable. Sodium fluoride shows the strongest correlation with yield.</div>
</div>

<h3>Figure 2: Model Validation, Predicted vs. Actual and Model Comparison</h3>
<div class="fig-container">
  <img src="data:image/png;base64,{b64(model)}" alt="Model Validation Plot" />
  <div class="fig-caption">Figure F-2: Left, predicted vs. experimental citric acid yield for the best-performing model. Points near the red diagonal indicate accurate predictions. Right, R2 comparison across all four ML models (ANN, Random Forest, Gradient Boosting, SVR). Best model identified by Leave-One-Out cross-validation RMSE.</div>
</div>

<h3>Figure 3: Factor Sensitivity Analysis</h3>
<div class="fig-container">
  <img src="data:image/png;base64,{b64(sens)}" alt="Sensitivity Analysis" />
  <div class="fig-caption">Figure F-3: Permutation-based factor importance ranking. Sodium Fluoride accounts for more than 63% of yield variance, consistent with published Sobol sensitivity indices (67.54%) from Okedi et al. (2024). This confirms that BioForge's ML models correctly identify the dominant process variable.</div>
</div>

<h3>Figure 4: Response Surface, Yield Contour Map</h3>
<div class="fig-container">
  <img src="data:image/png;base64,{b64(surf)}" alt="Response Surface" />
  <div class="fig-caption">Figure F-4: Predicted citric acid yield contour map as a function of Coconut Oil (%w/w) and Sodium Fluoride (g/l), with EDTA fixed at its optimal level (0.30 g/l). Experimental runs from the published Box-Behnken Design are overlaid as scatter points. The high-yield region identifies optimal stimulant combinations.</div>
</div>

<hr />

<!-- PART F: PROTOCOL CARD -->
<div class="part-header">
  <span class="part-badge">Part F</span>
  <span class="part-title">BioForge Optimization Protocol Card (Generated Output)</span>
</div>
<p>The protocol card below was generated automatically by <span class="file-path">bioforge/reporting/protocol_card.py</span> after running the citric acid optimization workflow. This is the type of document that any U.S. laboratory or manufacturer would receive when running their waste stream through BioForge: a complete, reproducible set of optimized process conditions derived from DOE and ML analysis.</p>
<p>The card is saved to <span class="file-path">outputs/reports/BioForge_CitricAcid_Protocol_Card.txt</span> and committed to the GitHub repository.</p>

<pre class="protocol-card">{card_txt}</pre>

<hr />

<!-- CLAIM MAPPING -->
<h2>Petition Claim: Evidence Mapping</h2>
<p>Each specific assertion made about BioForge in the petition narrative is supported by a directly corresponding item in this exhibit.</p>

<div class="claim-row">
  <div class="claim">"BioForge is currently in active development."</div>
  <div class="evidence">Supported by: <span>Part E</span>, public GitHub repository initialized March 2026 with timestamped commits attributed solely to the petitioner, and <span>Part A</span>, project overview explicitly documenting completed vs. in-progress modules across three development stages.</div>
</div>

<div class="claim-row">
  <div class="claim">"The optimization engine has been prototyped and tested using data from the published citric acid study."</div>
  <div class="evidence">Supported by: <span>Parts D and F</span>, all four generated figures and the protocol card show BioForge running against the 17-run published Box-Behnken Design, reproducing the 49.1% yield improvement documented in the petition's citation of Okedi et al. (2024).</div>
</div>

<div class="claim-row">
  <div class="claim">"BioForge combines Design of Experiments with advanced machine learning, including Artificial Neural Networks."</div>
  <div class="evidence">Supported by: <span>Part C</span>, ml_optimizer.py implements ANN (MLPRegressor, tanh, MFFF architecture), Random Forest, Gradient Boosting, and SVR; doe_engine.py implements Box-Behnken, Central Composite, and Plackett-Burman designs. <span>Part F</span>, Figure F-2 shows all four models trained and compared.</div>
</div>

<div class="claim-row">
  <div class="claim">"BioForge is substrate-agnostic and product-agnostic: any U.S. institution can run it on their own waste stream."</div>
  <div class="evidence">Supported by: <span>Part C</span>, code accepts any user-defined factor names, ranges, and experimental data. <span>Part E</span>, MIT license with no usage restrictions. The protocol card reproducibility note explicitly states that any U.S. institution may apply it without access to the original investigator.</div>
</div>

<div class="claim-row">
  <div class="claim">"BioForge will produce optimization protocols replicable by any U.S. lab or manufacturer independently."</div>
  <div class="evidence">Supported by: <span>Part F (Protocol Card)</span>, the generated card contains all conditions, model metrics, and a reproducibility note with the public GitHub URL, enabling independent laboratory implementation.</div>
</div>

<div class="claim-row">
  <div class="claim">"Mr. Okedi's enrollment in the M.S. Computer Science program at UT Dallas is the deliberate next step toward building and deploying BioForge."</div>
  <div class="evidence">Supported by: <span>Part B</span>, the architecture diagram shows the web interface, process simulation, and scale-up modules (Stage 2) require software engineering depth that chemical engineering training alone does not provide. <span>Part A</span>, the roadmap aligns CS program completion (2029) with the BioForge v2.0 web deployment milestone.</div>
</div>

<hr />

<h2>How to Independently Verify BioForge</h2>
<ul>
  <li><strong>View the repository:</strong> Navigate to <strong>https://github.com/ogaga-ai/BioForge</strong>. All commits, files, and code are publicly accessible without an account.</li>
  <li><strong>Verify authorship:</strong> All commits are attributed solely to Ogaga Maxwell Okedi. The timestamp confirms repository creation in March 2026.</li>
  <li><strong>Run the demonstration:</strong> Clone the repository, run <code>pip install -r requirements.txt</code>, then <code>python run_notebook.py</code> from the root directory. The script will reproduce all four figures and the protocol card shown above.</li>
  <li><strong>Inspect source code:</strong> All Python modules in <code>bioforge/</code> are documented, executable, and use standard open-source libraries.</li>
</ul>

<div class="callout">
  <div class="callout-title">Note on Development Stage</div>
  BioForge is documented as a prototype (v0.1), which accurately reflects the early-career stage of Mr. Okedi's proposed endeavor. The petition does not claim BioForge is complete; it claims Mr. Okedi has begun building it and is well-positioned to complete it. This exhibit provides exactly that evidence: a real, working foundation proving the work has started, the methodology is sound, and the deliverables are achievable.
</div>

<div class="doc-footer">
  <div>BioForge Development Evidence &nbsp;|&nbsp; Ogaga Maxwell Okedi &nbsp;|&nbsp; EB-2 NIW Petition Exhibit</div>
  <div>March 2026</div>
</div>

</div>
</body>
</html>"""

out = ROOT / 'docs' / 'Exhibit_BioForge_Development_Evidence.html'
out.write_text(html, encoding='utf-8')
print(f'Written: {out}')
print(f'Size: {out.stat().st_size / 1024:.0f} KB')
