# Muscat 2040: Growth & Infrastructure Challenge

**CodeStacker 2026 — Data Analytics Track**

Estimating Muscat Governorate's population growth to 2040 and analyzing its impact on healthcare and education infrastructure.

## 🎯 Challenge

Estimate how Muscat's population may grow by 2040 and analyse how that growth could impact infrastructure capacity. Build three growth scenarios, assess at least two infrastructure sectors, and create an interactive model.

## 📊 Key Findings

| Metric | 2024 | 2040 (Base Case) | Gap |
|--------|------|------------------|-----|
| **Population** | 1.50M | 2.23M | +48% |
| **Hospital Beds** | 2,500 | 6,678 needed | -3,778 deficit |
| **Schools** | 330 | 742 needed | +412 new |
| **Teachers** | ~15,000 | ~29,700 needed | +14,700 new |

Both healthcare and education **already fall below international benchmarks** and gaps widen under all scenarios.

## 🏗️ Project Structure

```
├── app.py                              # Interactive Streamlit dashboard
├── requirements.txt                    # Python dependencies
├── data/
│   ├── sources.json                    # Raw data + source citations
│   ├── population_projections.json     # Projection model output
│   └── infrastructure_analysis.json    # Healthcare + education analysis
├── notebooks/
│   ├── population_projection.py        # Population model + charts
│   ├── infrastructure_analysis.py      # Infrastructure analysis + charts
│   ├── population_projection.png       # Population chart
│   ├── growth_sensitivity.png          # Sensitivity chart
│   ├── healthcare_analysis.png         # Healthcare charts
│   └── education_analysis.png          # Education charts
└── docs/
    ├── executive_summary.md            # 2-page executive summary
    └── technical_appendix.md           # Full methodology + sources
```

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/abdullah-aljunaibi/codestacker-2026-data-analytics.git
cd codestacker-2026-data-analytics

# Install
pip install -r requirements.txt

# Run interactive model
streamlit run app.py
```

The dashboard opens at `http://localhost:8501` with adjustable sliders for:
- Population growth rates (base/high/low)
- Net migration adjustment
- Hospital bed benchmarks
- School capacity targets
- Teacher:student ratios

## 📈 Three Scenarios

| Scenario | Rate | Pop 2040 | Rationale |
|----------|------|----------|-----------|
| **Low Growth** | 1.5%/yr | 1.90M | Omanization pressure, low oil |
| **Base Case** | 2.5%/yr | 2.23M | Vision 2040 diversification |
| **High Growth** | 4.0%/yr | 2.81M | Muscat as regional hub |

## 📖 Deliverables

1. **Executive Summary** — `docs/executive_summary.md` (2 pages, decision-maker focused)
2. **Interactive Model** — `app.py` (Streamlit with 8+ adjustable assumptions)
3. **Technical Appendix** — `docs/technical_appendix.md` (sources, assumptions, methodology)

## 🔗 Data Sources

- NCSI Oman (population statistics)
- WHO (healthcare benchmarks)
- UNESCO (education benchmarks)
- Oman News Agency (hospital data)
- Oman Observer / Muscat Daily (reporting)

Full citations with URLs in `docs/technical_appendix.md`.

## Author

**Abdullah Al Junaibi** — BxB | CodeStacker 2026
