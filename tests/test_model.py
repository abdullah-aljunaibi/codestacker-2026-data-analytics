import math
import subprocess
import sys
from pathlib import Path

import pytest


POPULATION_SCRIPT = Path("notebooks/population_projection.py")
INFRASTRUCTURE_SCRIPT = Path("notebooks/infrastructure_analysis.py")


def test_baseline_population_is_correct(population_projections_json, baseline_population):
    assert population_projections_json["baseline"]["population"] == baseline_population


def test_base_case_2040_within_range(population_projections_json, baseline_population):
    projected = population_projections_json["scenarios"]["Base Case"]["pop_2040"]
    expected = baseline_population * (1 + 0.025) ** 16
    assert projected == pytest.approx(expected, rel=0.01)


def test_high_growth_exceeds_base(population_projections_json):
    scenarios = population_projections_json["scenarios"]
    assert scenarios["High Growth"]["pop_2040"] > scenarios["Base Case"]["pop_2040"]


def test_low_growth_below_base(population_projections_json):
    scenarios = population_projections_json["scenarios"]
    assert scenarios["Low Growth"]["pop_2040"] < scenarios["Base Case"]["pop_2040"]


def test_growth_formula_compound(population_projections_json, baseline_population):
    baseline_year = population_projections_json["baseline"]["year"]

    for scenario in population_projections_json["scenarios"].values():
        rate = scenario["annual_growth_rate"]
        for year, population in scenario["yearly"].items():
            years_elapsed = int(year) - baseline_year
            expected = int(baseline_population * (1 + rate) ** years_elapsed)
            assert population == expected


def test_bed_demand_formula(population_projections_json):
    base_pop_2040 = population_projections_json["scenarios"]["Base Case"]["pop_2040"]
    benchmark_rate = 3.0
    beds_needed = base_pop_2040 / 1000 * benchmark_rate
    assert beds_needed == pytest.approx(6678.264, rel=1e-9)


def test_current_beds_below_who(baseline_population):
    current_beds_per_1000 = 2500 / (baseline_population / 1000)
    assert current_beds_per_1000 < 3.0


def test_gap_is_positive_all_scenarios(infrastructure_analysis_json):
    for scenario in infrastructure_analysis_json["healthcare"]["scenarios"].values():
        assert scenario["gap_who_2040"] > 0
        assert scenario["gap_gcc_2040"] > 0


def test_school_age_share(population_projections_json, infrastructure_analysis_json):
    share = infrastructure_analysis_json["education"]["school_age_share"]
    students_2024 = population_projections_json["baseline"]["population"] * share
    assert share == pytest.approx(0.20)
    assert students_2024 == pytest.approx(299909.8)


def test_schools_needed_formula(infrastructure_analysis_json):
    base_case = infrastructure_analysis_json["education"]["scenarios"]["Base Case"]
    quality_target = infrastructure_analysis_json["education"]["benchmarks"]["quality_target"]
    schools_needed = base_case["students_2040"] / quality_target
    assert schools_needed == pytest.approx(base_case["schools_needed_quality"], rel=0.01)


def test_teacher_gap_positive(infrastructure_analysis_json):
    for scenario in infrastructure_analysis_json["education"]["scenarios"].values():
        assert scenario["teacher_gap"] > 0
        assert scenario["teachers_needed"] > 0


def test_water_demand_formula(population_projections_json, infrastructure_analysis_json):
    base_pop_2040 = population_projections_json["scenarios"]["Base Case"]["pop_2040"]
    assumptions = infrastructure_analysis_json["water"]["assumptions"]
    demand = (
        base_pop_2040
        * assumptions["per_capita_lpd"]
        * assumptions["safety_factor"]
        / 1_000_000
    )
    assert demand == pytest.approx(
        infrastructure_analysis_json["water"]["scenarios"]["Base Case"]["demand_2040_mld"],
        rel=1e-3,
    )


def test_capacity_after_expansion(infrastructure_analysis_json):
    water = infrastructure_analysis_json["water"]
    assert water["current_capacity_mld"] + water["planned_additions_mld"] == 580
    assert water["total_after_expansion_mld"] == 580


def test_sources_json_has_all_sectors(sources_json):
    assert {"population", "healthcare", "education", "water"} <= set(sources_json)


def test_population_projections_json_has_3_scenarios(population_projections_json):
    assert set(population_projections_json["scenarios"]) == {
        "Base Case",
        "High Growth",
        "Low Growth",
    }


def test_infrastructure_analysis_json_has_3_sectors(infrastructure_analysis_json):
    assert set(infrastructure_analysis_json) == {"healthcare", "education", "water"}


def _run_script(repo_root: Path, script: Path):
    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=repo_root,
        env={"MPLBACKEND": "Agg"},
        capture_output=True,
        text=True,
        check=False,
    )
    return completed


def test_projection_script_runs_without_error(repo_root):
    result = _run_script(repo_root, POPULATION_SCRIPT)
    assert result.returncode == 0, result.stderr


def test_infrastructure_script_runs_without_error(repo_root):
    result = _run_script(repo_root, INFRASTRUCTURE_SCRIPT)
    assert result.returncode == 0, result.stderr


def test_output_files_created(repo_root):
    _run_script(repo_root, POPULATION_SCRIPT)
    _run_script(repo_root, INFRASTRUCTURE_SCRIPT)

    expected_files = [
        repo_root / "data" / "population_projections.json",
        repo_root / "data" / "infrastructure_analysis.json",
        repo_root / "data" / "sources.json",
    ]
    for file_path in expected_files:
        assert file_path.exists()
