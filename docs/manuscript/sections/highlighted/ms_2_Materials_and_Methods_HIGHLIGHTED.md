# Section 2 (Materials and Methods) — Word Revision & Highlight Guide

**Color Legend for Word Edits:**
- <mark style="background-color: #fff176; color: #000000; padding: 1px 3px;">Yellow highlight</mark> = Text added or refined for Q1 style
- <del style="color: #c62828; background-color: #ffebee; text-decoration: line-through;">Red strikethrough</del> = Legacy wordy phrase removed

## 1. Word Revision Summary

| Location | Revision Type | Rationale |
| :--- | :--- | :--- |
| Throughout | Template alignment | Keep running prose conceptual and reproducible; store exhaustive hyperparameter grids in Supplementary Material. |

---

## 2. Full Section Text with Revision Markup

## 2. Materials and Methods

### 2.1 Study Domain and Quality Control

Describe the observational dataset, temporal window, spatial footprint, and minimum instrument detection threshold configured in `.env`. Quality screening filters anomalous records and retains only stations/samples meeting completeness criteria, leaving *N* = 1,000 quality-controlled units for analysis (Table 1).

| Partition | Period / Scope | Sample Size (*n*) | Purpose |
| :--- | :--- | ---: | :--- |
| Development (Train) | Years 1-4 | 600 | Fitting and scaling |
| Validation | Years 5-6 | 200 | Hyperparameter selection |
| Temporal Test | Years 7-8 | 200 | Frozen final benchmark |

### 2.2 Modeling Framework and Evaluation Metrics

Candidate models and the mathematical baseline are trained strictly on the development split, ranked on validation, and evaluated once on held-out temporal test data without data leakage.

```
y_hat_i = f_model(X_i)
```

Multi-objective accuracy and distributional fidelity are quantified using MAE, correlation coefficient, and composite skill scores clipped at the physical detection limit (Gupta et al., 2009). Statistical differences across models are evaluated via Friedman aligned ranks followed by pairwise Wilcoxon signed-rank tests with Holm-Bonferroni correction (Demšar, 2006; García et al., 2010).

---

## 3. References Cited in Section 2 (Materials and Methods) (Verified with DOIs)

1. Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. *Journal of Machine Learning Research*, 7, 1-30. https://jmlr.org/papers/v7/demsar06a.html
2. García, S., Fernández, A., Luengo, J., & Herrera, F. (2010). Advanced nonparametric tests for multiple comparisons in the design of experiments in computational intelligence and data mining. *Information Sciences*, 180(10), 2044-2064. https://doi.org/10.1016/j.ins.2009.12.010
3. Gupta, H. V., Kling, H., Yilmaz, K. K., & Martinez, G. F. (2009). Decomposition of the mean squared error and NSE performance criteria: Implications for improving hydrological modelling. *Journal of Hydrology*, 377(1-2), 80-91. https://doi.org/10.1016/j.jhydrol.2009.08.003
