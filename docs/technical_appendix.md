# Technical Appendix — Muscat 2040 Growth & Infrastructure Model

---

## 1. Data Sources

| Source | Data Used | URL |
|--------|-----------|-----|
| NCSI (via Muscat Daily, Jan 2025) | Muscat population 2024: 1,499,549; 3.0% growth | https://www.muscatdaily.com/2025/01/26/oman-population-increases-2-to-5-268mn-in-2024/ |
| NCSI (via Oman Observer, Oct 2023) | National population growth 6.1% Q3 2023 | https://www.omanobserver.om/article/1144777/ |
| NCSI (via Oman Observer, Jan 2024) | Muscat = 29.7% of national, 1,546,667 residents | https://www.omanobserver.om/article/1147705/ |
| NCSI (via OmanQ, Mar 2025) | Muscat pop 1,499,549; Omanis 584,092 (39%) | https://omanq.com/news/muscats-population-surpasses-1-5-million/ |
| Wikipedia / NCSI | Muscat 2022 population: ~1.72M | https://en.wikipedia.org/wiki/Muscat |
| Oman News Agency (Aug 2024) | 92 hospitals nationally, 7,691 beds | https://omannews.gov.om/topics/en/79/show/118135/ |
| Grokipedia / MoH | MoH manages 50 hospitals with 5,024 beds (2023) | https://grokipedia.com/page/List_of_hospitals_in_Oman |
| Times of Oman / Oman Observer (May 2023) | 11 new hospitals under construction | https://www.omanobserver.om/article/1136940/ |
| Oman Observer (Mar 2023) | 710,000 students nationally = 20% of population | https://www.omanobserver.om/article/1133871/ |
| Oman Observer (Aug 2024) | 46 international schools, 61,704 students, 21 in Muscat | https://www.omanobserver.om/article/1157275/ |
| WHO | Hospital beds benchmark: 3.0 per 1,000 population | https://www.who.int/data/gho |
| UNESCO | Quality education benchmarks: teacher ratios, class sizes | https://uis.unesco.org/ |

---

## 2. Assumptions Table

| Assumption | Value | Justification |
|-----------|-------|---------------|
| Baseline population | 1,499,549 (end 2024) | NCSI official figure |
| Base growth rate | 2.5%/yr | Slightly below recent 3.0%, accounting for maturation |
| High growth rate | 4.0%/yr | Reflects successful Vision 2040 diversification |
| Low growth rate | 1.5%/yr | Aggressive Omanization, low oil prices scenario |
| Expat share | ~61% | NCSI 2024 data |
| Muscat hospital beds | ~2,500 | Estimated from national total (7,691) × Muscat share (~32%) + known major hospitals (Royal 590, SQUH 524, Khoula 360, Al Nahda 300) |
| Planned bed additions | 400 by 2028 | Based on announced hospital construction projects in Muscat area |
| WHO beds benchmark | 3.0 per 1,000 | WHO global standard |
| GCC average beds | 2.0 per 1,000 | Regional average (UAE 1.8, Saudi 2.2, Kuwait 2.0) |
| School-age population | 20% of total | NCSI/Oman Observer: 710K students out of ~3.5M national population |
| Current schools in Muscat | ~330 | Estimated from government + private school counts |
| Students per school (current) | 900 | Derived: ~300,000 students ÷ 330 schools |
| Quality target | 600 students/school | UNESCO quality benchmark for class sizes |
| Teacher:student ratio target | 15:1 | UNESCO recommended ratio |

---

## 3. Calculation Methodology

### Population Projection

Compound annual growth model:

```
P(t) = P(2024) × (1 + r)^(t - 2024)
```

Where:
- `P(2024)` = 1,499,549 (NCSI baseline)
- `r` = annual growth rate (varies by scenario)
- `t` = target year (2024–2040)

**Why this method:** Simple exponential growth is appropriate for 16-year projections when the growth rate is the primary variable. More complex models (cohort-component) would require age-structure data unavailable at the governorate level. The three-scenario approach captures uncertainty without false precision.

### Healthcare Demand

```
Beds_needed(t) = P(t) / 1000 × benchmark_rate
Gap(t) = Beds_needed(t) - Capacity(t)
```

Capacity increases by 400 beds in 2028 (planned construction), then remains flat — a conservative assumption that highlights the investment needed.

### Education Demand

```
Students(t) = P(t) × 0.20  (school-age share)
Schools_needed(t) = Students(t) / target_density
Teacher_gap(t) = Students(t) / target_ratio - current_teachers
```

### Sensitivity Analysis

Sweeps growth rate from 0.5% to 5.5% in 0.5% increments, computing all metrics at each rate. Visualized as bar charts in the interactive model.

---

## 4. Reproduction Instructions

### Prerequisites
- Python 3.10+
- pip

### Setup
```bash
git clone https://github.com/abdullah-aljunaibi/codestacker-2026-data-analytics.git
cd codestacker-2026-data-analytics
pip install -r requirements.txt
```

### Run the Interactive Model
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`. Use the sidebar sliders to adjust assumptions.

### Run the Analysis Scripts
```bash
python3 notebooks/population_projection.py    # Generates projection charts
python3 notebooks/infrastructure_analysis.py  # Generates infrastructure charts
```

### Output Files
- `data/population_projections.json` — All projection data
- `data/infrastructure_analysis.json` — Healthcare + education analysis
- `notebooks/*.png` — Static charts
- `app.py` — Interactive Streamlit dashboard

---

## 5. Limitations

1. **Population model simplicity:** Exponential growth doesn't capture age-structure transitions, which matter for education demand specifically.
2. **Muscat bed count is estimated:** No official governorate-level bed count was found; we derived from national data and known hospital capacities.
3. **Static capacity:** We only model announced bed additions (400 by 2028). Actual government investment may differ.
4. **Expat volatility:** Expat population (61% of Muscat) is highly sensitive to economic cycles and visa policies — a risk not fully captured in smooth growth rates.
5. **Education data gaps:** School counts by governorate are estimated; official NCSI data at governorate level was not publicly accessible.

---

*Last updated: March 2026*
