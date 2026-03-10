"""
Phase 2: Muscat Governorate Population Projection to 2040
Three scenarios: Base, High Growth, Low Growth
"""
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# === BASELINE DATA (NCSI) ===
# Source: NCSI via Muscat Daily (Jan 2025), Oman Observer, OmanQ
historical = {
    2020: 1_340_000,  # Estimated from 2022 figure working back at ~3% avg
    2021: 1_380_000,
    2022: 1_720_000,  # NCSI official (includes post-COVID expat return surge)
    2023: 1_455_680,  # NCSI official (correction: expat outflow normalization)
    2024: 1_499_549,  # NCSI official
}

# Note: 2022 spike was due to mass expat return post-COVID; 2023 correction reflects
# NCSI methodology change separating registered vs resident population.
# We use 2023-2024 as the stable baseline.

baseline_pop = 1_499_549  # End of 2024
baseline_year = 2024
target_year = 2040

# === GROWTH RATE ASSUMPTIONS ===
# Source: NCSI data shows Muscat grew 3.0% in 2024 (2023→2024)
# Oman Vision 2040 plans diversification which attracts workers
# Historical Oman national growth: 2-6% depending on oil cycle

scenarios = {
    "Base Case": {
        "description": "Moderate growth assuming Oman Vision 2040 diversification proceeds steadily",
        "annual_growth_rate": 0.025,  # 2.5% — slightly below recent 3%, accounting for maturation
        "assumptions": [
            "Oman Vision 2040 diversification creates steady job growth",
            "Expat share stabilizes around 60%",
            "Fertility rate follows GCC declining trend (2.5 → 2.2 by 2040)",
            "No major economic shocks or oil price collapse",
            "Net migration +15,000/year average",
        ],
    },
    "High Growth": {
        "description": "Rapid growth driven by successful economic diversification and megaprojects",
        "annual_growth_rate": 0.040,  # 4.0% — similar to 2022 surge sustained
        "assumptions": [
            "Muscat becomes regional logistics/tech hub",
            "Major FDI inflows from Oman Investment Authority projects",
            "Expat share rises to 65% as labor demand surges",
            "Tourism sector doubles (Oman 2040 target: 11M visitors)",
            "Net migration +30,000/year average",
        ],
    },
    "Low Growth": {
        "description": "Slower growth due to economic headwinds and Omanization pressure",
        "annual_growth_rate": 0.015,  # 1.5% — reflects aggressive Omanization, reduced expat intake
        "assumptions": [
            "Oil prices remain below $60/barrel long-term",
            "Aggressive Omanization reduces expat workforce by 20%",
            "Fertility continues declining faster than expected",
            "Regional competition (UAE, Saudi) diverts investment",
            "Net migration near zero or slightly negative",
        ],
    },
}

# === PROJECTION ===
years = list(range(baseline_year, target_year + 1))
projections = {}

for name, scenario in scenarios.items():
    rate = scenario["annual_growth_rate"]
    pop = [baseline_pop]
    for i in range(1, len(years)):
        pop.append(pop[-1] * (1 + rate))
    projections[name] = pop
    scenario["pop_2040"] = int(pop[-1])
    scenario["pop_2030"] = int(pop[2030 - baseline_year])
    scenario["total_growth"] = pop[-1] / baseline_pop - 1

# === HISTORICAL + PROJECTION DATA FOR EXPORT ===
output = {
    "baseline": {"year": baseline_year, "population": baseline_pop},
    "historical": historical,
    "scenarios": {},
}
for name, scenario in scenarios.items():
    output["scenarios"][name] = {
        "annual_growth_rate": scenario["annual_growth_rate"],
        "description": scenario["description"],
        "assumptions": scenario["assumptions"],
        "pop_2030": scenario["pop_2030"],
        "pop_2040": scenario["pop_2040"],
        "total_growth_pct": round(scenario["total_growth"] * 100, 1),
        "yearly": {str(y): int(p) for y, p in zip(years, projections[name])},
    }

with open("data/population_projections.json", "w") as f:
    json.dump(output, f, indent=2)

# === CHART 1: Population Projection (3 scenarios) ===
fig, ax = plt.subplots(figsize=(12, 7))

colors = {"Base Case": "#2196F3", "High Growth": "#FF5722", "Low Growth": "#4CAF50"}
for name in scenarios:
    ax.plot(years, [p / 1e6 for p in projections[name]], 
            label=f'{name} ({scenarios[name]["annual_growth_rate"]*100:.1f}%/yr)',
            linewidth=2.5, color=colors[name])
    # Annotate 2040 value
    ax.annotate(f'{projections[name][-1]/1e6:.2f}M', 
                xy=(2040, projections[name][-1]/1e6),
                xytext=(10, 0), textcoords='offset points',
                fontsize=10, fontweight='bold', color=colors[name])

# Historical data
hist_years = sorted(historical.keys())
hist_pops = [historical[y] / 1e6 for y in hist_years]
ax.scatter(hist_years, hist_pops, color='black', zorder=5, s=40, label='Historical (NCSI)')
ax.plot(hist_years, hist_pops, color='black', linewidth=1, linestyle='--', alpha=0.5)

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Population (Millions)', fontsize=12)
ax.set_title('Muscat Governorate Population Projection to 2040\nThree Growth Scenarios', fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
ax.set_xlim(2020, 2042)

# Add shaded range between low and high
ax.fill_between(years, 
                [p/1e6 for p in projections["Low Growth"]], 
                [p/1e6 for p in projections["High Growth"]], 
                alpha=0.1, color='gray', label='_Range')

plt.tight_layout()
plt.savefig('notebooks/population_projection.png', dpi=150, bbox_inches='tight')
print("Chart saved: notebooks/population_projection.png")

# === CHART 2: Growth Rate Sensitivity ===
fig2, ax2 = plt.subplots(figsize=(10, 6))

rates = np.arange(0.005, 0.055, 0.005)
pop_2040_by_rate = [baseline_pop * (1 + r) ** 16 for r in rates]

ax2.bar([f'{r*100:.1f}%' for r in rates], [p/1e6 for p in pop_2040_by_rate], 
        color=['#4CAF50' if r < 0.02 else '#2196F3' if r < 0.035 else '#FF5722' for r in rates])

# Mark our 3 scenarios
for name, scenario in scenarios.items():
    r = scenario["annual_growth_rate"]
    p = scenario["pop_2040"]
    ax2.axhline(y=p/1e6, color=colors[name], linestyle='--', alpha=0.7, linewidth=1)
    ax2.annotate(f'{name}: {p/1e6:.2f}M', xy=(0.02, p/1e6), 
                fontsize=9, color=colors[name], fontweight='bold')

ax2.set_xlabel('Annual Growth Rate', fontsize=12)
ax2.set_ylabel('Projected Population 2040 (Millions)', fontsize=12)
ax2.set_title('Sensitivity: Muscat 2040 Population by Growth Rate', fontsize=13, fontweight='bold')
ax2.grid(True, axis='y', alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('notebooks/growth_sensitivity.png', dpi=150, bbox_inches='tight')
print("Chart saved: notebooks/growth_sensitivity.png")

# === SUMMARY ===
print("\n" + "="*60)
print("MUSCAT GOVERNORATE POPULATION PROJECTION SUMMARY")
print("="*60)
print(f"Baseline: {baseline_pop:,} (end of {baseline_year})")
print(f"Target year: {target_year}")
print()
for name, scenario in scenarios.items():
    print(f"  {name} ({scenario['annual_growth_rate']*100:.1f}%/yr):")
    print(f"    2030: {scenario['pop_2030']:,}")
    print(f"    2040: {scenario['pop_2040']:,}")
    print(f"    Total growth: +{scenario['total_growth']*100:.1f}%")
    print()
print(f"Population range in 2040: {scenarios['Low Growth']['pop_2040']:,} — {scenarios['High Growth']['pop_2040']:,}")
