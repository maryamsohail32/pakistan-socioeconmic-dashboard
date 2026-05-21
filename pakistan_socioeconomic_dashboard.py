# ============================================================
#   PAKISTAN SOCIOECONOMIC DASHBOARD
#   Lab 7 — Open Ended Project
# ============================================================

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime


# ─────────────────────────────────────────────
#  LAB 1 — Variables & Data Types
#  Named constants used throughout the project
# ─────────────────────────────────────────────

PROJECT_TITLE  = "Pakistan Socioeconomic Dashboard"   # str
START_YEAR     = 2019                                  # int
END_YEAR       = 2024                                  # int
ESI_CRITICAL   = 60.0                                  # float — stress threshold
ESI_HIGH       = 40.0                                  # float
ESI_MODERATE   = 25.0                                  # float
CITIES         = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta"]  # list
DATA_SOURCES   = {"national": "SBP / PBS / World Bank", "city": "PBS 2024"}  # dict


# ─────────────────────────────────────────────
#  LAB 3 — OOP: Base Class
# ─────────────────────────────────────────────

class EconomicIndicator:
    """
    Base class representing a single economic indicator tracked over time.
    Demonstrates: __init__, instance attributes, instance methods, __repr__
    """

    def __init__(self, name: str, unit: str, data: dict):
        """
        Args:
            name : Indicator name e.g. 'Inflation Rate'
            unit : Unit string e.g. '%', 'PKR/USD'
            data : {year (int): value (float)} dictionary  ← Lab 4
        """
        self.name = name          # str attribute
        self.unit = unit          # str attribute
        self.data = data          # dict attribute — Lab 4

    # Instance method — returns sorted list of years
    def get_years(self) -> list:
        return sorted(self.data.keys())   # list — Lab 4

    # Instance method — returns values in year order
    def get_values(self) -> list:
        return [self.data[yr] for yr in self.get_years()]   # list comprehension

    # Instance method — returns most recent (year, value) tuple
    def latest(self) -> tuple:
        latest_year = max(self.data.keys())   # Lab 2 — uses built-in max
        return latest_year, self.data[latest_year]

    # Dunder method for readable object representation
    def __repr__(self) -> str:
        yr, val = self.latest()
        return f"<EconomicIndicator | {self.name}: {val}{self.unit} ({yr})>"


# ─────────────────────────────────────────────
#  LAB 3 — OOP: Subclass (Inheritance)
# ─────────────────────────────────────────────

class CityIndicator(EconomicIndicator):
    """
    Subclass of EconomicIndicator that also stores city-level data.
    Demonstrates: inheritance, super(), method extension
    """

    def __init__(self, name: str, unit: str, data: dict, city_data: dict):
        super().__init__(name, unit, data)   # call parent __init__
        self.city_data = city_data           # extra attribute: {city: {year: value}}

    # Extended method — get latest value for a specific city
    def get_city_latest(self, city: str) -> tuple:
        if city not in self.city_data:
            return None
        city_years = self.city_data[city]
        latest_year = max(city_years.keys())
        return latest_year, city_years[latest_year]

    # Get all city values for a given year
    def get_city_values_for_year(self, year: int) -> dict:
        result = {}
        for city, years_dict in self.city_data.items():
            if year in years_dict:
                result[city] = years_dict[year]
        return result


# ─────────────────────────────────────────────
#  LAB 4 — Data Structures: Dictionaries & Lists
# ─────────────────────────────────────────────

# Dictionary: {year: value} for each national indicator
inflation = EconomicIndicator(
    name="Inflation Rate", unit="%",
    data={2019: 6.8, 2020: 10.7, 2021: 8.9,
          2022: 12.2, 2023: 29.2, 2024: 23.4}
)

rupee_rate = EconomicIndicator(
    name="PKR/USD Exchange Rate", unit=" PKR",
    data={2019: 150.0, 2020: 168.0, 2021: 176.0,
          2022: 204.0, 2023: 285.0, 2024: 278.0}
)

unemployment = EconomicIndicator(
    name="Unemployment Rate", unit="%",
    data={2019: 4.1, 2020: 4.5, 2021: 6.0,
          2022: 6.2, 2023: 8.5, 2024: 7.9}
)

gdp_growth = EconomicIndicator(
    name="GDP Growth Rate", unit="%",
    data={2019: 1.9, 2020: -0.5, 2021: 5.7,
          2022: 6.1, 2023: -0.2, 2024: 2.4}
)

# Subclass instance: city-level unemployment data
city_unemployment = CityIndicator(
    name="City Unemployment Rate", unit="%",
    data={2019: 4.1, 2020: 4.5, 2021: 6.0,
          2022: 6.2, 2023: 8.5, 2024: 7.9},
    city_data={
        "Karachi":   {2022: 7.1, 2023: 9.2, 2024: 8.6},
        "Lahore":    {2022: 5.8, 2023: 8.0, 2024: 7.4},
        "Islamabad": {2022: 4.2, 2023: 6.5, 2024: 5.9},
        "Peshawar":  {2022: 8.3, 2023: 10.1, 2024: 9.5},
        "Quetta":    {2022: 9.0, 2023: 11.2, 2024: 10.3},
    }
)

# List of all national indicators — Lab 4
all_indicators = [inflation, rupee_rate, unemployment, gdp_growth]

# Sorted list of years — Lab 4
YEARS = sorted(inflation.get_years())


# ─────────────────────────────────────────────
#  LAB 5 — NumPy: Statistical Analysis
# ─────────────────────────────────────────────

def numpy_analysis(indicator: EconomicIndicator) -> dict:
    """
    Run full NumPy statistical analysis on any indicator.
    Uses: np.array, np.mean, np.std, np.min, np.max,
          np.median, np.diff, np.abs, np.percentile
    """
    values = np.array(indicator.get_values(), dtype=float)  # NumPy array
    yearly_changes = np.diff(values)                         # year-on-year change

    return {
        "Mean":          round(float(np.mean(values)), 2),
        "Median":        round(float(np.median(values)), 2),
        "Std Dev":       round(float(np.std(values)), 2),
        "Min":           round(float(np.min(values)), 2),
        "Max":           round(float(np.max(values)), 2),
        "Avg Change/yr": round(float(np.mean(yearly_changes)), 2),
        "Worst Jump":    round(float(np.max(np.abs(yearly_changes))), 2),
        "75th Pctile":   round(float(np.percentile(values, 75)), 2),
    }


def compute_stress_index(inf_val: float, unemp_val: float,
                         rupee_val: float, gdp_val: float) -> float:
    """
    Custom Economic Stress Index (ESI) using NumPy-style weighted formula.
    Scale: 0 (best) to 100 (worst crisis).
    Weights: Inflation 40% | Unemployment 25% | PKR Rate 20% | GDP 15%
    """
    # Lab 5 — NumPy operations inside formula
    values   = np.array([inf_val, unemp_val, rupee_val, gdp_val])
    weights  = np.array([40.0, 25.0, 20.0, 15.0])

    inf_score   = min(values[0] / 30.0, 1.0) * weights[0]
    unemp_score = min(values[1] / 15.0, 1.0) * weights[1]
    rupee_score = min((values[2] - 100) / 200.0, 1.0) * weights[2]
    gdp_score   = max(0.0, (5.0 - values[3]) / 10.0) * weights[3]

    return round(float(inf_score + unemp_score + rupee_score + gdp_score), 1)


# ─────────────────────────────────────────────
#  LAB 6 — Pandas: DataFrames
# ─────────────────────────────────────────────

def build_national_dataframe() -> pd.DataFrame:
    """
    Build national indicators DataFrame.
    Lab 6: DataFrame creation, computed columns, set_index
    Lab 2: Control flow for ESI status classification
    """
    rows = []
    for yr in YEARS:   # Lab 2 — for loop
        esi = compute_stress_index(
            inflation.data.get(yr, 0),
            unemployment.data.get(yr, 0),
            rupee_rate.data.get(yr, 0),
            gdp_growth.data.get(yr, 0)
        )
        # Lab 2 — if/elif/else control flow
        if esi >= ESI_CRITICAL:
            status = "CRITICAL"
        elif esi >= ESI_HIGH:
            status = "HIGH STRESS"
        elif esi >= ESI_MODERATE:
            status = "MODERATE"
        else:
            status = "STABLE"

        rows.append({
            "Year":             yr,
            "Inflation (%)":    inflation.data.get(yr),
            "PKR/USD":          rupee_rate.data.get(yr),
            "Unemployment (%)": unemployment.data.get(yr),
            "GDP Growth (%)":   gdp_growth.data.get(yr),
            "Stress Index":     esi,
            "Status":           status,
        })

    return pd.DataFrame(rows).set_index("Year")


def build_city_dataframe() -> pd.DataFrame:
    """
    Build city-level unemployment DataFrame.
    Lab 6: DataFrame creation
    Lab 2: Control flow for severity classification
    """
    rows = []
    for city in CITIES:   # Lab 2 — for loop over list
        result = city_unemployment.get_city_latest(city)
        if result:         # Lab 2 — if condition
            yr, val = result
            # Lab 2 — if/elif/else
            if val >= 10:
                severity = "CRITICAL"
            elif val >= 8:
                severity = "HIGH"
            elif val >= 6:
                severity = "MODERATE"
            else:
                severity = "LOW"
            rows.append({
                "City":             city,
                "Unemployment (%)": val,
                "Severity":         severity
            })

    return pd.DataFrame(rows).set_index("City")


# ─────────────────────────────────────────────
#  LAB 6 — Pandas: Filtering, Sorting, Aggregation
# ─────────────────────────────────────────────

def pandas_analysis(df_national: pd.DataFrame, df_city: pd.DataFrame):
    """
    Demonstrates all three Pandas operations explicitly:
    1. Filtering  — select rows matching a condition
    2. Sorting    — sort_values() ascending and descending
    3. Aggregation — describe(), mean(), groupby-style summary
    """
    LINE = "─" * 65

    # ── FILTERING ──────────────────────────────────────────
    print(f"\n{LINE}")
    print("  PANDAS FILTERING — Crisis Years (ESI >= 40):")
    print(LINE)
    crisis = df_national[df_national["Stress Index"] >= ESI_HIGH]   # filtering
    print(crisis[["Inflation (%)", "PKR/USD", "Unemployment (%)",
                  "Stress Index", "Status"]].to_string())

    print(f"\n{LINE}")
    print("  PANDAS FILTERING — Cities with HIGH or CRITICAL unemployment:")
    print(LINE)
    high_cities = df_city[df_city["Severity"].isin(["HIGH", "CRITICAL"])]
    print(high_cities.to_string())

    # ── SORTING ────────────────────────────────────────────
    print(f"\n{LINE}")
    print("  PANDAS SORTING — Years ranked by Stress Index (worst first):")
    print(LINE)
    sorted_by_esi = df_national.sort_values("Stress Index", ascending=False)
    print(sorted_by_esi[["Inflation (%)", "Stress Index", "Status"]].to_string())

    print(f"\n{LINE}")
    print("  PANDAS SORTING — Cities ranked by Unemployment (highest first):")
    print(LINE)
    sorted_cities = df_city.sort_values("Unemployment (%)", ascending=False)
    print(sorted_cities.to_string())

    # ── AGGREGATION ────────────────────────────────────────
    print(f"\n{LINE}")
    print("  PANDAS AGGREGATION — Statistical Summary (describe):")
    print(LINE)
    numeric_cols = df_national[["Inflation (%)", "PKR/USD",
                                "Unemployment (%)", "GDP Growth (%)", "Stress Index"]]
    print(numeric_cols.describe().round(2).to_string())

    print(f"\n{LINE}")
    print("  PANDAS AGGREGATION — Average values by Status group:")
    print(LINE)
    group_summary = df_national.groupby("Status")[
        ["Inflation (%)", "Unemployment (%)", "Stress Index"]
    ].mean().round(2)
    print(group_summary.to_string())


# ─────────────────────────────────────────────
#  TERMINAL SUMMARY
# ─────────────────────────────────────────────

def print_summary(df_national: pd.DataFrame, df_city: pd.DataFrame):
    """Print full terminal summary covering all labs."""
    LINE = "=" * 65

    print(f"\n{LINE}")
    print(f"       {PROJECT_TITLE}")
    print(f"       Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}")
    print(LINE)

    # Full national data table
    print("\n  SECTION 1 — NATIONAL DATA TABLE (2019–2024):\n")
    print(df_national.to_string())

    # City data
    print(f"\n{'─'*65}")
    print("  SECTION 2 — CITY UNEMPLOYMENT 2024:\n")
    print(df_city.to_string())

    # NumPy stats for ALL indicators
    print(f"\n{'─'*65}")
    print("  SECTION 3 — NUMPY STATISTICAL ANALYSIS (All Indicators):\n")
    for ind in all_indicators:   # Lab 2 — for loop over list
        stats = numpy_analysis(ind)
        print(f"  {ind.name} ({ind.unit.strip()}):")
        for stat_name, stat_val in stats.items():   # Lab 4 — dict iteration
            print(f"    {stat_name:<16}: {stat_val}")
        print()

    # Pandas filtering, sorting, aggregation
    print(f"{'─'*65}")
    print("  SECTION 4 — PANDAS OPERATIONS (Filtering / Sorting / Aggregation):")
    pandas_analysis(df_national, df_city)

    print(f"\n{LINE}")
    print(f"  Data Sources: {DATA_SOURCES['national']}")
    print(f"  ESI Formula : Inflation 40% + Unemployment 25% + PKR 20% + GDP 15%")
    print(f"{LINE}\n")


# ─────────────────────────────────────────────
#  MATPLOTLIB VISUAL DASHBOARD
# ─────────────────────────────────────────────

def get_esi_color(esi: float) -> str:
    """Lab 2 — control flow: assign bar color based on ESI severity."""
    if esi >= ESI_CRITICAL:   return '#A32D2D'
    elif esi >= ESI_HIGH:     return '#EF9F27'
    elif esi >= ESI_MODERATE: return '#1D9E75'
    else:                     return '#185FA5'


def plot_dashboard(df_national: pd.DataFrame, df_city: pd.DataFrame):
    """Generate the full 6-panel visual dashboard using Matplotlib."""
    fig = plt.figure(figsize=(16, 18))
    fig.patch.set_facecolor('#FAFAFA')

    fig.text(0.5, 0.978, PROJECT_TITLE,
             ha='center', va='top', fontsize=20, fontweight='bold', color='#0E7C7B')
    fig.text(0.5, 0.963,
             f'National Economic Indicators {START_YEAR}–{END_YEAR}  |  '
             f'Generated: {datetime.now().strftime("%d %B %Y")}',
             ha='center', va='top', fontsize=11, color='#888780')

    years_str = [str(y) for y in YEARS]
    bar_w = 0.55

    # ── Panel 1: Inflation Bar Chart ──────────────────────
    ax1 = fig.add_subplot(4, 2, 1)
    infl_vals = inflation.get_values()
    infl_colors = ['#F09595' if v < 15 else '#A32D2D' for v in infl_vals]
    bs1 = ax1.bar(years_str, infl_vals, color=infl_colors, width=bar_w, zorder=3)
    ax1.set_title('Inflation Rate (%)', fontweight='bold', fontsize=12, color='#1A1A2E', pad=8)
    ax1.set_facecolor('#F8F8F8')
    ax1.grid(axis='y', color='#DDDDDD', linewidth=0.7, zorder=0)
    ax1.tick_params(colors='#888780', labelsize=10)
    for b, v in zip(bs1, infl_vals):
        ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4,
                 f'{v}%', ha='center', va='bottom', fontsize=9,
                 color='#444441', fontweight='bold')
    for s in ax1.spines.values(): s.set_visible(False)

    # ── Panel 2: PKR/USD Line Chart ───────────────────────
    ax2 = fig.add_subplot(4, 2, 2)
    pkr_vals = rupee_rate.get_values()
    ax2.plot(years_str, pkr_vals, color='#185FA5', linewidth=2.5,
             marker='o', markersize=7, markerfacecolor='#185FA5', zorder=3)
    ax2.fill_between(years_str, pkr_vals, alpha=0.12, color='#185FA5')
    ax2.set_title('PKR / USD Exchange Rate', fontweight='bold', fontsize=12,
                  color='#1A1A2E', pad=8)
    ax2.set_facecolor('#F8F8F8')
    ax2.grid(axis='y', color='#DDDDDD', linewidth=0.7, zorder=0)
    ax2.tick_params(colors='#888780', labelsize=10)
    for i, (yr, val) in enumerate(zip(years_str, pkr_vals)):
        ax2.text(i, val + 4, f'Rs.{int(val)}', ha='center', va='bottom',
                 fontsize=9, color='#0C447C', fontweight='bold')
    for s in ax2.spines.values(): s.set_visible(False)

    # ── Panel 3: Unemployment Bar Chart ───────────────────
    ax3 = fig.add_subplot(4, 2, 3)
    unemp_vals = unemployment.get_values()
    unemp_colors = ['#FAC775' if v < 6 else '#EF9F27' if v < 8 else '#BA7517'
                    for v in unemp_vals]
    bs3 = ax3.bar(years_str, unemp_vals, color=unemp_colors, width=bar_w, zorder=3)
    ax3.set_title('Unemployment Rate (%)', fontweight='bold', fontsize=12,
                  color='#1A1A2E', pad=8)
    ax3.set_facecolor('#F8F8F8')
    ax3.grid(axis='y', color='#DDDDDD', linewidth=0.7, zorder=0)
    ax3.tick_params(colors='#888780', labelsize=10)
    for b, v in zip(bs3, unemp_vals):
        ax3.text(b.get_x() + b.get_width()/2, b.get_height() + 0.08,
                 f'{v}%', ha='center', va='bottom', fontsize=9,
                 color='#444441', fontweight='bold')
    for s in ax3.spines.values(): s.set_visible(False)

    # ── Panel 4: GDP Growth Bar Chart ─────────────────────
    ax4 = fig.add_subplot(4, 2, 4)
    gdp_vals = gdp_growth.get_values()
    gdp_colors = ['#F09595' if v < 0 else '#1D9E75' for v in gdp_vals]
    bs4 = ax4.bar(years_str, gdp_vals, color=gdp_colors, width=bar_w, zorder=3)
    ax4.axhline(0, color='#AAAAAA', linewidth=0.8)
    ax4.set_title('GDP Growth Rate (%)', fontweight='bold', fontsize=12,
                  color='#1A1A2E', pad=8)
    ax4.set_facecolor('#F8F8F8')
    ax4.grid(axis='y', color='#DDDDDD', linewidth=0.7, zorder=0)
    ax4.tick_params(colors='#888780', labelsize=10)
    for b, v in zip(bs4, gdp_vals):
        off = 0.15 if v >= 0 else -0.35
        ax4.text(b.get_x() + b.get_width()/2, v + off,
                 f'{v}%', ha='center', va='bottom', fontsize=9,
                 color='#444441', fontweight='bold')
    ax4.legend(handles=[
        mpatches.Patch(color='#1D9E75', label='Positive growth'),
        mpatches.Patch(color='#F09595', label='Negative growth')
    ], fontsize=8, framealpha=0.5)
    for s in ax4.spines.values(): s.set_visible(False)

    # ── Panel 5–6: Economic Stress Index (wide) ───────────
    ax5 = fig.add_subplot(4, 2, (5, 6))
    esi_vals    = list(df_national['Stress Index'])
    esi_colors  = [get_esi_color(v) for v in esi_vals]
    status_list = list(df_national['Status'])
    hb = ax5.barh(years_str, esi_vals, color=esi_colors, height=0.55, zorder=3)
    ax5.set_xlim(0, 100)
    ax5.set_title(
        'Economic Stress Index (ESI) — 0 to 100  |  Higher = more stress',
        fontweight='bold', fontsize=12, color='#1A1A2E', pad=8)
    ax5.set_facecolor('#F8F8F8')
    ax5.grid(axis='x', color='#DDDDDD', linewidth=0.7, zorder=0)
    ax5.tick_params(colors='#888780', labelsize=10)
    for b, v, st in zip(hb, esi_vals, status_list):
        ax5.text(v + 1.5, b.get_y() + b.get_height()/2,
                 f'{v}  [{st}]', va='center', fontsize=10,
                 color='#1A1A2E', fontweight='bold')
    ax5.legend(handles=[
        mpatches.Patch(color='#185FA5', label='Stable (< 25)'),
        mpatches.Patch(color='#1D9E75', label='Moderate (25–40)'),
        mpatches.Patch(color='#EF9F27', label='High Stress (40–60)'),
        mpatches.Patch(color='#A32D2D', label='Critical (60+)'),
    ], loc='lower right', fontsize=9, framealpha=0.6)
    for s in ax5.spines.values(): s.set_visible(False)

    # ── Panel 7–8: City Unemployment (wide) ───────────────
    ax6 = fig.add_subplot(4, 2, (7, 8))
    city_names    = list(df_city.index)
    city_vals     = list(df_city['Unemployment (%)'])
    severity_list = list(df_city['Severity'])

    def city_color(v: float) -> str:
        if v >= 10: return '#A32D2D'
        elif v >= 8: return '#EF9F27'
        elif v >= 6: return '#FAC775'
        else: return '#1D9E75'

    city_colors = [city_color(v) for v in city_vals]
    hc = ax6.barh(city_names, city_vals, color=city_colors, height=0.5, zorder=3)
    ax6.set_xlim(0, 14)
    ax6.set_title('City-Level Unemployment Rate (%) — 2024',
                  fontweight='bold', fontsize=12, color='#1A1A2E', pad=8)
    ax6.set_facecolor('#F8F8F8')
    ax6.grid(axis='x', color='#DDDDDD', linewidth=0.7, zorder=0)
    ax6.tick_params(colors='#888780', labelsize=10)
    for b, v, sv in zip(hc, city_vals, severity_list):
        ax6.text(v + 0.2, b.get_y() + b.get_height()/2,
                 f'{v}%  [{sv}]', va='center', fontsize=10,
                 color='#1A1A2E', fontweight='bold')
    for s in ax6.spines.values(): s.set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.958])
    plt.savefig('pakistan_dashboard.png', dpi=150,
                bbox_inches='tight', facecolor='#FAFAFA')
    print("  Visual dashboard saved as: pakistan_dashboard.png")
    st.image("pakistan_dashboard.png")


# ─────────────────────────────────────────────
#  MAIN — Entry Point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Build Pandas DataFrames (Lab 6)
    df_national = build_national_dataframe()
    df_city     = build_city_dataframe()

    # Print full terminal summary (all labs)
    print_summary(df_national, df_city)

    # Generate visual charts (Matplotlib)
    plot_dashboard(df_national, df_city)
