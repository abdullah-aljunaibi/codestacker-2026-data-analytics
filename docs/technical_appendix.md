# Technical Appendix — Muscat 2040 Growth & Infrastructure Model

---

## 1. Purpose

This appendix documents the data, assumptions, formulas, validation checks, and output pipeline used in the Muscat 2040 growth and infrastructure model. It supports the executive summary and the Streamlit dashboard with reproducible technical detail.

The model is designed for strategic planning and challenge submission purposes. It is not an official forecast, engineering design, or fiscal model.

---

## 2. Data Sources

| Source | Data Used | URL |
|--------|-----------|-----|
| NCSI (via Muscat Daily, Jan 2025) | Muscat population 2024: 1,499,549; 3.0% growth | https://www.muscatdaily.com/2025/01/26/oman-population-increases-2-to-5-268mn-in-2024/ |
| NCSI (via Oman Observer, Oct 2023) | National population growth 6.1% Q3 2023 | https://www.omanobserver.om/article/1144777/ |
| NCSI (via Oman Observer, Jan 2024) | Muscat = 29.7% of national, 1,546,667 residents | https://www.omanobserver.om/article/1147705/ |
| NCSI (via OmanQ, Mar 2025) | Muscat pop 1,499,549; Omanis 584,092 (39%) | https://omanq.com/news/muscats-population-surpasses-1-5-million/ |
| Wikipedia / NCSI | Muscat 2022 population: ~1.72M | https://en.wikipedia.org/wiki/Muscat |
| Oman News Agency (Aug 2024) | 92 hospitals nationally, 7,691 beds | https://omannews.gov.om/topics/en/79/show/118135/ |
| MoH Annual Health Report (2023) | MoH manages 50 hospitals with 5,024 beds nationally | https://www.moh.gov.om |
| Times of Oman / Oman Observer (May 2023) | 11 new hospitals under construction | https://www.omanobserver.om/article/1136940/ |
| Oman Observer (Mar 2023) | 710,000 students nationally = 20% of population | https://www.omanobserver.om/article/1133871/ |
| Oman Observer (Aug 2024) | 46 international schools, 61,704 students, 21 in Muscat | https://www.omanobserver.om/article/1157275/ |
| WHO | Hospital beds benchmark: 3.0 per 1,000 population | https://www.who.int/data/gho |
| UNESCO | Education quality benchmarks | https://uis.unesco.org/ |
| PAEW annual reporting | Domestic water consumption assumptions | Referenced in `data/sources.json` |
| OPWP planning statements | Desalination capacity and planned additions | Referenced in `data/sources.json` |

---

## 3. Scope

The model covers:

- Population growth from 2024 to 2040
- Healthcare demand through hospital beds
- Education demand through schools and teachers
- Water demand through desalinated supply capacity
- Sensitivity analysis around growth assumptions
- Dashboard consumption through JSON outputs

The model does not cover transport, housing, wastewater, electricity, or wilayat-level spatial allocation.

---

## 4. Assumptions Table

| Assumption | Value | Justification |
|-----------|-------|---------------|
| Baseline population | 1,499,549 (end 2024) | NCSI official figure |
| Base growth rate | 2.5%/yr | Slightly below recent 3.0%, accounting for maturation |
| High growth rate | 4.0%/yr | Reflects successful Vision 2040 diversification |
| Low growth rate | 1.5%/yr | Omanization and slower migration scenario |
| Expat share | ~61% | NCSI 2024 data |
| Muscat hospital beds | ~2,500 | Estimated from national total and major Muscat hospitals |
| Planned bed additions | 400 by 2028 | Based on announced hospital construction projects |
| WHO beds benchmark | 3.0 per 1,000 | WHO planning standard |
| GCC average beds | 2.0 per 1,000 | Regional comparison point |
| School-age population | 20% of total | Public reporting on student share |
| Current schools in Muscat | ~330 | Estimated from government and private schools |
| Students per school (current) | 900 | Derived from enrollment and school count |
| Quality target | 600 students/school | Planning-quality benchmark |
| Teacher:student ratio target | 15:1 | UNESCO-oriented quality target |
| Effective Muscat water capacity | 280 MLD | Estimated effective supply serving Muscat |
| Planned water addition | 300 MLD by 2025 | Al Ghubrah 3 planning assumption |
| Per-capita water use | 180 L/day | Planning assumption from public reporting |
| Water safety factor | 1.15 | Reserve margin for planning |
| Desalination capex proxy | USD 1M per MLD | Indicative cost framing only |

---

## 5. Population Projection Methodology

Population is projected using a compound annual growth model:

```text
P(t) = P(2024) x (1 + r)^(t - 2024)
```

Where:

- `P(2024)` = 1,499,549
- `r` = annual growth rate
- `t` = target year from 2024 to 2040

Scenarios:

- `Low Growth` at 1.5%
- `Base Case` at 2.5%
- `High Growth` at 4.0%

This method was chosen because it is transparent, reproducible, and appropriate for a scenario-planning exercise. A cohort-component approach would require detailed age-specific fertility, mortality, and migration inputs that were not assembled at governorate level for this project.

---

## 6. Healthcare Methodology

Healthcare demand is modeled as hospital beds required per 1,000 residents under two benchmarks:

- WHO benchmark: 3.0 beds per 1,000
- GCC comparison: 2.0 beds per 1,000

Formulas:

```text
Beds_needed(t) = Population(t) / 1000 x benchmark_rate
Gap(t) = Beds_needed(t) - Capacity(t)
```

Current Muscat capacity is estimated at 2,500 beds. The model adds 400 beds from 2028 onward, then holds capacity flat. Because current capacity is already below benchmark demand, healthcare enters the horizon with an existing deficit.

---

## 7. Education Methodology

Education demand is modeled from total population using a fixed school-age share, then converted into school and teacher requirements.

Formulas:

```text
Students(t) = Population(t) x 0.20
Schools_needed_current_density = Students(t) / 900
Schools_needed_quality = Students(t) / 600
Teachers_needed_quality = Students(t) / 15
Teacher_gap = Teachers_needed_quality - Current_teachers
```

Current capacity is represented as 330 schools at roughly 900 students per school, or about 297,000 students. The model reports needs under both current density and a stronger quality target.

---

## 8. Water Methodology

Water and utilities demand is modeled as domestic desalinated water demand in million liters per day (MLD), compared with effective Muscat supply.

Formulas:

```text
Demand_MLD(t) = Population(t) x per_capita_lpd x safety_factor / 1,000,000
Gap_MLD(t) = Demand_MLD(t) - Capacity_MLD(t)
```

Key assumptions:

- Effective Muscat supply in 2024: 280 MLD
- Planned addition from 2025: 300 MLD
- Per-capita planning assumption: 180 liters/day
- Safety factor: 1.15
- WHO minimum reference: 100 liters/day
- Gulf urban comparison range: 250 to 350 liters/day

The planned addition raises modeled capacity to 580 MLD. Under the base case that keeps Muscat in surplus through 2040, while high growth effectively exhausts the reserve.

---

## 9. Sensitivity Analysis Methodology

The population script sweeps annual growth rates from 0.5% to 5.0% in 0.5-point increments and calculates the implied 2040 population at each rate. The result is exported as `notebooks/growth_sensitivity.png`.

This is included because small changes in annual growth compound materially over 16 years, especially in a migration-sensitive city such as Muscat.

---

## 10. Gap Analysis Logic

Each sector is reported as a gap between modeled demand and available capacity:

- Healthcare: beds required minus beds available
- Education: schools and teachers required minus current supply
- Water: MLD demand minus desalination capacity

This makes the outputs decision-oriented. The model is designed to estimate additional capacity requirements, not just future demand totals.

---

## 11. Data Pipeline Description

The repository uses a simple script-to-JSON-to-dashboard pipeline.

### Step 1: Population analysis

`notebooks/population_projection.py`:

- Defines historical reference points
- Applies growth scenarios
- Exports `data/population_projections.json`
- Exports projection and sensitivity charts

### Step 2: Infrastructure analysis

`notebooks/infrastructure_analysis.py`:

- Loads `data/population_projections.json`
- Computes healthcare, education, and water results
- Exports `data/infrastructure_analysis.json`
- Exports sector charts to `notebooks/`

### Step 3: Source metadata

`data/sources.json` stores summarized source references and key values used across sectors.

### Step 4: Dashboard layer

`app.py` reads the JSON outputs and renders the interactive Streamlit interface.

---

## 12. Model Validation Approach

Validation is implemented through the automated test suite in `tests/`. The repository currently includes **22 tests** that check:

- Baseline population integrity
- Growth formula correctness
- Relative ordering of scenarios
- Healthcare demand calculations
- Education demand formulas
- Water demand and capacity calculations
- Presence of all expected sectors in JSON outputs
- Successful execution of both analysis scripts
- Creation of the expected output files

This is software-style validation: it verifies internal consistency, expected outputs, and reproducibility of the pipeline.

---

## 13. Reproduction Instructions

### Prerequisites

- Python 3.12 recommended
- `pip`

### Install dependencies

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

### Run the analysis pipeline

```bash
python3 notebooks/population_projection.py
python3 notebooks/infrastructure_analysis.py
```

### Run the dashboard

```bash
streamlit run app.py
```

### Run tests

```bash
python3 -m pytest tests/ -v
```

### Validate Streamlit app syntax

```bash
python3 -c "import ast; ast.parse(open('app.py').read()); print('Streamlit syntax OK')"
```

---

## 14. Output Artifacts

Generated data files:

- `data/population_projections.json`
- `data/infrastructure_analysis.json`
- `data/sources.json`

Generated charts:

- `notebooks/population_projection.png`
- `notebooks/growth_sensitivity.png`
- `notebooks/healthcare_analysis.png`
- `notebooks/education_analysis.png`
- `notebooks/water_analysis.png`

Primary application:

- `app.py`

---

## 15. Limitations

1. **Population model simplicity:** Exponential growth does not capture age-structure transitions or migration shocks explicitly.
2. **Infrastructure estimates:** Several Muscat-level counts are inferred from national totals and major facility references.
3. **Static future capacity:** Only explicitly modeled additions are included.
4. **Water simplification:** The water model does not separate domestic, industrial, and seasonal peak loads.
5. **Education simplification:** The school-age share is held constant through 2040.
6. **Benchmark interpretation:** WHO, UNESCO, and regional benchmarks are useful planning references but not complete service-quality measures.

---

## 16. Practical Interpretation

The model supports a clear conclusion: Muscat's base-case growth path is enough to create major infrastructure requirements by 2040. Healthcare and education require structural expansion from an already constrained baseline, while water depends on timely execution of planned desalination capacity to maintain resilience.

---

*Last updated: March 2026*
