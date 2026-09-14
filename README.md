# Runtime Performance Analysis of Optimized Docker Images in CI/CD Deployment

Experiment data, measurement scripts, and statistical analysis for the paper
**"Runtime Performance Analysis of Optimized Docker Images in CI/CD Deployment"**
by Alvian Devano Sugiarto and Nicholaus Hendrik Jeremy (School of Computer Science,
Binus University), presented at ICACSIS 2026.

This study extends Fachrudin & Affandi (2025), *"Implementation and Analysis of
Container Image Optimization Using Alpine Linux and Multi-Stage Builds"*
(Teknika, vol. 14, no. 1), by evaluating whether Docker image optimization using
Alpine Linux and multi-stage builds introduces runtime performance trade-offs
for Node.js applications in CI/CD deployment.

## Key Findings

- The Alpine multi-stage image pulled **~4.3× faster** than the unoptimized
  baseline (Kruskal-Wallis H = 74.30, p < 0.001, ε² = 0.85 — large effect)
- **No statistically significant differences** were detected in container
  startup time, throughput, or p95 response latency (all small effect sizes)
- Memory usage was lowest for the Alpine multi-stage image, consistent with
  prior work on musl libc

## Image Configurations

| Configuration | Base Image | Build Strategy | Approx. Size |
|---|---|---|---|
| node-single | node:18 | single-stage | ~400 MB |
| node-alpine-multi | node:18-alpine | multi-stage | ~51 MB |
| alpine-multi | alpine:3.19 | multi-stage | ~24 MB |

Images are published on Docker Hub under `vee4n/`.

## Experiment Environment

- **Server:** AWS EC2 t3.small (2 vCPU, 2 GB RAM), Ubuntu 22.04 LTS
- **Docker:** Engine 29.1.3, images built with Docker Buildx
  (`--platform linux/amd64`, `--no-cache`), hosted on Docker Hub
- **Workload:** Node.js Express application with three endpoints
  (`/health`, `/compute`, `/data`)
- **Load testing:** k6 — 50 virtual users, 60 seconds, targeting `/compute`,
  run from a separate machine to avoid resource contention
- **Trials:** 30 independent trials per image configuration for pull time,
  startup time, throughput, and p95 latency; CPU/memory collected as
  descriptive time series

## Metrics

| Category | Metric | Unit |
|---|---|---|
| Deployment | Image pull time | ms |
| Startup | Container startup time | ms |
| Runtime | Throughput | req/s |
| Runtime | p95 response latency | ms |
| Resource | CPU usage | % |
| Resource | Memory usage | MB |

## Statistical Analysis

- **Normality:** Shapiro-Wilk test
- **Group comparison:** Kruskal-Wallis (non-parametric, independent samples)
- **Post-hoc:** Dunn's test with Bonferroni correction
- **Effect size:** epsilon-squared (ε²)
- Significance assessed at α = 0.05

## Reproducing the Analysis

```bash
pip install pandas numpy scipy
python scripts/statistical_analysis.py
python scripts/stats_revision.py   # medians, IQR, sample sizes, effect sizes
```

## Citation

If you use this data or code, please cite:

```
A. D. Sugiarto and N. H. Jeremy, "Runtime Performance Analysis of Optimized
Docker Images in CI/CD Deployment," in Proc. International Conference on
Advanced Computer Science and Information Systems (ICACSIS), 2026.
```

## License

Data and code are provided for academic and research purposes.
