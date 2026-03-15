"""
Muscat 2040: Growth & Infrastructure Interactive Model
Streamlit Dashboard — CodeStacker 2026 Data Analytics Challenge
Author: Abdullah Al Junaibi
"""
import json
from pathlib import Path

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Muscat 2040 — Growth & Infrastructure", layout="wide", page_icon="🏙️")

# ── LOAD GENERATED DATA (single source of truth for defaults) ──
_data_dir = Path(__file__).parent / "data"
_sources = json.loads((_data_dir / "sources.json").read_text()) if (_data_dir / "sources.json").exists() else {}
_pop_defaults = _sources.get("population", {})
_health_defaults = _sources.get("healthcare", {})
_edu_defaults = _sources.get("education", {})
_water_defaults = _sources.get("water", {})

# ── TITLE ──
st.title("🏙️ Muscat 2040: Growth & Infrastructure Model")
st.markdown("**Interactive population projection and infrastructure demand analysis for Muscat Governorate**")
st.markdown("---")

# ── SIDEBAR: ADJUSTABLE ASSUMPTIONS ──
st.sidebar.header("📊 Model Assumptions")
st.sidebar.markdown("Adjust these to see how results change dynamically.")

st.sidebar.subheader("Population")
baseline_pop = st.sidebar.number_input("Baseline Population (2024)", value=_pop_defaults.get("muscat_2024", 1_499_549), step=10000, format="%d")
low_growth = st.sidebar.slider("Low Growth Rate (%/yr)", 0.5, 4.0, 1.5, 0.1) / 100
base_growth = st.sidebar.slider("Base Case Growth Rate (%/yr)", 0.5, 6.0, 2.5, 0.1) / 100
high_growth = st.sidebar.slider("High Growth Rate (%/yr)", 0.5, 8.0, 4.0, 0.1) / 100
migration_adj = st.sidebar.slider("Net Migration Adjustment (%)", -50, 100, 0, 5)

# Enforce scenario ordering: Low ≤ Base ≤ High
if low_growth > base_growth:
    st.sidebar.warning("⚠️ Low growth rate exceeds base case — results may be misleading.")
if base_growth > high_growth:
    st.sidebar.warning("⚠️ Base case exceeds high growth rate — results may be misleading.")

st.sidebar.subheader("Healthcare")
beds_current = st.sidebar.number_input("Current Hospital Beds (Muscat)", value=_health_defaults.get("muscat_beds_estimate", 2500), step=100)
beds_planned = st.sidebar.number_input("Planned Bed Additions (by 2028)", value=400, step=50)
beds_benchmark = st.sidebar.slider("Target Beds per 1,000 People", 1.0, 5.0, float(_health_defaults.get("who_benchmark_beds_per_1000", 3.0)), 0.1)

st.sidebar.subheader("Education")
school_age_pct = st.sidebar.slider("School-Age Population (%)", 10, 30, int(_edu_defaults.get("school_age_share_of_population", 0.20) * 100), 1) / 100
schools_current = st.sidebar.number_input("Current Schools (Muscat)", value=_edu_defaults.get("muscat_schools_estimate", 330), step=10)
students_per_school = st.sidebar.slider("Students per School (current)", 400, 1200, _edu_defaults.get("students_per_school_current_density", 900), 50)
quality_target = st.sidebar.slider("Quality Target (students/school)", 300, 800, _edu_defaults.get("students_per_school_quality_target", 600), 50)
teacher_ratio = st.sidebar.slider("Target Teacher:Student Ratio", 10, 30, _edu_defaults.get("teacher_student_ratio_benchmark", 15), 1)

st.sidebar.subheader("Water & Utilities")
water_capacity_current = st.sidebar.number_input("Current Water Capacity (MLD)", value=_water_defaults.get("muscat_effective_capacity_mld_2024", 280), step=10)
water_per_capita = st.sidebar.slider("Per-Capita Water Use (L/day)", 100, 400, _water_defaults.get("per_capita_consumption_lpd", 180), 5)
water_planned_additions = st.sidebar.number_input("Planned Capacity Additions (MLD, by 2025)", value=_water_defaults.get("al_ghubrah_3_iwp_planned_mld", 300), step=10)
water_safety_factor = st.sidebar.slider("Peak/Loss Safety Factor", 1.00, 1.50, 1.15, 0.01)

# ── COMPUTE PROJECTIONS ──
years = list(range(2024, 2041))
n_years = len(years)

# Apply migration adjustment to growth rates
mig_factor = 1 + migration_adj / 100
rates = {
    "Base Case": base_growth * mig_factor,
    "High Growth": high_growth * mig_factor,
    "Low Growth": low_growth * mig_factor,
}
scenario_colors = {"Base Case": "#2196F3", "High Growth": "#FF5722", "Low Growth": "#4CAF50"}

projections = {}
for name, rate in rates.items():
    pop = [baseline_pop]
    for i in range(1, n_years):
        pop.append(pop[-1] * (1 + rate))
    projections[name] = pop

# ── SECTION 1: POPULATION ──
st.header("📈 Population Projection")
col1, col2, col3 = st.columns(3)
for col, name in zip([col1, col2, col3], rates):
    pop_2040 = projections[name][-1]
    growth_total = (pop_2040 / baseline_pop - 1) * 100
    col.metric(f"{name} (2040)", f"{pop_2040/1e6:.2f}M", f"+{growth_total:.0f}%")

fig1 = go.Figure()
for name in projections:
    fig1.add_trace(go.Scatter(
        x=years, y=[p/1e6 for p in projections[name]],
        name=f"{name} ({rates[name]*100:.1f}%/yr)",
        line=dict(color=scenario_colors[name], width=3),
        hovertemplate="%{x}: %{y:.3f}M<extra></extra>"
    ))

# Shaded range
fig1.add_trace(go.Scatter(
    x=years + years[::-1],
    y=[p/1e6 for p in projections["High Growth"]] + [p/1e6 for p in projections["Low Growth"]][::-1],
    fill='toself', fillcolor='rgba(150,150,150,0.1)',
    line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'
))

fig1.update_layout(
    title="Muscat Governorate Population Projection to 2040",
    xaxis_title="Year", yaxis_title="Population (Millions)",
    hovermode="x unified", height=450,
    legend=dict(x=0.02, y=0.98)
)
st.plotly_chart(fig1, use_container_width=True)

# ── SECTION 2: HEALTHCARE ──
st.header("🏥 Healthcare: Hospital Bed Demand")

# Capacity timeline
capacity = [beds_current if y < 2028 else beds_current + beds_planned for y in years]

col1, col2 = st.columns(2)

# Chart: demand vs capacity
fig2 = go.Figure()
for name in projections:
    demand = [p / 1000 * beds_benchmark for p in projections[name]]
    fig2.add_trace(go.Scatter(
        x=years, y=demand, name=f"{name} demand",
        line=dict(color=scenario_colors[name], width=2),
        hovertemplate="%{x}: %{y:,.0f} beds<extra></extra>"
    ))
fig2.add_trace(go.Scatter(
    x=years, y=capacity, name="Capacity (current + planned)",
    line=dict(color="black", width=3, dash="dash"),
    hovertemplate="%{x}: %{y:,.0f} beds<extra></extra>"
))
fig2.add_trace(go.Scatter(
    x=years, y=capacity, fill='tozeroy', fillcolor='rgba(76,175,80,0.08)',
    line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'
))
fig2.update_layout(
    title=f"Hospital Bed Demand ({beds_benchmark:.1f} per 1,000) vs Capacity",
    xaxis_title="Year", yaxis_title="Hospital Beds",
    hovermode="x unified", height=400
)
col1.plotly_chart(fig2, use_container_width=True)

# Gap metrics
with col2:
    st.subheader("Bed Shortfall by 2040")
    final_cap = beds_current + beds_planned
    for name in projections:
        pop_2040 = projections[name][-1]
        demand = pop_2040 / 1000 * beds_benchmark
        gap = demand - final_cap
        
        # Breakpoint
        bp = "—"
        for i, y in enumerate(years):
            if projections[name][i] / 1000 * beds_benchmark > capacity[i]:
                bp = str(y)
                break
        
        st.markdown(f"**{name}:** {int(demand):,} needed → **gap: {int(gap):,} beds** (exceeds capacity: {bp})")
    
    st.markdown("---")
    st.markdown(f"**Current ratio:** {beds_current / (baseline_pop/1000):.2f} beds/1,000")
    st.markdown(f"**Target:** {beds_benchmark:.1f} beds/1,000")

# ── SECTION 3: EDUCATION ──
st.header("🎓 Education: School Capacity")

school_capacity = schools_current * students_per_school

col1, col2 = st.columns(2)

fig3 = go.Figure()
for name in projections:
    students = [p * school_age_pct for p in projections[name]]
    fig3.add_trace(go.Scatter(
        x=years, y=[s/1000 for s in students], name=name,
        line=dict(color=scenario_colors[name], width=2),
        hovertemplate="%{x}: %{y:,.0f}K students<extra></extra>"
    ))
fig3.add_hline(y=school_capacity/1000, line_dash="dash", line_color="black",
               annotation_text=f"Current capacity ({school_capacity/1000:.0f}K)")
fig3.update_layout(
    title="School-Age Population vs Current School Capacity",
    xaxis_title="Year", yaxis_title="Students (Thousands)",
    hovermode="x unified", height=400
)
col1.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Schools & Teachers Needed by 2040")
    for name in projections:
        students_2040 = projections[name][-1] * school_age_pct
        schools_needed = int(students_2040 / quality_target)
        school_gap = schools_needed - schools_current
        teachers_needed = int(students_2040 / teacher_ratio)
        
        st.markdown(f"**{name}:**")
        st.markdown(f"  - Students: {int(students_2040):,}")
        st.markdown(f"  - Schools needed: {schools_needed} → **+{school_gap} new**")
        st.markdown(f"  - Teachers needed ({teacher_ratio}:1): **{teachers_needed:,}**")
    
    st.markdown("---")
    st.markdown(f"**Quality target:** {quality_target} students/school")

# ── SECTION 4: SENSITIVITY ANALYSIS ──
st.header("💧 Water & Utilities")

water_capacity = [water_capacity_current if y < 2025 else water_capacity_current + water_planned_additions for y in years]

col1, col2 = st.columns(2)

fig4 = go.Figure()
for name in projections:
    demand_mld = [p * water_per_capita * water_safety_factor / 1_000_000 for p in projections[name]]
    fig4.add_trace(go.Scatter(
        x=years, y=demand_mld, name=f"{name} demand",
        line=dict(color=scenario_colors[name], width=2),
        hovertemplate="%{x}: %{y:.1f} MLD<extra></extra>"
    ))
fig4.add_trace(go.Scatter(
    x=years, y=water_capacity, name="Capacity (current + planned)",
    line=dict(color="black", width=3, dash="dash"),
    hovertemplate="%{x}: %{y:.1f} MLD<extra></extra>"
))
fig4.add_trace(go.Scatter(
    x=years, y=water_capacity, fill='tozeroy', fillcolor='rgba(76,175,80,0.08)',
    line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'
))
fig4.update_layout(
    title="Water Demand vs Desalination Capacity",
    xaxis_title="Year", yaxis_title="Water Demand (MLD)",
    hovermode="x unified", height=400
)
col1.plotly_chart(fig4, use_container_width=True)

with col2:
    st.subheader("Water Gap by 2040")
    final_water_capacity = water_capacity_current + water_planned_additions
    for name in projections:
        demand_2040 = projections[name][-1] * water_per_capita * water_safety_factor / 1_000_000
        water_gap = demand_2040 - final_water_capacity
        investment_needed = max(water_gap, 0) * 1_000_000

        bp = "—"
        for i, y in enumerate(years):
            demand_year = projections[name][i] * water_per_capita * water_safety_factor / 1_000_000
            if demand_year > water_capacity[i]:
                bp = str(y)
                break

        st.markdown(
            f"**{name}:** {demand_2040:.1f} MLD needed → "
            f"**gap: {water_gap:+.1f} MLD** (exceeds capacity: {bp}, investment: ${investment_needed/1e6:,.1f}M)"
        )

    st.markdown("---")
    st.markdown(f"**Current effective capacity:** {water_capacity_current:.0f} MLD")
    st.markdown("**Reference range:** WHO minimum 100 L/day, Gulf standard 250-350 L/day")

# ── SECTION 5: SENSITIVITY ANALYSIS ──
st.header("🔄 Sensitivity Analysis")
st.markdown("How does the growth rate affect 2040 outcomes?")

test_rates = np.arange(0.005, 0.06, 0.005)
fig5 = make_subplots(rows=1, cols=4,
                     subplot_titles=["Population 2040", "Bed Gap 2040", "School Gap 2040", "Water Gap 2040"])

pops = [baseline_pop * (1 + r) ** 16 for r in test_rates]
bed_gaps = [p / 1000 * beds_benchmark - (beds_current + beds_planned) for p in pops]
school_gaps = [int(p * school_age_pct / quality_target) - schools_current for p in pops]
water_gaps = [p * water_per_capita * water_safety_factor / 1_000_000 - (water_capacity_current + water_planned_additions) for p in pops]
labels = [f"{r*100:.1f}%" for r in test_rates]

bar_colors = ['#4CAF50' if r < 0.02 else '#2196F3' if r < 0.035 else '#FF5722' for r in test_rates]

fig5.add_trace(go.Bar(x=labels, y=[p/1e6 for p in pops], marker_color=bar_colors, showlegend=False), row=1, col=1)
fig5.add_trace(go.Bar(x=labels, y=bed_gaps, marker_color=bar_colors, showlegend=False), row=1, col=2)
fig5.add_trace(go.Bar(x=labels, y=school_gaps, marker_color=bar_colors, showlegend=False), row=1, col=3)
fig5.add_trace(go.Bar(x=labels, y=water_gaps, marker_color=bar_colors, showlegend=False), row=1, col=4)

fig5.update_layout(height=400, title_text="Sensitivity to Annual Growth Rate")
fig5.update_xaxes(title_text="Growth Rate", row=1, col=2)
fig5.update_yaxes(title_text="Millions", row=1, col=1)
fig5.update_yaxes(title_text="Bed Deficit", row=1, col=2)
fig5.update_yaxes(title_text="Schools Needed", row=1, col=3)
fig5.update_yaxes(title_text="MLD Gap", row=1, col=4)

st.plotly_chart(fig5, use_container_width=True)

# ── SECTION 6: KEY FINDINGS ──
st.header("📋 Key Findings")

base_pop_2040 = projections["Base Case"][-1]
base_bed_gap = base_pop_2040 / 1000 * beds_benchmark - (beds_current + beds_planned)
base_school_gap = int(base_pop_2040 * school_age_pct / quality_target) - schools_current
base_water_demand = base_pop_2040 * water_per_capita * water_safety_factor / 1_000_000
base_water_gap = base_water_demand - (water_capacity_current + water_planned_additions)

st.markdown(f"""
| Metric | 2024 (Current) | 2040 Base Case | Gap |
|--------|---------------|----------------|-----|
| **Population** | {baseline_pop:,} | {int(base_pop_2040):,} | +{int(base_pop_2040 - baseline_pop):,} |
| **Hospital Beds** | {beds_current:,} | {int(base_pop_2040/1000*beds_benchmark):,} needed | **{int(base_bed_gap):,} deficit** |
| **Schools** | {schools_current} | {int(base_pop_2040*school_age_pct/quality_target)} needed | **+{base_school_gap} new** |
| **Teachers** | ~{int(baseline_pop*school_age_pct/20):,} | {int(base_pop_2040*school_age_pct/teacher_ratio):,} needed | +{int(base_pop_2040*school_age_pct/teacher_ratio - baseline_pop*school_age_pct/20):,} |
| **Water Capacity** | {water_capacity_current:.0f} MLD | {base_water_demand:.1f} MLD needed | **{base_water_gap:+.1f} MLD** |
""")

st.markdown("---")
st.caption("Data sources: NCSI Oman, WHO, UNESCO, Oman Observer, Times of Oman, ONA, PAEW, OPWP | Built for CodeStacker 2026")
