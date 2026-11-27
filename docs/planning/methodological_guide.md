# Methodological Guide

Document the mathematical definitions, data partitioning protocol, feature transformations, evaluation metrics, and statistical hypothesis tests governing this research project.

## 1. Data Partitioning & Leakage Prevention
- Clearly separate development (`train`), model selection (`validation`), and final held-out evaluation (`test`) sets.
- Compute scalers, encoders, and imputation statistics strictly on `train`.

## 2. Evaluation Metrics & Physical Thresholds
- Define every evaluation formula cleanly and load physical detection floors from `.env` rather than hardcoding magic numbers.
