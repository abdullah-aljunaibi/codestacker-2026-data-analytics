"""
Phase 3: Infrastructure Demand Analysis — Healthcare + Education
Muscat Governorate to 2040
"""
import json
import matplotlib.pyplot as plt
import numpy as np

# Load projections
with open("data/population_projections.json") as f:
    proj = json.load(f)

baseline_year = 2024
years = list(range(baseline_year, 2041))

scenarios = {}
for name, s in proj["scenarios"].items():
    scenarios[name] = [s["yearly"][str(y)] for y in years]

colors = {"Base Case": "#2196F3", "High Growth": "#FF5722", "Low Growth": "#4CAF50"}

# ============================================================
# SECTOR 1: HEALTHCARE
# ============================================================
# Current capacity (Muscat Governorate)
# Source: ONA (Aug 2024) — 92 hospitals nationally, 7,691 beds
# Muscat has ~32% of beds (capital concentration + referral hospitals)
# Royal Hospital (590 beds), Sultan Qaboos University Hospital (524 beds),
# Al Nahda Hospital (300 beds), Khoula Hospital (360 beds) — all in Muscat
# Plus private hospitals: ~800 beds
# Estimate: ~2,500 total beds in Muscat governorate

MUSCAT_BEDS_CURRENT = 2500
MUSCAT_BEDS_YEAR = 2024

# Planned additions: 11 new hospitals nationally under construction
# Assume ~400 new beds reach Muscat by 2028 (new Muscat hospital projects)
PLANNED_BEDS_ADDITION = 400
PLANNED_BEDS_YEAR = 2028

# Benchmarks
WHO_BEDS_PER_1000 = 3.0        # WHO recommended minimum
GCC_AVG_BEDS_PER_1000 = 2.0    # GCC average (UAE 1.8, Saudi 2.2, Kuwait 2.0)
OMAN_CURRENT_BEDS_PER_1000 = 1.46  # National average

# Demand calculation
health_data = {"years": years}
for name in scenarios:
    pop = scenarios[name]
    # Demand at WHO benchmark
    demand_who = [p / 1000 * WHO_BEDS_PER_1000 for p in pop]
    # Demand at GCC average
    demand_gcc = [p / 1000 * GCC_AVG_BEDS_PER_1000 for p in pop]
    
    health_data[f"{name}_demand_who"] = demand_who
    health_data[f"{name}_demand_gcc"] = demand_gcc

# Capacity timeline (current + planned)
capacity = []
for y in years:
    if y < PLANNED_BEDS_YEAR:
        capacity.append(MUSCAT_BEDS_CURRENT)
    else:
        capacity.append(MUSCAT_BEDS_CURRENT + PLANNED_BEDS_ADDITION)
health_data["capacity"] = capacity

# Find breakpoint years
print("=" * 60)
print("HEALTHCARE ANALYSIS — Hospital Beds")
print("=" * 60)
print(f"Current capacity: {MUSCAT_BEDS_CURRENT} beds ({MUSCAT_BEDS_YEAR})")
print(f"Planned additions: +{PLANNED_BEDS_ADDITION} beds by {PLANNED_BEDS_YEAR}")
print(f"Post-expansion capacity: {MUSCAT_BEDS_CURRENT + PLANNED_BEDS_ADDITION} beds")
print(f"\nBenchmarks: WHO = {WHO_BEDS_PER_1000}/1000, GCC avg = {GCC_AVG_BEDS_PER_1000}/1000")
print()

health_results = {}
for name in scenarios:
    pop_2040 = scenarios[name][-1]
    demand_who_2040 = pop_2040 / 1000 * WHO_BEDS_PER_1000
    demand_gcc_2040 = pop_2040 / 1000 * GCC_AVG_BEDS_PER_1000
    final_cap = MUSCAT_BEDS_CURRENT + PLANNED_BEDS_ADDITION
    gap_who = demand_who_2040 - final_cap
    gap_gcc = demand_gcc_2040 - final_cap
    
    # Find year when GCC-level demand exceeds capacity
    breakpoint = None
    for i, y in enumerate(years):
        cap = capacity[i]
        demand = scenarios[name][i] / 1000 * GCC_AVG_BEDS_PER_1000
        if demand > cap and breakpoint is None:
            breakpoint = y
    
    health_results[name] = {
        "pop_2040": pop_2040,
        "demand_who_2040": int(demand_who_2040),
        "demand_gcc_2040": int(demand_gcc_2040),
        "gap_who_2040": int(gap_who),
        "gap_gcc_2040": int(gap_gcc),
        "breakpoint_gcc": breakpoint,
    }
    
    print(f"  {name}:")
    print(f"    Pop 2040: {pop_2040:,}")
    print(f"    Beds needed (WHO 3.0): {int(demand_who_2040):,} → gap: {int(gap_who):,}")
    print(f"    Beds needed (GCC 2.0): {int(demand_gcc_2040):,} → gap: {int(gap_gcc):,}")
    if breakpoint:
        print(f"    ⚠️  GCC-level demand exceeds capacity in {breakpoint}")
    print()

# === CHART: Healthcare ===
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Left: Demand vs Capacity (WHO benchmark)
for name in scenarios:
    demand = [p / 1000 * WHO_BEDS_PER_1000 for p in scenarios[name]]
    ax1.plot(years, demand, label=f'{name} demand', color=colors[name], linewidth=2)

ax1.plot(years, capacity, 'k--', linewidth=2.5, label='Current + planned capacity')
ax1.fill_between(years, 0, capacity, alpha=0.08, color='green')
ax1.set_title('Hospital Beds: Demand (WHO 3.0/1000) vs Capacity', fontsize=12, fontweight='bold')
ax1.set_xlabel('Year')
ax1.set_ylabel('Hospital Beds')
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(2024, 2040)

# Right: Gap by 2040
scenario_names = list(scenarios.keys())
gaps_who = [health_results[n]["gap_who_2040"] for n in scenario_names]
gaps_gcc = [health_results[n]["gap_gcc_2040"] for n in scenario_names]

x = np.arange(len(scenario_names))
w = 0.35
ax2.bar(x - w/2, gaps_who, w, label='Gap (WHO 3.0)', color='#E53935')
ax2.bar(x + w/2, gaps_gcc, w, label='Gap (GCC 2.0)', color='#FF9800')
ax2.set_xticks(x)
ax2.set_xticklabels(scenario_names)
ax2.set_title('Hospital Bed Shortfall by 2040', fontsize=12, fontweight='bold')
ax2.set_ylabel('Bed Deficit')
ax2.legend()
ax2.grid(True, axis='y', alpha=0.3)

for i, (gw, gg) in enumerate(zip(gaps_who, gaps_gcc)):
    ax2.text(i - w/2, gw + 50, f'{gw:,}', ha='center', fontsize=9, fontweight='bold')
    ax2.text(i + w/2, gg + 50, f'{gg:,}', ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('notebooks/healthcare_analysis.png', dpi=150, bbox_inches='tight')
print("Chart saved: notebooks/healthcare_analysis.png")

# ============================================================
# SECTOR 2: EDUCATION
# ============================================================
print("\n" + "=" * 60)
print("EDUCATION ANALYSIS — School Capacity")
print("=" * 60)

# Current data
# Source: Oman Observer (Mar 2023) — 710,000 students nationally = 20% of pop
# Source: NCSI — Muscat has ~30% of population
# Muscat estimated school-age students: ~300,000 (2024)
# Schools in Muscat: ~250 govt + ~80 private = ~330 schools
# Avg students per school: ~900

SCHOOL_AGE_SHARE = 0.20          # 20% of population is school-age (5-18)
MUSCAT_SCHOOLS_CURRENT = 330     # Government + private schools
MUSCAT_SCHOOL_CAPACITY = 330 * 900  # ~297,000 students
STUDENTS_PER_SCHOOL = 900        # Current average
IDEAL_STUDENTS_PER_SCHOOL = 600  # UNESCO quality benchmark
TEACHER_STUDENT_RATIO = 20       # Current Oman average
IDEAL_TEACHER_RATIO = 15         # UNESCO quality benchmark

print(f"Current schools: {MUSCAT_SCHOOLS_CURRENT}")
print(f"Current capacity: ~{MUSCAT_SCHOOL_CAPACITY:,} students (at {STUDENTS_PER_SCHOOL}/school)")
print(f"School-age share: {SCHOOL_AGE_SHARE*100:.0f}% of population")
print(f"Quality benchmark: {IDEAL_STUDENTS_PER_SCHOOL} students/school")
print()

edu_results = {}
for name in scenarios:
    pop_2040 = scenarios[name][-1]
    students_2024 = scenarios[name][0] * SCHOOL_AGE_SHARE
    students_2040 = pop_2040 * SCHOOL_AGE_SHARE
    
    # Schools needed at current density
    schools_needed_current = students_2040 / STUDENTS_PER_SCHOOL
    # Schools needed at quality benchmark
    schools_needed_quality = students_2040 / IDEAL_STUDENTS_PER_SCHOOL
    
    gap_current = schools_needed_current - MUSCAT_SCHOOLS_CURRENT
    gap_quality = schools_needed_quality - MUSCAT_SCHOOLS_CURRENT
    
    # Teachers needed
    teachers_2040 = students_2040 / IDEAL_TEACHER_RATIO
    teachers_current = students_2024 / TEACHER_STUDENT_RATIO
    teacher_gap = teachers_2040 - teachers_current
    
    # Breakpoint: when does demand exceed current capacity?
    breakpoint = None
    for i, y in enumerate(years):
        demand = scenarios[name][i] * SCHOOL_AGE_SHARE
        if demand > MUSCAT_SCHOOL_CAPACITY and breakpoint is None:
            breakpoint = y
    
    edu_results[name] = {
        "students_2024": int(students_2024),
        "students_2040": int(students_2040),
        "schools_needed_current": int(schools_needed_current),
        "schools_needed_quality": int(schools_needed_quality),
        "gap_current": int(gap_current),
        "gap_quality": int(gap_quality),
        "teachers_needed": int(teachers_2040),
        "teacher_gap": int(teacher_gap),
        "breakpoint": breakpoint,
    }
    
    print(f"  {name}:")
    print(f"    Students 2040: {int(students_2040):,}")
    print(f"    Schools needed (current density): {int(schools_needed_current)} → gap: +{int(gap_current)}")
    print(f"    Schools needed (quality target):  {int(schools_needed_quality)} → gap: +{int(gap_quality)}")
    print(f"    Teachers needed (15:1 ratio): {int(teachers_2040):,} → +{int(teacher_gap):,} new")
    if breakpoint:
        print(f"    ⚠️  Capacity exceeded in {breakpoint}")
    print()

# === CHART: Education ===
fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(16, 7))

# Left: Student population over time
for name in scenarios:
    students = [p * SCHOOL_AGE_SHARE for p in scenarios[name]]
    ax3.plot(years, [s/1000 for s in students], label=name, color=colors[name], linewidth=2)

ax3.axhline(y=MUSCAT_SCHOOL_CAPACITY/1000, color='black', linestyle='--', linewidth=2, label=f'Current capacity ({MUSCAT_SCHOOL_CAPACITY/1000:.0f}K)')
ax3.fill_between(years, 0, [MUSCAT_SCHOOL_CAPACITY/1000]*len(years), alpha=0.08, color='green')
ax3.set_title('School-Age Population vs School Capacity', fontsize=12, fontweight='bold')
ax3.set_xlabel('Year')
ax3.set_ylabel('Students (Thousands)')
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)

# Right: School gap by 2040
names = list(edu_results.keys())
gap_curr = [edu_results[n]["gap_current"] for n in names]
gap_qual = [edu_results[n]["gap_quality"] for n in names]

x = np.arange(len(names))
w = 0.35
ax4.bar(x - w/2, gap_curr, w, label='Gap (current density)', color='#1976D2')
ax4.bar(x + w/2, gap_qual, w, label='Gap (quality target)', color='#7B1FA2')
ax4.set_xticks(x)
ax4.set_xticklabels(names)
ax4.set_title('Additional Schools Needed by 2040', fontsize=12, fontweight='bold')
ax4.set_ylabel('Schools Needed')
ax4.legend()
ax4.grid(True, axis='y', alpha=0.3)

for i, (gc, gq) in enumerate(zip(gap_curr, gap_qual)):
    ax4.text(i - w/2, gc + 5, f'+{gc}', ha='center', fontsize=10, fontweight='bold')
    ax4.text(i + w/2, gq + 5, f'+{gq}', ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('notebooks/education_analysis.png', dpi=150, bbox_inches='tight')
print("Chart saved: notebooks/education_analysis.png")

# === SAVE ALL RESULTS ===
all_results = {
    "healthcare": {
        "current_beds": MUSCAT_BEDS_CURRENT,
        "planned_additions": PLANNED_BEDS_ADDITION,
        "total_after_expansion": MUSCAT_BEDS_CURRENT + PLANNED_BEDS_ADDITION,
        "benchmarks": {"WHO": WHO_BEDS_PER_1000, "GCC_avg": GCC_AVG_BEDS_PER_1000},
        "scenarios": health_results,
    },
    "education": {
        "current_schools": MUSCAT_SCHOOLS_CURRENT,
        "current_capacity": MUSCAT_SCHOOL_CAPACITY,
        "school_age_share": SCHOOL_AGE_SHARE,
        "benchmarks": {"current_density": STUDENTS_PER_SCHOOL, "quality_target": IDEAL_STUDENTS_PER_SCHOOL},
        "scenarios": edu_results,
    },
}

with open("data/infrastructure_analysis.json", "w") as f:
    json.dump(all_results, f, indent=2, default=str)
print("\nResults saved: data/infrastructure_analysis.json")
