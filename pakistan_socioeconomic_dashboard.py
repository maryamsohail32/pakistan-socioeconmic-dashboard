# ============================================================
#   PAKISTAN SOCIOECONOMIC DASHBOARD
#   Lab 7 — Open Ended Project (Streamlit Interactive Version)
#
#   Converted from the original Matplotlib static-image script
#   into a real interactive Streamlit app. All Lab 1–6 logic
#   below (constants, OOP, dicts/lists, NumPy, Pandas) is
#   unchanged from the original — only the presentation layer
#   changed from plt.savefig() to live st.* components, with
#   an added Lab 8-style UI section for interactivity.
# ============================================================

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import streamlit as st

# ─────────────────────────────────────────────
# STREAMLIT PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Pakistan Socioeconomic Dashboard",
    page_icon="🇵🇰",
    layout="wide",
)

# ─────────────────────────────────────────────
# LAB 1 — Variables & Data Types
# Named constants used throughout the project
# ─────────────────────────────────────────────
PROJECT_TITLE = "Pakistan Socioeconomic Dashboard"   # str
START_YEAR = 2019                                    # int
END_YEAR = 2024                                      # int
ESI_CRITICAL = 60.0                                  # float — stress threshold
ESI_HIGH = 40.0                                       # float
ESI_MODERATE = 25.0                                   # float
CITIES = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta"]  # list
DATA_SOURCES = {"national": "SBP / PBS / World Bank", "city": "PBS 2024"}  # dict


# ─────────────────────────────────────────────
# LAB 3 — OOP: Base Class
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
            data : {year (int): value (float)} dictionary ← Lab 4
        """
        self.name = name   # str attribute
        self.unit = unit   # str attribute
        self.data = data   # dict attribute — Lab 4

    # Instance method — returns sorted list of years
    def get_years(self) -> list:
        return sorted(self.data.keys())  # list — Lab 4

    # Instance method — returns values in year order.
    # `years` param added for Streamlit UI filtering (Lab 8);
    # defaults to all years, preserving original behavior.
    def get_values(self, years=None) -> list:
        years = years if years is not None else self.get_years()
        return [self.data[yr] for yr in years if yr in self.data]

    # Instance method — returns most recent (year, value) tuple
    def latest(self, years=None) -> tuple:
        pool = years if years else self.data.keys()  # Lab 2 — uses built-in max
        latest_year = max(pool)
        return latest_year, self.data[latest_year]

    # Dunder method for readable object representation
    def __repr__(self) -> str:
        yr, val = self.latest()
        return f"<EconomicIndicator | {self.name}: {val}{self.unit} ({yr})>"


# ─────────────────────────────────────────────
# LAB 3 — OOP: Subclass (Inheritance)
# ─────────────────────────────────────────────
class CityIndicator(EconomicIndicator):
    """
    Subclass of EconomicIndicator that also stores city-level data.
    Demonstrates: inheritance, super(), method extension
    """

    def __init__(self, name: str, unit: str, data: dict, city_data: dict):
        super().__init__(name, unit, data)      # call parent __init__
        self.city_data = city_data              # extra attribute: {city: {year: value}}

    # Extended method — get latest value for a specific city
    def get_city_latest(self, city: str) -> tuple:
        if city not in self.city_data:
            return None
        city_years = self.city_data[city]
        latest_year = max(city_years.keys())
        return latest_year, city_years[latest_year]

    def get_city_values_for_year(self, year: int) -> dict:
        result = {}
        for city, years_dict in self.city_data.items():
            if year in years_dict:
                result[city] = years_dict[year]
        return result


# ─────────────────────────────────────────────
# LAB 4 — Data Structures: Dictionaries & Lists
# ─────────────────────────────────────────────
# Dictionary: {year: value} for each national indicator
inflation = EconomicIndicator(
    name="Inflation Rate", unit="%",
    data={2019: 6.8, 2020: 10.7, 2021: 8.9, 2022: 12.2, 2023: 29.2, 2024: 23.4}
)
rupee_rate = EconomicIndicator(
    name="PKR/USD Exchange Rate", unit=" PKR",
    data={2019: 150.0, 2020: 168.0, 2021: 176.0, 2022: 204.0, 2023: 285.0, 2024: 278.0}
)
unemployment = EconomicIndicator(
    name="Unemployment Rate", unit="%",
    data={2019: 4.1, 2020: 4.5, 2021: 6.0, 2022: 6.2, 2023: 8.5, 2024: 7.9}
)
gdp_growth = EconomicIndicator(
    name="GDP Growth Rate", unit="%",
    data={2019: 1.9, 2020: -0.5, 2021: 5.7, 2022: 6.1, 2023: -0.2, 2024: 2.4}
)
# Subclass instance: city-level unemployment data
city_unemployment = CityIndicator(
    name="City Unemployment Rate", unit="%",
    data={2019: 4.1, 2020: 4.5, 2021: 6.0, 2022: 6.2, 2023: 8.5, 2024: 7.9},
    city_data={
        "Karachi": {2022: 7.1, 2023: 9.2, 2024: 8.6},
        "Lahore": {2022: 5.8, 2023: 8.0, 2024: 7.4},
        "Islamabad": {2022: 4.2, 2023: 6.5, 2024: 5.9},
        "Peshawar": {2022: 8.3, 2023: 10.1, 2024: 9.5},
        "Quetta": {2022: 9.0, 2023: 11.2, 2024: 10.3},
    }
)

# List of all national indicators — Lab 4
all_indicators = [inflation, rupee_rate, unemployment, gdp_growth]

# Sorted list of years — Lab 4
ALL_YEARS = sorted(inflation.get_years())

# Lab 8 (Streamlit UI) — available years for the city-year dropdown
CITY_YEARS = sorted({yr for c in city_unemployment.city_data.values() for yr in c})


# ─────────────────────────────────────────────
# LAB 5 — NumPy: Statistical Analysis
# ─────────────────────────────────────────────
def numpy_analysis(indicator: EconomicIndicator, years: list) -> dict:
    """
    Run full NumPy statistical analysis on any indicator, restricted to
    the given `years` (Lab 8 — driven by the Streamlit year-range slider).
    Uses: np.array, np.mean, np.std, np.min, np.max,
          np.median, np.diff, np.abs, np.percentile
    """
    values = np.array(indicator.get_values(years), dtype=float)  # NumPy array
    if len(values) == 0:
        return {}
    yearly_changes = np.diff(values) if len(values) > 1 else np.array([0.0])  # year-on-year change
    return {
        "Mean": round(float(np.mean(values)), 2),
        "Median": round(float(np.median(values)), 2),
        "Std Dev": round(float(np.std(values)), 2),
        "Min": round(float(np.min(values)), 2),
        "Max": round(float(np.max(values)), 2),
        "Avg Change/yr": round(float(np.mean(yearly_changes)), 2),
        "Worst Jump": round(float(np.max(np.abs(yearly_changes))), 2),
        "75th Pctile": round(float(np.percentile(values, 75)), 2),
    }


def compute_stress_index(inf_val: float, unemp_val: float,
                          rupee_val: float, gdp_val: float) -> float:
    """
    Custom Economic Stress Index (ESI) using NumPy-style weighted formula.
    Scale: 0 (best) to 100 (worst crisis).
    Weights: Inflation 40% | Unemployment 25% | PKR Rate 20% | GDP 15%
    """
    # Lab 5 — NumPy operations inside formula
    values = np.array([inf_val, unemp_val, rupee_val, gdp_val])
    weights = np.array([40.0, 25.0, 20.0, 15.0])
    inf_score = min(values[0] / 30.0, 1.0) * weights[0]
    unemp_score = min(values[1] / 15.0, 1.0) * weights[1]
    rupee_score = min((values[2] - 100) / 200.0, 1.0) * weights[2]
    gdp_score = max(0.0, (5.0 - values[3]) / 10.0) * weights[3]
    return round(float(inf_score + unemp_score + rupee_score + gdp_score), 1)


# ─────────────────────────────────────────────
# LAB 6 — Pandas: DataFrames
# ─────────────────────────────────────────────
def build_national_dataframe(years: list) -> pd.DataFrame:
    """
    Build national indicators DataFrame, restricted to `years`
    (Lab 8 — driven by the Streamlit year-range slider).
    Lab 6: DataFrame creation, computed columns, set_index
    Lab 2: Control flow for ESI status classification
    """
    rows = []
    for yr in years:  # Lab 2 — for loop
        esi = compute_stress_index(
            inflation.data.get(yr, 0),
            unemployment.data.get(yr, 0),
            rupee_rate.data.get(yr, 0),
            gdp_growth.data.get(yr, 0),
        )
        if esi >= ESI_CRITICAL:
            status = "CRITICAL"
        elif esi >= ESI_HIGH:
            status = "HIGH STRESS"
        elif esi >= ESI_MODERATE:
            status = "MODERATE"
        else:
            status = "STABLE"

        rows.append({
            "Year": yr,
            "Inflation (%)": inflation.data.get(yr),
            "PKR/USD": rupee_rate.data.get(yr),
            "Unemployment (%)": unemployment.data.get(yr),
            "GDP Growth (%)": gdp_growth.data.get(yr),
            "Stress Index": esi,
            "Status": status,
        })
    return pd.DataFrame(rows).set_index("Year")


def build_city_dataframe(cities: list, year: int) -> pd.DataFrame:
    """
    Build city-level unemployment DataFrame for the selected `cities`
    and `year` (Lab 8 — driven by the Streamlit sidebar controls).
    Lab 6: DataFrame creation
    Lab 2: Control flow for severity classification
    """
    rows = []
    for city in cities:  # Lab 2 — for loop over list
        years_dict = city_unemployment.city_data.get(city, {})
        if year in years_dict:
            val = years_dict[year]
        elif years_dict:
            # fall back to latest available year at/under the selected year, else latest overall
            eligible = [y for y in years_dict if y <= year]
            fallback_year = max(eligible) if eligible else max(years_dict.keys())
            val = years_dict[fallback_year]
        else:
            continue

        if val >= 10:
            severity = "CRITICAL"
        elif val >= 8:
            severity = "HIGH"
        elif val >= 6:
            severity = "MODERATE"
        else:
            severity = "LOW"

        rows.append({"City": city, "Unemployment (%)": val, "Severity": severity})
    return pd.DataFrame(rows).set_index("City") if rows else pd.DataFrame(
        columns=["Unemployment (%)", "Severity"]
    )


def get_esi_color(esi: float) -> str:
    """Lab 2 — control flow: assign bar color based on ESI severity."""
    if esi >= ESI_CRITICAL: return '#A32D2D'
    elif esi >= ESI_HIGH: return '#EF9F27'
    elif esi >= ESI_MODERATE: return '#1D9E75'
    else: return '#185FA5'


def city_color(v: float) -> str:
    """Lab 2 — control flow: assign bar color based on unemployment severity."""
    if v >= 10: return '#A32D2D'
    elif v >= 8: return '#EF9F27'
    elif v >= 6: return '#FAC775'
    else: return '#1D9E75'


# ─────────────────────────────────────────────
# LAB 8 — Streamlit UI: Interactive Controls
# (This section replaces the original's static
#  plot_dashboard()/plt.savefig() call — everything
#  above this line is unchanged Lab 1–6 logic.)
# ─────────────────────────────────────────────
st.sidebar.title("🇵🇰 Dashboard Filters")

year_range = st.sidebar.slider(
    "Year range",
    min_value=START_YEAR,
    max_value=END_YEAR,
    value=(START_YEAR, END_YEAR),
    step=1,
)
selected_years = [y for y in ALL_YEARS if year_range[0] <= y <= year_range[1]]

city_year = st.sidebar.selectbox(
    "City data — year",
    options=CITY_YEARS,
    index=len(CITY_YEARS) - 1,
)

selected_cities = st.sidebar.multiselect(
    "Cities to display",
    options=CITIES,
    default=CITIES,
)

st.sidebar.markdown("---")
st.sidebar.caption(
    f"Data Sources: {DATA_SOURCES['national']}. Some figures are estimates/"
    "approximations based on publicly available data at time of compilation."
)

if not selected_years:
    st.warning("Select at least one year in the sidebar to see data.")
    st.stop()

df_national = build_national_dataframe(selected_years)
df_city = build_city_dataframe(selected_cities if selected_cities else CITIES, city_year)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title(PROJECT_TITLE)
st.caption(
    f"National Economic Indicators {year_range[0]}–{year_range[1]} | "
    f"City data: {city_year} | Generated: {datetime.now().strftime('%d %B %Y')}"
)

# ─────────────────────────────────────────────
# KPI ROW — latest selected year
# ─────────────────────────────────────────────
latest_yr = max(selected_years)
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Inflation", f"{inflation.data.get(latest_yr, 0)}%")
k2.metric("PKR/USD", f"Rs.{int(rupee_rate.data.get(latest_yr, 0))}")
k3.metric("Unemployment", f"{unemployment.data.get(latest_yr, 0)}%")
k4.metric("GDP Growth", f"{gdp_growth.data.get(latest_yr, 0)}%")
latest_esi = df_national.loc[latest_yr, "Stress Index"] if latest_yr in df_national.index else None
k5.metric("Stress Index", f"{latest_esi}" if latest_esi is not None else "—",
          df_national.loc[latest_yr, "Status"] if latest_yr in df_national.index else "")

st.markdown("---")

years_str = [str(y) for y in selected_years]
bar_w = 0.55

# ─────────────────────────────────────────────
# ROW 1: Inflation + PKR/USD
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    infl_vals = inflation.get_values(selected_years)
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    infl_colors = ['#F09595' if v < 15 else '#A32D2D' for v in infl_vals]
    bs1 = ax1.bar(years_str, infl_vals, color=infl_colors, width=bar_w, zorder=3)
    ax1.set_title('Inflation Rate (%)', fontweight='bold', fontsize=12, color='#1A1A2E')
    ax1.set_facecolor('#F8F8F8')
    ax1.grid(axis='y', color='#DDDDDD', linewidth=0.7, zorder=0)
    for b, v in zip(bs1, infl_vals):
        ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4, f'{v}%',
                  ha='center', va='bottom', fontsize=9, color='#444441', fontweight='bold')
    for s in ax1.spines.values(): s.set_visible(False)
    st.pyplot(fig1, use_container_width=True)

with col2:
    pkr_vals = rupee_rate.get_values(selected_years)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(years_str, pkr_vals, color='#185FA5', linewidth=2.5, marker='o',
             markersize=7, markerfacecolor='#185FA5', zorder=3)
    ax2.fill_between(years_str, pkr_vals, alpha=0.12, color='#185FA5')
    ax2.set_title('PKR / USD Exchange Rate', fontweight='bold', fontsize=12, color='#1A1A2E')
    ax2.set_facecolor('#F8F8F8')
    ax2.grid(axis='y', color='#DDDDDD', linewidth=0.7, zorder=0)
    for i, (yr, val) in enumerate(zip(years_str, pkr_vals)):
        ax2.text(i, val + 4, f'Rs.{int(val)}', ha='center', va='bottom',
                  fontsize=9, color='#0C447C', fontweight='bold')
    for s in ax2.spines.values(): s.set_visible(False)
    st.pyplot(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# ROW 2: Unemployment + GDP
# ─────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    unemp_vals = unemployment.get_values(selected_years)
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    unemp_colors = ['#FAC775' if v < 6 else '#EF9F27' if v < 8 else '#BA7517' for v in unemp_vals]
    bs3 = ax3.bar(years_str, unemp_vals, color=unemp_colors, width=bar_w, zorder=3)
    ax3.set_title('Unemployment Rate (%)', fontweight='bold', fontsize=12, color='#1A1A2E')
    ax3.set_facecolor('#F8F8F8')
    ax3.grid(axis='y', color='#DDDDDD', linewidth=0.7, zorder=0)
    for b, v in zip(bs3, unemp_vals):
        ax3.text(b.get_x() + b.get_width()/2, b.get_height() + 0.08, f'{v}%',
                  ha='center', va='bottom', fontsize=9, color='#444441', fontweight='bold')
    for s in ax3.spines.values(): s.set_visible(False)
    st.pyplot(fig3, use_container_width=True)

with col4:
    gdp_vals = gdp_growth.get_values(selected_years)
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    gdp_colors = ['#F09595' if v < 0 else '#1D9E75' for v in gdp_vals]
    bs4 = ax4.bar(years_str, gdp_vals, color=gdp_colors, width=bar_w, zorder=3)
    ax4.axhline(0, color='#AAAAAA', linewidth=0.8)
    ax4.set_title('GDP Growth Rate (%)', fontweight='bold', fontsize=12, color='#1A1A2E')
    ax4.set_facecolor('#F8F8F8')
    ax4.grid(axis='y', color='#DDDDDD', linewidth=0.7, zorder=0)
    for b, v in zip(bs4, gdp_vals):
        off = 0.15 if v >= 0 else -0.35
        ax4.text(b.get_x() + b.get_width()/2, v + off, f'{v}%',
                  ha='center', va='bottom', fontsize=9, color='#444441', fontweight='bold')
    ax4.legend(handles=[
        mpatches.Patch(color='#1D9E75', label='Positive growth'),
        mpatches.Patch(color='#F09595', label='Negative growth')
    ], fontsize=8, framealpha=0.5)
    for s in ax4.spines.values(): s.set_visible(False)
    st.pyplot(fig4, use_container_width=True)

# ─────────────────────────────────────────────
# ROW 3: Economic Stress Index (wide)
# ─────────────────────────────────────────────
st.subheader("Economic Stress Index (ESI) — 0 to 100 | Higher = more stress")
esi_vals = list(df_national['Stress Index'])
esi_colors = [get_esi_color(v) for v in esi_vals]
status_list = list(df_national['Status'])
fig5, ax5 = plt.subplots(figsize=(12, 3.5))
hb = ax5.barh(years_str, esi_vals, color=esi_colors, height=0.55, zorder=3)
ax5.set_xlim(0, 100)
ax5.set_facecolor('#F8F8F8')
ax5.grid(axis='x', color='#DDDDDD', linewidth=0.7, zorder=0)
for b, v, st_label in zip(hb, esi_vals, status_list):
    ax5.text(v + 1.5, b.get_y() + b.get_height()/2, f'{v} [{st_label}]',
              va='center', fontsize=10, color='#1A1A2E', fontweight='bold')
ax5.legend(handles=[
    mpatches.Patch(color='#185FA5', label='Stable (< 25)'),
    mpatches.Patch(color='#1D9E75', label='Moderate (25–40)'),
    mpatches.Patch(color='#EF9F27', label='High Stress (40–60)'),
    mpatches.Patch(color='#A32D2D', label='Critical (60+)'),
], loc='lower right', fontsize=9, framealpha=0.6)
for s in ax5.spines.values(): s.set_visible(False)
st.pyplot(fig5, use_container_width=True)

# ─────────────────────────────────────────────
# ROW 4: City Unemployment (wide, interactive)
# ─────────────────────────────────────────────
st.subheader(f"City-Level Unemployment Rate (%) — {city_year}")
if df_city.empty:
    st.info("No city data available for the current filter selection.")
else:
    city_names = list(df_city.index)
    city_vals = list(df_city['Unemployment (%)'])
    severity_list = list(df_city['Severity'])
    city_colors = [city_color(v) for v in city_vals]
    fig6, ax6 = plt.subplots(figsize=(12, 3.5))
    hc = ax6.barh(city_names, city_vals, color=city_colors, height=0.5, zorder=3)
    ax6.set_xlim(0, 14)
    ax6.set_facecolor('#F8F8F8')
    ax6.grid(axis='x', color='#DDDDDD', linewidth=0.7, zorder=0)
    for b, v, sv in zip(hc, city_vals, severity_list):
        ax6.text(v + 0.2, b.get_y() + b.get_height()/2, f'{v}% [{sv}]',
                  va='center', fontsize=10, color='#1A1A2E', fontweight='bold')
    for s in ax6.spines.values(): s.set_visible(False)
    st.pyplot(fig6, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# DATA TABLES + NUMPY STATS (expandable, still interactive)
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 National Data Table", "🏙️ City Data Table", "📈 NumPy Statistics"])

with tab1:
    st.dataframe(df_national, use_container_width=True)
    crisis = df_national[df_national["Stress Index"] >= ESI_HIGH]
    if not crisis.empty:
        st.caption("Years with High Stress or Critical status (ESI ≥ 40):")
        st.dataframe(crisis[["Inflation (%)", "PKR/USD", "Unemployment (%)", "Stress Index", "Status"]],
                     use_container_width=True)

with tab2:
    st.dataframe(df_city, use_container_width=True)

with tab3:
    for ind in all_indicators:
        stats = numpy_analysis(ind, selected_years)
        if stats:
            st.markdown(f"**{ind.name} ({ind.unit.strip()})**")
            st.dataframe(pd.DataFrame([stats]), use_container_width=True, hide_index=True)

st.caption(
    "Data compiled from publicly reported SBP, PBS, and World Bank/IMF figures. "
    "Some figures may be estimates or approximations."
)
