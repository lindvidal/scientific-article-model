# Q1 Figure Caption Patterns

Compact reference templates targeting **20–35 words** (≤ 45 words) across common scientific figure archetypes.

## 1. Multi-Panel Spatial Characterization (`(a)–(d)`)
> **Figure 1.** Study area characterization: (a) geographic macro-regions and state boundaries; (b) gauge spatial density (`1° × 1°` grid, log scale); (c) SRTM elevation; and (d) Köppen–Geiger climate classification (Alvares et al., 2013b).

*Pruned:* two-letter state codes, individual climate subtype codes listed in the legend, `500 km` scale bar, North arrow, and peak cell count reported in prose.

## 2. Regional / Network Zoom Comparison
> **Figure 2.** Homogeneous precipitation regions (adapted from Lemos et al., 2023) and UNIPLU-BR gauge distribution (2015–2025): (a) Brazil (*n* = 4,771); (b) Northeast coast (*n* = 852); and (c) Southeast coast (*n* = 1,249).

*Pruned:* redundant `"zoom inset"` / `"dashed bounding boxes"` explanations visible on the graphic.

## 3. Methodological Workflow / Diagram
> **Figure 3.** Methodological workflow of the framework, spanning data curation and REF-VI quality control, spatial feature engineering, hyperparameter optimization with IDW benchmarking, and statistical evaluation.

*Pruned:* step-by-step section numbers and tuning trial counts detailed in Section 3 prose/tables.

## 4. Multi-Model Boxplots / Distance-Decay / Seasonal Series
> **Figure 8.** Validation KGE across nine *k* = 5 mean neighbor-distance intervals for each machine learning model (*N* = 3,813 gauges, 2015–2023; outliers omitted).

*Pruned:* verbatim bin bounds (`0–10 km` to `200–600 km`) and per-bin *n* values printed directly on the x-axis.

## 5. Feature Importance / Matrix Heatmap
> **Figure 10.** Global permutation feature importance (mean KGE reduction) across all 40 predictors for the top-three models (GBR, XGB, and MLP; 2015–2023 validation).

*Pruned:* Python class names (`GradientBoostingRegressor`, `XGBRegressor`), sorting rule, and raw feature regex suffixes already shown on the y-axis.

---

## Pre-Finish Checklist
- [ ] Plot image and plotting code/notebook both inspected in the current session.
- [ ] Word count of `**Figure N.**` body is concise (**20–35 words**, ≤ 45 unless multi-panel complexity demands more).
- [ ] No duplication of legend entries, axis bounds, scale bars, or narrative statistics.
- [ ] Model/dataset names follow canonical manuscript nomenclature; defined acronyms stay compact.
- [ ] Alt-text `![Figure N: ...]` and in-text `(Figure N)` numbers match sequential order.
