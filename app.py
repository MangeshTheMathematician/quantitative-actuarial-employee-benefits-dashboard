# =============================================================================
# HESSIAN-AI
# QUANTITATIVE ACTUARIAL EMPLOYEE BENEFITS DASHBOARD
# STREAMLIT APPLICATION
# =============================================================================
#
# PURPOSE
# -------
#
# This Streamlit application consumes ONLY the validated dashboard-ready
# datasets produced by Pipeline 11.
#
# The dashboard does NOT recalculate actuarial liabilities or assumptions.
#
# Data architecture:
#
# Pipelines 01-10
#       ->
# Pipeline 11 Dashboard Data Mart
#       ->
# Data/dashboard_ready/
#       ->
# Streamlit Dashboard
#
# =============================================================================


# Import Path so file locations remain portable across Windows,
# GitHub and Streamlit deployment.
from pathlib import Path


# Import NumPy for numerical and missing-value handling.
import numpy as np


# Import pandas for reading and filtering dashboard datasets.
import pandas as pd


# Import Streamlit for the interactive web dashboard.
import streamlit as st


# Import Plotly Express for professional interactive charts.
import plotly.express as px


# Import Plotly Graph Objects for charts requiring multiple series.
import plotly.graph_objects as go


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================


# Configure the Streamlit browser page.
st.set_page_config(
    page_title="Hessian-AI Employee Benefits Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# PROJECT PATHS
# =============================================================================


# Identify the project root from the location of app.py.
PROJECT_ROOT = Path(__file__).resolve().parent


# Define the dashboard-ready data directory created by Pipeline 11.
DATA_DIR = (
    PROJECT_ROOT
    / "Data"
    / "dashboard_ready"
)


# =============================================================================
# DASHBOARD FILE MAP
# =============================================================================


# Map logical dashboard datasets to physical CSV files.
FILES = {

    "kpis":
        "dashboard_kpi_cards.csv",

    "products":
        "dashboard_product_overview.csv",

    "plans":
        "dashboard_plan_overview.csv",

    "employees":
        "dashboard_employee_detail.csv",

    "segments":
        "dashboard_segment_risk.csv",

    "governance":
        "dashboard_governance.csv",

    "validation":
        "dashboard_validation.csv",

    "filters":
        "dashboard_filters.csv",

    "visual_catalog":
        "dashboard_visual_catalog.csv",

    "manifest":
        "dashboard_manifest.csv",
}


# =============================================================================
# DATA LOADER
# =============================================================================


# Cache CSV files so Streamlit does not reload them on every interaction.
@st.cache_data(show_spinner=False)
def load_dashboard_file(
    file_name,
):


    # Construct full file path.
    path = (
        DATA_DIR
        / file_name
    )


    # Stop gracefully when a required dashboard file is absent.
    if not path.exists():

        return pd.DataFrame()


    # Load CSV.
    return pd.read_csv(
        path
    )


# =============================================================================
# LOAD PIPELINE 11 DATA MART
# =============================================================================


# Load executive KPI cards.
kpis = load_dashboard_file(
    FILES["kpis"]
)


# Load product-level portfolio summary.
products = load_dashboard_file(
    FILES["products"]
)


# Load plan-level portfolio summary.
plans = load_dashboard_file(
    FILES["plans"]
)


# Load employee drill-down table.
employees = load_dashboard_file(
    FILES["employees"]
)


# Load workforce concentration table.
segments = load_dashboard_file(
    FILES["segments"]
)


# Load governance register.
governance = load_dashboard_file(
    FILES["governance"]
)


# Load validation register.
validation = load_dashboard_file(
    FILES["validation"]
)


# Load dashboard filter catalogue.
filters = load_dashboard_file(
    FILES["filters"]
)


# Load visualization catalogue.
visual_catalog = load_dashboard_file(
    FILES["visual_catalog"]
)


# Load dashboard dataset manifest.
manifest = load_dashboard_file(
    FILES["manifest"]
)


# =============================================================================
# CRITICAL DATA CHECK
# =============================================================================


# Stop the application if Pipeline 11 outputs are unavailable.
if kpis.empty:

    st.error(
        "Pipeline 11 dashboard-ready data could not be found."
    )

    st.code(
        str(DATA_DIR)
    )

    st.stop()


# =============================================================================
# FORMAT HELPERS
# =============================================================================


# Safely convert one value to a number.
def to_number(
    value,
):


    # Convert invalid values to NaN.
    return pd.to_numeric(
        pd.Series([value]),
        errors="coerce",
    ).iloc[0]


# Format Indian Rupee values compactly.
def format_inr(
    value,
):


    # Convert input.
    value = to_number(
        value
    )


    # Missing value.
    if pd.isna(
        value
    ):

        return "N/A"


    # Billions.
    if abs(value) >= 1_000_000_000:

        return (
            f"₹{value / 1_000_000_000:,.2f}B"
        )


    # Millions.
    if abs(value) >= 1_000_000:

        return (
            f"₹{value / 1_000_000:,.2f}M"
        )


    # Thousands.
    if abs(value) >= 1_000:

        return (
            f"₹{value / 1_000:,.2f}K"
        )


    # Small values.
    return (
        f"₹{value:,.2f}"
    )


# Format an integer.
def format_integer(
    value,
):


    # Convert input.
    value = to_number(
        value
    )


    # Missing.
    if pd.isna(
        value
    ):

        return "N/A"


    # Return whole-number format.
    return f"{int(round(value)):,}"


# Format a ratio as percentage.
def format_percentage(
    value,
):


    # Convert input.
    value = to_number(
        value
    )


    # Missing.
    if pd.isna(
        value
    ):

        return "N/A"


    # Pipeline 11 KPI ratio values remain decimal ratios.
    return f"{value:.2%}"


# =============================================================================
# KPI LOOKUP
# =============================================================================


# Retrieve one KPI from dashboard_kpi_cards.csv.
def get_kpi(
    kpi_id,
):


    # Find requested KPI row.
    match = kpis.loc[

        kpis[
            "kpi_id"
        ].eq(
            kpi_id
        )

    ]


    # Return missing if no row exists.
    if match.empty:

        return np.nan


    # Return numeric value.
    return match[
        "numeric_value"
    ].iloc[0]


# Display a KPI using its correct format.
def show_metric(
    label,
    value,
    format_type="number",
):


    # Currency.
    if format_type == "currency":

        display_value = format_inr(
            value
        )


    # Percentage.
    elif format_type == "percentage":

        display_value = format_percentage(
            value
        )


    # Integer.
    elif format_type == "integer":

        display_value = format_integer(
            value
        )


    # Generic number.
    else:

        display_value = str(
            value
        )


    # Render Streamlit metric.
    st.metric(
        label=label,
        value=display_value,
    )


# =============================================================================
# SIDEBAR
# =============================================================================


# Dashboard identity.
st.sidebar.title(
    "Hessian-AI"
)


# Dashboard subtitle.
st.sidebar.caption(
    "Quantitative Actuarial Employee Benefits Dashboard"
)


# Navigation pages.
page = st.sidebar.radio(

    "Navigation",

    [

        "Executive Overview",

        "Funding & Liabilities",

        "DC Superannuation",

        "Group Risk — GTI & EDLI",

        "Workforce Concentration",

        "Employee Drill-Down",

        "Governance & Validation",
    ],
)


# Divider.
st.sidebar.divider()


# Display master valuation date.
st.sidebar.markdown(
    "**Valuation Date**"
)

st.sidebar.write(
    "1 September 2026"
)


# Display data layer.
st.sidebar.markdown(
    "**Data Layer**"
)

st.sidebar.write(
    "Pipeline 11 — P11-C01"
)


# Display modeling status.
st.sidebar.success(
    "Portfolio validation passed"
)


# =============================================================================
# MAIN HEADER
# =============================================================================


# Main application title.
st.title(
    "Quantitative Actuarial Employee Benefits Dashboard"
)


# Explain dashboard scope.
st.caption(
    "Gratuity • Superannuation • DB Pension • EDLI • "
    "Group Term Insurance • Funding • Risk • Governance"
)


# =============================================================================
# PAGE 1 - EXECUTIVE OVERVIEW
# =============================================================================


if page == "Executive Overview":


    # Page heading.
    st.header(
        "Executive Overview"
    )


    # -------------------------------------------------------------------------
    # WORKFORCE
    # -------------------------------------------------------------------------


    st.subheader(
        "Covered Workforce"
    )


    # Create six KPI columns.
    cols = st.columns(
        6
    )


    # Active employees.
    with cols[0]:

        show_metric(
            "Active Employees",
            get_kpi(
                "active_employees"
            ),
            "integer",
        )


    # Gratuity.
    with cols[1]:

        show_metric(
            "Gratuity",
            get_kpi(
                "gratuity_members"
            ),
            "integer",
        )


    # DB Pension.
    with cols[2]:

        show_metric(
            "DB Pension",
            get_kpi(
                "db_pension_members"
            ),
            "integer",
        )


    # DC.
    with cols[3]:

        show_metric(
            "DC Superannuation",
            get_kpi(
                "dc_members"
            ),
            "integer",
        )


    # EDLI.
    with cols[4]:

        show_metric(
            "EDLI",
            8501,
            "integer",
        )


    # GTI.
    with cols[5]:

        show_metric(
            "GTI",
            7913,
            "integer",
        )


    # -------------------------------------------------------------------------
    # DEFINED BENEFIT FUNDING
    # -------------------------------------------------------------------------


    st.subheader(
        "Defined Benefit Funding"
    )


    # Four DB financial metrics.
    cols = st.columns(
        4
    )


    with cols[0]:

        show_metric(
            "Combined DB Liability",
            get_kpi(
                "combined_db_liability"
            ),
            "currency",
        )


    with cols[1]:

        show_metric(
            "DB Plan Assets",
            get_kpi(
                "combined_db_assets"
            ),
            "currency",
        )


    with cols[2]:

        show_metric(
            "Funding Ratio",
            get_kpi(
                "combined_db_funding_ratio"
            ),
            "percentage",
        )


    with cols[3]:

        show_metric(
            "Funding Deficit",
            get_kpi(
                "combined_db_funding_deficit"
            ),
            "currency",
        )


    # -------------------------------------------------------------------------
    # GROUP RISK
    # -------------------------------------------------------------------------


    st.subheader(
        "Group Risk"
    )


    cols = st.columns(
        5
    )


    with cols[0]:

        show_metric(
            "GTI Sum Assured",
            get_kpi(
                "gti_total_sum_assured"
            ),
            "currency",
        )


    with cols[1]:

        show_metric(
            "Expected Claims",
            get_kpi(
                "gti_expected_claims"
            ),
            "currency",
        )


    with cols[2]:

        show_metric(
            "Fresh Gross Premium",
            get_kpi(
                "gti_fresh_gross_premium"
            ),
            "currency",
        )


    with cols[3]:

        show_metric(
            "FCL Referrals",
            get_kpi(
                "gti_fcl_referrals"
            ),
            "integer",
        )


    with cols[4]:

        show_metric(
            "FCL Referral Rate",
            get_kpi(
                "gti_fcl_referral_rate"
            ),
            "percentage",
        )


    # -------------------------------------------------------------------------
    # DEFINED BENEFIT PRODUCT CHART
    # -------------------------------------------------------------------------


    st.subheader(
        "Defined Benefit Liability by Product"
    )


    # Keep Gratuity and DB Pension.
    db_products = products.loc[

        products[
            "product_type"
        ].isin([

            "Gratuity",

            "DB_Pension",
        ])

    ].copy()


    # Draw chart when data exist.
    if not db_products.empty:


        fig = px.bar(

            db_products,

            x="product_type",

            y="actuarial_liability",

            labels={

                "product_type":
                    "Product",

                "actuarial_liability":
                    "Actuarial Liability (INR)",
            },

            title=(
                "Gratuity vs DB Pension Liability"
            ),
        )


        # Display interactive chart.
        st.plotly_chart(

            fig,

            use_container_width=True
        )


# =============================================================================
# PAGE 2 - FUNDING AND LIABILITIES
# =============================================================================


elif page == "Funding & Liabilities":


    # Page heading.
    st.header(
        "Defined Benefit Funding & Liabilities"
    )


    # Keep funded DB products only.
    funded = plans.loc[

        plans[
            "funded_db_product_flag"
        ].fillna(
            False
        )

    ].copy()


    # -------------------------------------------------------------------------
    # LIABILITY VS ASSETS
    # -------------------------------------------------------------------------


    if not funded.empty:


        # Create grouped bar chart.
        fig = go.Figure()


        # Liability bars.
        fig.add_bar(

            name="Actuarial Liability",

            x=funded[
                "plan_id"
            ],

            y=funded[
                "actuarial_liability"
            ],
        )


        # Asset bars.
        fig.add_bar(

            name="Plan Assets",

            x=funded[
                "plan_id"
            ],

            y=funded[
                "plan_assets"
            ],
        )


        # Group the two bars.
        fig.update_layout(

            barmode="group",

            title=(
                "Plan Liability vs Funded Assets"
            ),

            xaxis_title="Plan",

            yaxis_title="INR",
        )


        # Display chart.
        st.plotly_chart(

            fig,

            use_container_width=True
        )


        # ---------------------------------------------------------------------
        # FUNDING RATIO
        # ---------------------------------------------------------------------


        fig = px.bar(

            funded,

            x="plan_id",

            y="funding_ratio_pct",

            labels={

                "plan_id":
                    "Plan",

                "funding_ratio_pct":
                    "Funding Ratio (%)",
            },

            title="Funding Ratio by Plan",
        )


        # Display.
        st.plotly_chart(

            fig,

            use_container_width=True
        )


        # Display source table.
        st.subheader(
            "Plan Funding Detail"
        )


        st.dataframe(

            funded,

            use_container_width=True,

            hide_index=True,
        )


# =============================================================================
# PAGE 3 - DC SUPERANNUATION
# =============================================================================


elif page == "DC Superannuation":


    # Page heading.
    st.header(
        "Defined Contribution Superannuation"
    )


    # Keep DC plans.
    dc = plans.loc[

        plans[
            "product_type"
        ].eq(
            "DC_Superannuation"
        )

    ].copy()


    # -------------------------------------------------------------------------
    # COMPANY-LEVEL DC KPIs
    # -------------------------------------------------------------------------


    cols = st.columns(
        3
    )


    with cols[0]:

        show_metric(
            "DC Members",
            get_kpi(
                "dc_members"
            ),
            "integer",
        )


    # Employer contributions from plan data.
    employer_contribution = (

        pd.to_numeric(

            dc.get(
                "annual_employer_contribution",
                pd.Series(dtype=float),
            ),

            errors="coerce"

        ).sum()
    )


    with cols[1]:

        show_metric(
            "Annual Employer Contributions",
            employer_contribution,
            "currency",
        )


    with cols[2]:

        show_metric(
            "Future-Contribution Corpus",
            get_kpi(
                "dc_future_corpus"
            ),
            "currency",
        )


    # -------------------------------------------------------------------------
    # FUTURE CORPUS BY PLAN
    # -------------------------------------------------------------------------


    if not dc.empty:


        fig = px.bar(

            dc,

            x="plan_id",

            y="projected_future_contribution_corpus",

            labels={

                "plan_id":
                    "DC Plan",

                "projected_future_contribution_corpus":
                    "Future-Contribution Corpus (INR)",
            },

            title=(
                "Projected Future-Contribution Corpus by DC Plan"
            ),
        )


        st.plotly_chart(

            fig,

            use_container_width=True
        )


        # Contribution comparison.
        contribution_columns = [

            column

            for column in [

                "plan_id",

                "annual_employer_contribution",

                "annual_employee_contribution",

                "projected_future_contribution_corpus",
            ]

            if column
            in dc.columns
        ]


        st.subheader(
            "DC Plan Detail"
        )


        st.dataframe(

            dc[
                contribution_columns
            ],

            use_container_width=True,

            hide_index=True,
        )


    # Explicit model limitation.
    st.info(
        "Projected DC values represent the future-contribution corpus. "
        "Opening individual member corpus was not available and is not "
        "fabricated or replaced with pooled plan assets."
    )


# =============================================================================
# PAGE 4 - GROUP RISK
# =============================================================================


elif page == "Group Risk — GTI & EDLI":


    # Page heading.
    st.header(
        "Group Risk — GTI & EDLI"
    )


    # -------------------------------------------------------------------------
    # GTI SECTION
    # -------------------------------------------------------------------------


    st.subheader(
        "Group Term Insurance"
    )


    # Keep GTI plans.
    gti = plans.loc[

        plans[
            "product_type"
        ].eq(
            "GTI"
        )

    ].copy()


    # KPI cards.
    cols = st.columns(
        4
    )


    with cols[0]:

        show_metric(
            "Total Sum Assured",
            get_kpi(
                "gti_total_sum_assured"
            ),
            "currency",
        )


    with cols[1]:

        show_metric(
            "Fresh Expected Claims",
            get_kpi(
                "gti_expected_claims"
            ),
            "currency",
        )


    with cols[2]:

        show_metric(
            "Fresh Gross Premium",
            get_kpi(
                "gti_fresh_gross_premium"
            ),
            "currency",
        )


    with cols[3]:

        show_metric(
            "FCL Referrals",
            get_kpi(
                "gti_fcl_referrals"
            ),
            "integer",
        )


    # GTI Sum Assured chart.
    if not gti.empty:


        fig = px.bar(

            gti,

            x="plan_id",

            y="total_sum_assured",

            labels={

                "plan_id":
                    "GTI Plan",

                "total_sum_assured":
                    "Sum Assured (INR)",
            },

            title="GTI Sum Assured by Plan",
        )


        st.plotly_chart(

            fig,

            use_container_width=True
        )


        # Expected claims chart.
        fig = px.bar(

            gti,

            x="plan_id",

            y="fresh_expected_claim_cost",

            labels={

                "plan_id":
                    "GTI Plan",

                "fresh_expected_claim_cost":
                    "Fresh Expected Claims (INR)",
            },

            title="Fresh Expected Claims by GTI Plan",
        )


        st.plotly_chart(

            fig,

            use_container_width=True
        )


        # FCL referrals.
        fig = px.bar(

            gti,

            x="plan_id",

            y="underwriting_referrals",

            labels={

                "plan_id":
                    "GTI Plan",

                "underwriting_referrals":
                    "Employees",
            },

            title="Free-Cover-Limit Underwriting Referrals",
        )


        st.plotly_chart(

            fig,

            use_container_width=True
        )


    # Explain premium basis.
    st.success(
        "Final GTI dashboard premium uses the fresh expected-claims "
        "pricing basis. Historical A/E credibility-adjusted pricing "
        "is intentionally excluded from the final KPI."
    )


    # -------------------------------------------------------------------------
    # EDLI SECTION
    # -------------------------------------------------------------------------


    st.subheader(
        "Employees' Deposit Linked Insurance"
    )


    # Keep EDLI plan.
    edli = plans.loc[

        plans[
            "product_type"
        ].eq(
            "EDLI"
        )

    ].copy()


    # Aggregate EDLI indicative ranges.
    edli_lower = pd.to_numeric(

        edli.get(

            "edli_part_b_lower_if_qualifying",

            pd.Series(dtype=float),
        ),

        errors="coerce"

    ).sum()


    edli_upper = pd.to_numeric(

        edli.get(

            "edli_part_b_upper_if_qualifying",

            pd.Series(dtype=float),
        ),

        errors="coerce"

    ).sum()


    # Display range.
    cols = st.columns(
        3
    )


    with cols[0]:

        show_metric(
            "EDLI Members",
            8501,
            "integer",
        )


    with cols[1]:

        show_metric(
            "Indicative Part B Lower",
            edli_lower,
            "currency",
        )


    with cols[2]:

        show_metric(
            "Indicative Part B Upper",
            edli_upper,
            "currency",
        )


    # EDLI governance warning.
    st.warning(
        "EDLI is an effective-date-sensitive statutory benefit. "
        "The displayed Part B range is analytical and must not be "
        "treated as the final official settlement amount. "
        "Official calculator verification remains required."
    )


# =============================================================================
# PAGE 5 - WORKFORCE CONCENTRATION
# =============================================================================


elif page == "Workforce Concentration":


    # Page heading.
    st.header(
        "Workforce Benefit & Risk Concentration"
    )


    # Confirm segment data exist.
    if segments.empty:


        st.warning(
            "No segment concentration data are available."
        )


    else:


        # Available segmentation types.
        segment_types = sorted(

            segments[
                "segment_type"
            ]

            .dropna()

            .unique()
        )


        # Select segmentation dimension.
        selected_segment = st.selectbox(

            "Segment By",

            segment_types,
        )


        # Available risk measures.
        risk_options = {

            "Defined Benefit Liability":
                "combined_db_liability",

            "DC Future-Contribution Corpus":
                "projected_future_contribution_corpus",

            "GTI Sum Assured":
                "gti_sum_assured",

            "GTI Expected Claims":
                "gti_fresh_expected_claim_cost",

            "GTI Fresh Gross Premium":
                "gti_fresh_model_gross_premium",
        }


        # Let user select metric.
        selected_label = st.selectbox(

            "Risk Measure",

            list(
                risk_options.keys()
            ),
        )


        # Resolve field.
        selected_metric = risk_options[
            selected_label
        ]


        # Filter selected segment type.
        segment_view = segments.loc[

            segments[
                "segment_type"
            ].eq(
                selected_segment
            )

        ].copy()


        # Sort largest first.
        segment_view = segment_view.sort_values(

            selected_metric,

            ascending=False
        )


        # Draw concentration chart.
        fig = px.bar(

            segment_view,

            x="segment_value",

            y=selected_metric,

            labels={

                "segment_value":
                    selected_segment.title(),

                selected_metric:
                    selected_label,
            },

            title=(
                f"{selected_label} by "
                f"{selected_segment.title()}"
            ),
        )


        # Display chart.
        st.plotly_chart(

            fig,

            use_container_width=True
        )


        # Display concentration table.
        st.dataframe(

            segment_view,

            use_container_width=True,

            hide_index=True,
        )


# =============================================================================
# PAGE 6 - EMPLOYEE DRILL-DOWN
# =============================================================================


elif page == "Employee Drill-Down":


    # Page heading.
    st.header(
        "Employee Benefit Drill-Down"
    )


    # Start with complete employee table.
    filtered_employees = employees.copy()


    # -------------------------------------------------------------------------
    # DEPARTMENT FILTER
    # -------------------------------------------------------------------------


    if "department" in employees.columns:


        departments = sorted(

            employees[
                "department"
            ]

            .dropna()

            .astype(
                str
            )

            .unique()
        )


        selected_departments = st.multiselect(

            "Department",

            departments,
        )


        # Apply selection.
        if selected_departments:


            filtered_employees = filtered_employees.loc[

                filtered_employees[
                    "department"
                ].astype(
                    str
                ).isin(
                    selected_departments
                )
            ]


    # -------------------------------------------------------------------------
    # LOCATION FILTER
    # -------------------------------------------------------------------------


    if "location" in employees.columns:


        locations = sorted(

            employees[
                "location"
            ]

            .dropna()

            .astype(
                str
            )

            .unique()
        )


        selected_locations = st.multiselect(

            "Location",

            locations,
        )


        # Apply selection.
        if selected_locations:


            filtered_employees = filtered_employees.loc[

                filtered_employees[
                    "location"
                ].astype(
                    str
                ).isin(
                    selected_locations
                )
            ]


    # -------------------------------------------------------------------------
    # GRADE FILTER
    # -------------------------------------------------------------------------


    if "grade" in employees.columns:


        grades = sorted(

            employees[
                "grade"
            ]

            .dropna()

            .astype(
                str
            )

            .unique()
        )


        selected_grades = st.multiselect(

            "Grade",

            grades,
        )


        # Apply selection.
        if selected_grades:


            filtered_employees = filtered_employees.loc[

                filtered_employees[
                    "grade"
                ].astype(
                    str
                ).isin(
                    selected_grades
                )
            ]


    # -------------------------------------------------------------------------
    # EMPLOYEE COUNT
    # -------------------------------------------------------------------------


    show_metric(
        "Employees in Current Selection",
        len(
            filtered_employees
        ),
        "integer",
    )


    # -------------------------------------------------------------------------
    # EMPLOYEE TABLE
    # -------------------------------------------------------------------------


    st.dataframe(

        filtered_employees,

        use_container_width=True,

        hide_index=True,

        height=600,
    )


    # -------------------------------------------------------------------------
    # DOWNLOAD FILTERED EMPLOYEE DATA
    # -------------------------------------------------------------------------


    st.download_button(

        label="Download Filtered Employee Data",

        data=filtered_employees.to_csv(
            index=False
        ).encode(
            "utf-8"
        ),

        file_name=(
            "employee_benefit_drilldown.csv"
        ),

        mime="text/csv",
    )


# =============================================================================
# PAGE 7 - GOVERNANCE AND VALIDATION
# =============================================================================


elif page == "Governance & Validation":


    # Page heading.
    st.header(
        "Model Governance & Validation"
    )


    # -------------------------------------------------------------------------
    # VALIDATION STATUS
    # -------------------------------------------------------------------------


    st.subheader(
        "Portfolio Validation"
    )


    # Count failures.
    validation_failures = int(

        validation[
            "status"
        ].astype(
            str
        ).str.upper().eq(
            "FAIL"
        ).sum()
    )


    # Count passed checks.
    validation_passes = int(

        validation[
            "status"
        ].astype(
            str
        ).str.upper().eq(
            "PASS"
        ).sum()
    )


    # Show validation metrics.
    cols = st.columns(
        2
    )


    with cols[0]:

        show_metric(
            "Validation Checks Passed",
            validation_passes,
            "integer",
        )


    with cols[1]:

        show_metric(
            "Validation Failures",
            validation_failures,
            "integer",
        )


    # Clear status.
    if validation_failures == 0:


        st.success(
            "All Pipeline 10 portfolio validation checks passed."
        )


    else:


        st.error(
            "One or more portfolio validation checks failed."
        )


    # Display validation table.
    st.dataframe(

        validation,

        use_container_width=True,

        hide_index=True,
    )


    # -------------------------------------------------------------------------
    # GOVERNANCE
    # -------------------------------------------------------------------------


    st.subheader(
        "Governance Register"
    )


    # Keep active reviews first.
    governance_view = governance.copy()


    # Convert counts.
    governance_view[
        "review_rows"
    ] = pd.to_numeric(

        governance_view[
            "review_rows"
        ],

        errors="coerce"

    ).fillna(
        0
    )


    # Sort largest governance review first.
    governance_view = governance_view.sort_values(

        "review_rows",

        ascending=False
    )


    # Display.
    st.dataframe(

        governance_view,

        use_container_width=True,

        hide_index=True,
    )


    # Explain governance distinction.
    st.info(
        "Governance reviews are documented model limitations, "
        "fallbacks or business-review items. They are not automatically "
        "mathematical validation failures."
    )


# =============================================================================
# FOOTER
# =============================================================================


# Separate footer from page content.
st.divider()


# Display project identity.
st.caption(
    "Hessian-AI • Quantitative Actuarial Employee Benefits Dashboard • "
    "Valuation Date: 1 September 2026 • Dashboard Data Mart: P11-C01"
)