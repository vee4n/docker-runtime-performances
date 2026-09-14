#!/usr/bin/env python3
"""
============================================================
Statistical Analysis Script
============================================================
Paper : Runtime Performance Analysis of Optimized Docker
        Images in CI/CD Pipeline Deployment
Author : Alvian Devano Sugiarto, Nicholaus Hendrik Jeremy
Purpose: Performs descriptive statistics, normality testing,
         non-parametric difference testing, and post-hoc
         analysis on Docker image runtime performance data.

Statistical Pipeline:
  1. Descriptive statistics (mean, std, min, max)
  2. Shapiro-Wilk normality test per group
  3. Kruskal-Wallis H test (non-parametric, 3 groups)
  4. Dunn post-hoc test with Bonferroni correction
     (only when Kruskal-Wallis is significant)

Significance level: alpha = 0.05 (95% confidence)

Dependencies:
  pandas, numpy, scipy, scikit-posthocs
Install:
  pip install pandas numpy scipy scikit-posthocs
============================================================
"""

import os
import pandas as pd
import numpy as np
from scipy import stats
import scikit_posthocs as sp

# ── Configuration ───────────────────────────────────────────
ALPHA = 0.05                       # significance threshold
IMAGES = ['node-single', 'node-alpine-multi', 'alpine-multi']

home = os.path.expanduser('~')
BASE = f'{home}/Desktop/Journal/docker-runtime/data/raw'


# ── Data loading ────────────────────────────────────────────
def load_data():
    """Load raw measurement CSVs into dataframes."""
    pull    = pd.read_csv(f'{BASE}/pull-time.csv')
    startup = pd.read_csv(f'{BASE}/startup-time.csv')
    k6      = pd.read_csv(f'{BASE}/k6-summary.csv')
    return pull, startup, k6


# ── Outlier removal ─────────────────────────────────────────
def remove_outliers(pull, startup, k6):
    """
    Remove documented outliers identified prior to analysis.
    Each removal is justified in the Threats to Validity section.
    """
    # Pull time: network anomaly spikes
    pull = pull[~((pull['image'] == 'node-single') &
                  (pull['trial'] == 27))]            # 27,174 ms
    pull = pull[~((pull['image'] == 'node-alpine-multi') &
                  (pull['trial'] == 23))]            # 7,773 ms

    # Startup time: cold-start and warm-up artifacts
    startup = startup[~((startup['image'] == 'node-alpine-multi') &
                        (startup['trial'] == 1))]    # 6,904 ms cold start
    startup = startup[~((startup['image'] == 'alpine-multi') &
                        (startup['trial'] == 1))]    # 6,135 ms cold start
    startup = startup[~((startup['image'] == 'node-single') &
                        (startup['trial'] == 12))]   # 1,126 ms warm-up
    startup = startup[~((startup['image'] == 'node-alpine-multi') &
                        (startup['trial'] == 27))]   # 1,215 ms warm-up
    startup = startup[~((startup['image'] == 'alpine-multi') &
                        (startup['trial'] == 8))]    # 1,180 ms warm-up

    # Runtime: EC2 network disruption during trials 14, 15
    k6 = k6[~((k6['image'] == 'alpine-multi') &
              (k6['trial'].isin([14, 15])))]

    return pull, startup, k6


# ── Core analysis routine ───────────────────────────────────
def analyze(name, df, col, unit):
    """
    Run the full statistical pipeline on one metric.

    Parameters
    ----------
    name : str   Human-readable metric name
    df   : DataFrame  Data containing 'image' and value column
    col  : str   Column holding the measured values
    unit : str   Measurement unit (for printout)
    """
    print("\n" + "=" * 60)
    print(f"METRIC: {name} ({unit})")
    print("=" * 60)

    # 1. Descriptive statistics
    print("\n[1] Descriptive Statistics")
    desc = df.groupby('image')[col].agg(['mean', 'std', 'min', 'max'])
    print(desc.round(2))

    # 2. Shapiro-Wilk normality test (per group)
    print("\n[2] Shapiro-Wilk Normality Test")
    all_normal = True
    for img in IMAGES:
        data = df[df['image'] == img][col].values
        if len(data) >= 3:
            w, p = stats.shapiro(data)
            verdict = "NORMAL" if p > ALPHA else "NON-NORMAL"
            if p <= ALPHA:
                all_normal = False
            print(f"    {img:<20} W={w:.4f}  p={p:.4f}  -> {verdict}")

    # 3. Kruskal-Wallis H test (non-parametric)
    #    Chosen because normality assumption is violated,
    #    making one-way ANOVA inappropriate.
    print("\n[3] Kruskal-Wallis H Test")
    groups = [df[df['image'] == img][col].values for img in IMAGES]
    h, p = stats.kruskal(*groups)
    significant = p < ALPHA
    verdict = "SIGNIFICANT" if significant else "NOT SIGNIFICANT"
    print(f"    H={h:.4f}  p={p:.4f}  -> {verdict}")

    # 4. Dunn post-hoc (only if Kruskal-Wallis is significant)
    print("\n[4] Dunn Post-hoc (Bonferroni-corrected)")
    if significant:
        posthoc = sp.posthoc_dunn(
            df, val_col=col, group_col='image', p_adjust='bonferroni'
        )
        print(posthoc.round(4).to_string())
    else:
        print("    Skipped (Kruskal-Wallis not significant)")


# ── Main execution ──────────────────────────────────────────
def main():
    pull, startup, k6 = load_data()
    pull, startup, k6 = remove_outliers(pull, startup, k6)

    analyze('Image Pull Time',   pull,    'pull_time_ms',    'ms')
    analyze('Container Startup', startup, 'startup_time_ms', 'ms')
    analyze('Runtime Throughput', k6,     'reqs_per_sec',    'req/s')
    analyze('P95 Response Latency', k6,   'p95_latency_ms',  'ms')

    print("\n" + "=" * 60)
    print("Analysis complete.")
    print("=" * 60)


if __name__ == '__main__':
    main()
