# Muscat 2040: Growth & Infrastructure Model

![Tests Passing](https://img.shields.io/badge/tests-passing-lightgrey)
![Python 3.12](https://img.shields.io/badge/python-3.12-lightgrey)
![Streamlit](https://img.shields.io/badge/streamlit-dashboard-lightgrey)

Muscat Governorate is projected to grow materially by 2040, and even moderate growth creates pressure on essential infrastructure. This project models three population scenarios and translates them into sector demand for healthcare, education, and water supply. The outputs are published as JSON artifacts and surfaced through a Streamlit dashboard for scenario testing. The work was developed for the CodeStacker 2026 Data Analytics challenge.

## Project Overview

The model starts from a 2024 Muscat baseline population of 1,499,549 and applies a compound annual growth approach through 2040. It then estimates infrastructure demand under three scenarios:

- `Low Growth`: 1.5% annual growth
- `Base Case`: 2.5% annual growth
- `High Growth`: 4.0% annual growth

Sector modules cover:

- Healthcare: hospital bed demand against WHO and GCC benchmarks
- Education: school and teacher requirements against quality capacity targets
- Water and utilities: desalination demand against current and planned supply

## Key Findings

| Sector | Current State | 2040 Gap | Key Insight |
|---|---|---:|---|
| Healthcare | ~2,500 beds in Muscat, or roughly 1.67 beds per 1,000 residents | Base case shortfall of ~3,778 beds against WHO 3.0/1,000 benchmark | Muscat already sits below benchmark levels today, so growth compounds an existing capacity deficit |
| Education | ~330 schools serving ~300,000 school-age students, or ~900 students per school | Base case need for ~412 additional schools at the 600-student quality target and ~14,685 more teachers | The city is already operating above a quality-oriented school density threshold |
| Water / Utilities | ~280 MLD effective supply in 2024, rising to ~580 MLD after planned additions | Base case shows no 2040 deficit after expansion; high growth narrows reserve materially | Water is the least constrained sector in the modeled base case, but resilience depends on delivery of planned desalination capacity |

## Architecture

```text
Public data sources
  NCSI / WHO / UNESCO / PAEW / OPWP / Omani reporting
            |
            v
Analysis scripts
  notebooks/population_projection.py
  notebooks/infrastructure_analysis.py
            |
            v
Generated JSON outputs
  data/population_projections.json
  data/infrastructure_analysis.json
  data/sources.json
            |
            v
Interactive Streamlit dashboard
  app.py
```

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/abdullah-aljunaibi/codestacker-2026-data-analytics.git
cd codestacker-2026-data-analytics
```

### 2. Install dependencies

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

### 3. Generate analysis outputs

```bash
python3 notebooks/population_projection.py
python3 notebooks/infrastructure_analysis.py
```

This refreshes:

- `data/population_projections.json`
- `data/infrastructure_analysis.json`
- `data/sources.json`
- `notebooks/*.png`

### 4. Launch the dashboard

```bash
streamlit run app.py
```

The dashboard opens locally at `http://localhost:8501` and allows interactive adjustment of growth rates, migration assumptions, sector benchmarks, and planning thresholds.

## Testing

Run the automated test suite with:

```bash
python3 -m pytest tests/ -v
```

The repository currently includes 22 tests covering:

- Population projection logic
- Infrastructure demand formulas
- Water capacity calculations
- Script execution and output generation
- Data drift detection (sources.json ↔ model ↔ docs consistency)

To validate the Streamlit app syntax without launching it:

```bash
python3 -c "import ast; ast.parse(open('app.py').read()); print('Streamlit syntax OK')"
```

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── tests.yml
├── app.py
├── Makefile
├── README.md
├── data/
│   ├── infrastructure_analysis.json
│   ├── population_projections.json
│   └── sources.json
├── docs/
│   ├── executive_summary.md
│   └── technical_appendix.md
├── notebooks/
│   ├── education_analysis.png
│   ├── growth_sensitivity.png
│   ├── healthcare_analysis.png
│   ├── infrastructure_analysis.py
│   ├── population_projection.png
│   ├── population_projection.py
│   └── water_analysis.png
├── requirements-dev.txt
├── requirements.txt
└── tests/
    ├── conftest.py
    └── test_model.py
```

## Data Sources

The model draws on public data and benchmarks, with detailed references stored in `data/sources.json` and expanded discussion in [docs/technical_appendix.md](docs/technical_appendix.md).

- `NCSI`: Muscat and national population totals, growth context, and population composition
- `WHO`: hospital bed and minimum domestic water access benchmarks
- `UNESCO`: education planning benchmarks, especially school quality and teacher ratios
- `PAEW`: domestic water consumption assumptions and utility planning context
- `OPWP`: desalination capacity and planned water infrastructure additions

Supporting Omani publications are used where governorate-level operational counts are not published directly in a single official table.

## Methodology

### Compound growth model

Population is projected using:

```text
P(t) = P(2024) x (1 + r)^(t - 2024)
```

where `r` varies by scenario.

### Benchmark-driven infrastructure demand

- Healthcare demand is derived from population and hospital beds per 1,000 people
- Education demand uses a school-age share assumption and target students-per-school / teacher ratios
- Water demand uses per-capita liters per day with a planning safety factor

### Gap analysis

Each sector compares modeled 2040 demand to current and planned capacity, then reports the residual shortfall or surplus. This makes the outputs decision-oriented rather than purely descriptive.

## Limitations and Assumptions

- Muscat-specific infrastructure counts are partly estimated from national totals and major facility references where official governorate data is incomplete
- Population is modeled with a simple compound growth framework rather than a cohort-component demographic model
- Capacity additions are treated as discrete planned expansions and do not include unknown future policy interventions
- Education demand uses a constant school-age population share across the projection horizon
- Water demand assumes a fixed per-capita consumption rate and safety factor rather than seasonal or industrial demand modeling
- The dashboard is a planning model, not a budget, engineering, or procurement system

## Documentation

- Executive summary: [docs/executive_summary.md](docs/executive_summary.md)
- Technical appendix: [docs/technical_appendix.md](docs/technical_appendix.md)

## Author and Challenge Attribution

Author: Abdullah Al Junaibi  
Challenge: CodeStacker 2026 Data Analytics  
Project focus: Muscat 2040 population growth and infrastructure demand modeling
