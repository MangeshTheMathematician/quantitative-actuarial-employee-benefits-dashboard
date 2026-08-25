# =============================================================================
# HESSIAN-AI
# QUANTITATIVE ACTUARIAL EMPLOYEE BENEFITS DASHBOARD
# STREAMLIT APPLICATION
#
# DASHBOARD DATA SOURCE:
# Pipeline 11 — Dashboard Data Mart
#
# IMPORTANT:
# This application DOES NOT recalculate actuarial liabilities.
# It consumes validated dashboard-ready outputs produced by Pipelines 01–11.
# =============================================================================


# =============================================================================
# IMPORTS
# =============================================================================

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Hessian-AI Employee Benefits Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# PROJECT PATHS
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = (
    PROJECT_ROOT
    / "Data"
    / "dashboard_ready"
)


# =============================================================================
# PIPELINE 11 DASHBOARD FILES
# =============================================================================

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

@st.cache_data(show_spinner=False)
def load_dashboard_file(
    file_name,
):

    path = (
        DATA_DIR
        / file_name
    )

    if not path.exists():

        return pd.DataFrame()

    return pd.read_csv(
        path
    )


# =============================================================================
# LOAD DASHBOARD DATA
# =============================================================================

kpis = load_dashboard_file(
    FILES["kpis"]
)

products = load_dashboard_file(
    FILES["products"]
)

plans = load_dashboard_file(
    FILES["plans"]
)

employees = load_dashboard_file(
    FILES["employees"]
)

segments = load_dashboard_file(
    FILES["segments"]
)

governance = load_dashboard_file(
    FILES["governance"]
)

validation = load_dashboard_file(
    FILES["validation"]
)

filters = load_dashboard_file(
    FILES["filters"]
)

visual_catalog = load_dashboard_file(
    FILES["visual_catalog"]
)

manifest = load_dashboard_file(
    FILES["manifest"]
)


# =============================================================================
# CRITICAL DATA CHECK
# =============================================================================

if kpis.empty:

    st.error(
        "Pipeline 11 dashboard-ready KPI data could not be found."
    )

    st.code(
        str(DATA_DIR)
    )

    st.stop()


# =============================================================================
# DISPLAY CONSTANTS
# =============================================================================

MISSING_TEXT = {
    "",
    "none",
    "nan",
    "nat",
    "<na>",
}


PRODUCT_LABELS = {

    "Gratuity":
        "Gratuity",

    "DB_Pension":
        "DB Pension",

    "DC_Superannuation":
        "DC Superannuation",

    "GTI":
        "Group Term Insurance",

    "EDLI":
        "EDLI",
}


DISPLAY_LABELS = {

    "plan_id":
        "Plan",

    "product_type":
        "Product",

    "active_members":
        "Active Members",

    "employee_id":
        "Employee ID",

    "employment_status":
        "Status",

    "department":
        "Department",

    "location":
        "Location",

    "grade":
        "Grade",

    "attained_age_years":
        "Age",

    "completed_service_years":
        "Completed Service",

    "gratuity_plan_id":
        "Gratuity Plan",

    "db_pension_plan_id":
        "DB Pension Plan",

    "dc_superannuation_plan_id":
        "DC Superannuation Plan",

    "gti_pricing_plan_id":
        "GTI Plan",

    "edli_plan_id":
        "EDLI Plan",

    "actuarial_liability":
        "Actuarial Liability",

    "puc_one_service_year_pv":
        "PUC One-Service-Year PV",

    "plan_assets":
        "Plan Assets",

    "funding_ratio_pct":
        "Funding Ratio",

    "funding_ratio":
        "Funding Ratio",

    "funding_deficit":
        "Funding Deficit",

    "funding_gap":
        "Funding Gap",

    "net_funded_position":
        "Net Funded Position",

    "annual_employer_contribution":
        "Annual Employer Contribution",

    "annual_employee_contribution":
        "Annual Employee Contribution",

    "current_annual_employer_contribution":
        "Annual Employer Contribution",

    "current_annual_employee_contribution":
        "Annual Employee Contribution",

    "projected_future_contribution_corpus":
        "Future-Contribution Corpus",

    "total_sum_assured":
        "Total Sum Assured",

    "gti_sum_assured":
        "GTI Sum Assured",

    "fresh_expected_claim_cost":
        "Fresh Expected Claims",

    "gti_fresh_expected_claim_cost":
        "GTI Fresh Expected Claims",

    "fresh_model_gross_premium":
        "Fresh Gross Premium",

    "gti_fresh_model_gross_premium":
        "GTI Fresh Gross Premium",

    "underwriting_referrals":
        "FCL Referrals",

    "gti_fcl_referral_rate":
        "FCL Referral Rate",

    "cover_above_free_cover_limit":
        "Cover Above FCL",

    "gti_cover_above_free_cover_limit":
        "GTI Cover Above FCL",

    "edli_part_b_lower_if_qualifying":
        "EDLI Part B Lower",

    "edli_part_b_upper_if_qualifying":
        "EDLI Part B Upper",

    "gratuity_dbo":
        "Gratuity DBO",

    "db_pension_liability":
        "DB Pension DBO",

    "combined_db_liability":
        "Combined DB Liability",

    "segment_type":
        "Segment Type",

    "segment_value":
        "Segment",

    "employee_count":
        "Employees",

    "portfolio_share_pct":
        "Portfolio Share",

    "governance_item":
        "Governance Item",

    "review_rows":
        "Review Rows",

    "treatment":
        "Treatment",

    "source_pipeline":
        "Source Pipeline",

    "dashboard_status":
        "Status",

    "check":
        "Validation Check",

    "exceptions":
        "Exceptions",

    "status":
        "Status",

    "note":
        "Note",
}


# =============================================================================
# GENERAL NUMERIC HELPERS
# =============================================================================

def to_number(
    value,
):

    if value is None:

        return np.nan

    if isinstance(
        value,
        (
            int,
            float,
            np.integer,
            np.floating,
        ),
    ):

        return float(
            value
        )

    text = (
        str(value)
        .strip()
        .replace(
            ",",
            "",
        )
    )

    if text.lower() in MISSING_TEXT:

        return np.nan

    return pd.to_numeric(
        text,
        errors="coerce",
    )


def numeric_series(
    df,
    column,
):

    if column not in df.columns:

        return pd.Series(
            index=df.index,
            dtype=float,
        )

    return pd.to_numeric(

        df[
            column
        ]
        .astype(
            str
        )
        .str.replace(
            ",",
            "",
            regex=False,
        ),

        errors="coerce",
    )


def safe_sum(
    df,
    column,
):

    if (
        df.empty
        or column not in df.columns
    ):

        return 0.0

    return float(

        numeric_series(
            df,
            column,
        )

        .fillna(
            0
        )

        .sum()
    )


def nonempty_mask(
    series,
):

    text = (
        series
        .astype(
            str
        )
        .str.strip()
    )

    return (

        series.notna()

        &

        ~text
        .str.lower()
        .isin(
            MISSING_TEXT
        )
    )


# =============================================================================
# EMPLOYEE MEMBERSHIP HELPERS
# =============================================================================

def active_employee_frame(
    df,
):

    if df.empty:

        return df.copy()

    if "employment_status" not in df.columns:

        return df.copy()

    status = (

        df[
            "employment_status"
        ]

        .astype(
            str
        )

        .str.strip()

        .str.lower()
    )

    return df.loc[
        status.eq(
            "active"
        )
    ].copy()


def count_active_plan_members(
    column_candidates,
):

    if employees.empty:

        return 0

    base = active_employee_frame(
        employees
    )

    for column in column_candidates:

        if column in base.columns:

            return int(

                nonempty_mask(
                    base[
                        column
                    ]
                )

                .sum()
            )

    return 0


# =============================================================================
# KPI HELPERS
# =============================================================================

def get_kpi(
    kpi_id,
    default=np.nan,
):

    if (

        kpis.empty

        or "kpi_id"
        not in kpis.columns

        or "numeric_value"
        not in kpis.columns
    ):

        return default

    match = kpis.loc[

        kpis[
            "kpi_id"
        ]
        .astype(
            str
        )
        .eq(
            kpi_id
        )

    ]

    if match.empty:

        return default

    value = to_number(

        match[
            "numeric_value"
        ]
        .iloc[
            0
        ]
    )

    if pd.isna(
        value
    ):

        return default

    return value


def get_kpi_any(
    kpi_ids,
    default=np.nan,
):

    for kpi_id in kpi_ids:

        value = get_kpi(
            kpi_id,
            default=np.nan,
        )

        if not pd.isna(
            value
        ):

            return value

    return default


# =============================================================================
# PRODUCT HELPERS
# =============================================================================

def normalize_product(
    value,
):

    return (

        str(
            value
        )

        .strip()

        .lower()

        .replace(
            " ",
            "_",
        )

        .replace(
            "-",
            "_",
        )
    )


def product_frame(
    df,
    product_names,
):

    if (

        df.empty

        or "product_type"
        not in df.columns
    ):

        return pd.DataFrame(
            columns=df.columns
        )

    targets = {

        normalize_product(
            name
        )

        for name in product_names
    }

    normalized = (

        df[
            "product_type"
        ]

        .astype(
            str
        )

        .map(
            normalize_product
        )
    )

    return df.loc[
        normalized.isin(
            targets
        )
    ].copy()


def product_label(
    value,
):

    text = str(
        value
    )

    return PRODUCT_LABELS.get(

        text,

        text.replace(
            "_",
            " ",
        ),
    )


# =============================================================================
# BOOLEAN HELPERS
# =============================================================================

def truthy_mask(
    series,
):

    return (

        series
        .astype(
            str
        )

        .str.strip()

        .str.lower()

        .isin(
            {
                "true",
                "1",
                "yes",
                "y",
                "t",
            }
        )
    )


def yes_no(
    value,
):

    if value is None:

        return "—"

    if (
        isinstance(
            value,
            float,
        )

        and pd.isna(
            value
        )
    ):

        return "—"

    text = (
        str(
            value
        )
        .strip()
        .lower()
    )

    if text in MISSING_TEXT:

        return "—"

    if text in {

        "true",
        "1",
        "yes",
        "y",
        "t",

    }:

        return "Yes"

    if text in {

        "false",
        "0",
        "no",
        "n",
        "f",

    }:

        return "No"

    return str(
        value
    )


# =============================================================================
# COLUMN HELPERS
# =============================================================================

def first_existing_column(
    df,
    candidates,
):

    for column in candidates:

        if column in df.columns:

            return column

    return None


def select_existing(
    df,
    columns,
):

    return [

        column

        for column
        in columns

        if column
        in df.columns
    ]


# =============================================================================
# NUMBER FORMATTING
# =============================================================================

def format_integer(
    value,
):

    value = to_number(
        value
    )

    if pd.isna(
        value
    ):

        return "—"

    return f"{int(round(value)):,}"


def format_decimal(
    value,
    digits=2,
):

    value = to_number(
        value
    )

    if pd.isna(
        value
    ):

        return "—"

    return f"{value:,.{digits}f}"


def format_inr_compact(
    value,
):

    value = to_number(
        value
    )

    if pd.isna(
        value
    ):

        return "—"

    sign = (
        "-"
        if value < 0
        else ""
    )

    amount = abs(
        value
    )

    if amount >= 1_000_000_000:

        return (
            f"{sign}₹"
            f"{amount / 1_000_000_000:,.2f}B"
        )

    if amount >= 1_000_000:

        return (
            f"{sign}₹"
            f"{amount / 1_000_000:,.2f}M"
        )

    if amount >= 1_000:

        return (
            f"{sign}₹"
            f"{amount / 1_000:,.2f}K"
        )

    return (
        f"{sign}₹{amount:,.2f}"
    )


def format_inr_exact(
    value,
):

    value = to_number(
        value
    )

    if pd.isna(
        value
    ):

        return "—"

    sign = (
        "-"
        if value < 0
        else ""
    )

    return (
        f"{sign}₹{abs(value):,.2f}"
    )


def format_percent(
    value,
    value_is_ratio=True,
    digits=2,
):

    value = to_number(
        value
    )

    if pd.isna(
        value
    ):

        return "—"

    if value_is_ratio:

        pct = (
            value
            * 100
        )

    else:

        pct = value

    return (
        f"{pct:,.{digits}f}%"
    )


# =============================================================================
# PROFESSIONAL TABLE FORMATTER
# =============================================================================

def pretty_table(
    df,
    columns,
    *,
    labels=None,
    money=None,
    compact_money=None,
    integers=None,
    decimals=None,
    pct_ratio=None,
    pct_values=None,
    booleans=None,
    product_columns=None,
):

    labels = (
        labels
        or {}
    )

    money = set(
        money
        or []
    )

    compact_money = set(
        compact_money
        or []
    )

    integers = set(
        integers
        or []
    )

    decimals = (
        decimals
        or {}
    )

    pct_ratio = set(
        pct_ratio
        or []
    )

    pct_values = set(
        pct_values
        or []
    )

    booleans = set(
        booleans
        or []
    )

    product_columns = set(
        product_columns
        or []
    )

    selected = select_existing(
        df,
        columns,
    )

    out = df[
        selected
    ].copy()

    for column in selected:

        if column in money:

            out[
                column
            ] = out[
                column
            ].map(
                format_inr_exact
            )

        elif column in compact_money:

            out[
                column
            ] = out[
                column
            ].map(
                format_inr_compact
            )

        elif column in integers:

            out[
                column
            ] = out[
                column
            ].map(
                format_integer
            )

        elif column in decimals:

            digits = decimals[
                column
            ]

            out[
                column
            ] = out[
                column
            ].map(

                lambda x:
                    format_decimal(
                        x,
                        digits,
                    )
            )

        elif column in pct_ratio:

            out[
                column
            ] = out[
                column
            ].map(

                lambda x:
                    format_percent(
                        x,
                        True,
                    )
            )

        elif column in pct_values:

            out[
                column
            ] = out[
                column
            ].map(

                lambda x:
                    format_percent(
                        x,
                        False,
                    )
            )

        elif column in booleans:

            out[
                column
            ] = out[
                column
            ].map(
                yes_no
            )

        elif column in product_columns:

            out[
                column
            ] = out[
                column
            ].map(
                product_label
            )

        else:

            out[
                column
            ] = out[
                column
            ].map(

                lambda x:

                    "—"

                    if (

                        x is None

                        or (

                            isinstance(
                                x,
                                float,
                            )

                            and pd.isna(
                                x
                            )
                        )

                        or str(
                            x
                        )
                        .strip()
                        .lower()
                        in MISSING_TEXT

                    )

                    else str(
                        x
                    )
            )

    rename_map = {

        column:

            labels.get(

                column,

                DISPLAY_LABELS.get(

                    column,

                    column
                    .replace(
                        "_",
                        " ",
                    )
                    .title(),
                ),
            )

        for column
        in selected
    }

    return out.rename(
        columns=rename_map
    )


# =============================================================================
# METRIC HELPER
# =============================================================================

def show_metric(
    label,
    value,
    kind="number",
):

    if kind == "currency":

        display = format_inr_compact(
            value
        )

    elif kind == "integer":

        display = format_integer(
            value
        )

    elif kind == "ratio":

        display = format_percent(
            value,
            value_is_ratio=True,
        )

    elif kind == "percentage":

        display = format_percent(
            value,
            value_is_ratio=False,
        )

    else:

        numeric_value = to_number(
            value
        )

        if pd.isna(
            numeric_value
        ):

            display = "—"

        else:

            display = str(
                value
            )

    st.metric(
        label=label,
        value=display,
    )


# =============================================================================
# CHART HELPER
# =============================================================================

def clean_chart(
    fig,
    *,
    height=410,
    y_title=None,
    show_legend=None,
):

    fig.update_layout(

        height=height,

        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10,
        ),

        hoverlabel=dict(
            namelength=-1,
        ),

        legend_title_text="",
    )

    if y_title:

        fig.update_yaxes(
            title_text=y_title
        )

    if show_legend is not None:

        fig.update_layout(
            showlegend=show_legend
        )

    return fig


# =============================================================================
# FUNDED DB PLAN FILTER
# =============================================================================

def funded_db_plans():

    if plans.empty:

        return plans.copy()

    if "funded_db_product_flag" in plans.columns:

        mask = truthy_mask(

            plans[
                "funded_db_product_flag"
            ]
        )

        funded_result = plans.loc[
            mask
        ].copy()

        if not funded_result.empty:

            return funded_result

    return product_frame(

        plans,

        [
            "Gratuity",
            "DB_Pension",
            "DB Pension",
        ],
    )


# =============================================================================
# GOVERNED VALUATION DATE
# =============================================================================

def infer_valuation_date():

    for df in [

        manifest,
        plans,
        products,
        kpis,

    ]:

        if df.empty:

            continue

        column = first_existing_column(

            df,

            [
                "valuation_date",
                "as_of_date",
                "data_date",
            ],
        )

        if column:

            values = (
                df[
                    column
                ]
                .dropna()
            )

            if not values.empty:

                parsed = pd.to_datetime(

                    values.iloc[
                        0
                    ],

                    errors="coerce",
                )

                if not pd.isna(
                    parsed
                ):

                    return (

                        f"{parsed.day} "
                        f"{parsed.strftime('%B %Y')}"
                    )

    return "1 September 2026"


# =============================================================================
# PIPELINE VERSION
# =============================================================================

def infer_pipeline_version():

    for df in [

        validation,
        governance,
        plans,
        products,
        manifest,

    ]:

        if df.empty:

            continue

        column = first_existing_column(

            df,

            [
                "pipeline_11_version",
                "dashboard_mart_version",
                "version",
            ],
        )

        if column:

            values = (

                df[
                    column
                ]

                .dropna()

                .astype(
                    str
                )
            )

            values = values.loc[

                ~values

                .str.strip()

                .str.lower()

                .isin(
                    MISSING_TEXT
                )

            ]

            if not values.empty:

                return values.iloc[
                    0
                ]

    return "P11-C01"


VALUATION_DATE = infer_valuation_date()

DASHBOARD_VERSION = infer_pipeline_version()


# =============================================================================
# PORTFOLIO MEMBER COUNTS
# =============================================================================

active_employees = get_kpi_any(

    [
        "active_employees",
    ],

    default=len(
        active_employee_frame(
            employees
        )
    ),
)


gratuity_members = get_kpi_any(

    [
        "gratuity_members",
        "active_gratuity_members",
    ],

    default=count_active_plan_members(
        [
            "gratuity_plan_id",
        ]
    ),
)


db_pension_members = get_kpi_any(

    [
        "db_pension_members",
        "active_db_pension_members",
    ],

    default=count_active_plan_members(
        [
            "db_pension_plan_id",
        ]
    ),
)


dc_members = get_kpi_any(

    [
        "dc_members",
        "active_dc_members",
    ],

    default=count_active_plan_members(
        [
            "dc_superannuation_plan_id",
        ]
    ),
)


edli_members = get_kpi_any(

    [
        "edli_members",
        "active_edli_members",
    ],

    default=count_active_plan_members(
        [
            "edli_plan_id",
        ]
    ),
)


gti_members = get_kpi_any(

    [
        "gti_members",
        "active_gti_members",
    ],

    default=count_active_plan_members(

        [
            "gti_pricing_plan_id",
            "gti_plan_id",
        ]
    ),
)


# =============================================================================
# PRODUCT FRAMES
# =============================================================================

funded = funded_db_plans()


dc_plans = product_frame(

    plans,

    [
        "DC_Superannuation",
        "DC Superannuation",
    ],
)


gti_plans = product_frame(

    plans,

    [
        "GTI",
    ],
)


edli_plans = product_frame(

    plans,

    [
        "EDLI",
    ],
)


# =============================================================================
# PORTFOLIO DB METRICS
# =============================================================================

combined_db_liability = get_kpi_any(

    [
        "combined_db_liability",
    ],

    default=safe_sum(
        funded,
        "actuarial_liability",
    ),
)


combined_db_assets = get_kpi_any(

    [
        "combined_db_assets",
        "combined_db_plan_assets",
    ],

    default=safe_sum(
        funded,
        "plan_assets",
    ),
)


combined_db_funding_ratio = get_kpi_any(

    [
        "combined_db_funding_ratio",
    ],

    default=(

        combined_db_assets
        /
        combined_db_liability

        if combined_db_liability > 0

        else np.nan
    ),
)


combined_db_funding_deficit = get_kpi_any(

    [
        "combined_db_funding_deficit",
    ],

    default=max(

        combined_db_liability
        -
        combined_db_assets,

        0,
    ),
)


# =============================================================================
# DC METRICS
# =============================================================================

dc_employer_contribution = get_kpi_any(

    [
        "dc_annual_employer_contributions",
        "annual_dc_employer_contributions",
    ],

    default=safe_sum(
        dc_plans,
        "annual_employer_contribution",
    ),
)


dc_employee_contribution = get_kpi_any(

    [
        "dc_annual_employee_contributions",
        "annual_dc_employee_contributions",
    ],

    default=safe_sum(
        dc_plans,
        "annual_employee_contribution",
    ),
)


dc_future_corpus = get_kpi_any(

    [
        "dc_future_corpus",
        "dc_future_contribution_corpus",
    ],

    default=safe_sum(
        dc_plans,
        "projected_future_contribution_corpus",
    ),
)


# =============================================================================
# GTI METRICS
# =============================================================================

gti_total_sum_assured = get_kpi_any(

    [
        "gti_total_sum_assured",
    ],

    default=safe_sum(
        gti_plans,
        "total_sum_assured",
    ),
)


gti_expected_claims = get_kpi_any(

    [
        "gti_expected_claims",
        "gti_fresh_expected_claims",
    ],

    default=safe_sum(
        gti_plans,
        "fresh_expected_claim_cost",
    ),
)


gti_fresh_gross_premium = get_kpi_any(

    [
        "gti_fresh_gross_premium",
        "gti_fresh_model_gross_premium",
    ],

    default=safe_sum(
        gti_plans,
        "fresh_model_gross_premium",
    ),
)


gti_fcl_referrals = get_kpi_any(

    [
        "gti_fcl_referrals",
    ],

    default=safe_sum(
        gti_plans,
        "underwriting_referrals",
    ),
)


gti_fcl_referral_rate = get_kpi_any(

    [
        "gti_fcl_referral_rate",
    ],

    default=(

        gti_fcl_referrals
        /
        gti_members

        if gti_members

        else np.nan
    ),
)


# =============================================================================
# VALIDATION STATUS
# =============================================================================

validation_failure_count = 0


if (

    not validation.empty

    and "status"
    in validation.columns
):

    validation_failure_count = int(

        validation[
            "status"
        ]

        .astype(
            str
        )

        .str.upper()

        .eq(
            "FAIL"
        )

        .sum()
    )


# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.title(
    "Hessian-AI"
)


st.sidebar.caption(
    "Quantitative Actuarial Employee Benefits Dashboard"
)


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


st.sidebar.divider()


st.sidebar.markdown(
    "**Valuation Date**"
)


st.sidebar.write(
    VALUATION_DATE
)


st.sidebar.markdown(
    "**Data Layer**"
)


st.sidebar.write(
    f"Pipeline 11 — {DASHBOARD_VERSION}"
)


if validation_failure_count == 0:

    st.sidebar.success(
        "Portfolio validation passed"
    )

else:

    st.sidebar.error(

        f"{validation_failure_count} "
        f"validation failure(s)"
    )


# =============================================================================
# COMMON PAGE HEADER
# =============================================================================

st.title(
    "Quantitative Actuarial Employee Benefits Dashboard"
)


st.caption(
    "Gratuity · Superannuation · DB Pension · EDLI · "
    "Group Term Insurance · Funding · Risk · Governance"
)


# =============================================================================
# PAGE 1
# EXECUTIVE OVERVIEW
# =============================================================================

if page == "Executive Overview":


    st.header(
        "Executive Overview"
    )


    # -------------------------------------------------------------------------
    # COVERED WORKFORCE
    # -------------------------------------------------------------------------

    st.subheader(
        "Covered Workforce"
    )


    cols = st.columns(
        6
    )


    with cols[0]:

        show_metric(
            "Active Employees",
            active_employees,
            "integer",
        )


    with cols[1]:

        show_metric(
            "Gratuity",
            gratuity_members,
            "integer",
        )


    with cols[2]:

        show_metric(
            "DB Pension",
            db_pension_members,
            "integer",
        )


    with cols[3]:

        show_metric(
            "DC Superannuation",
            dc_members,
            "integer",
        )


    with cols[4]:

        show_metric(
            "EDLI",
            edli_members,
            "integer",
        )


    with cols[5]:

        show_metric(
            "GTI",
            gti_members,
            "integer",
        )


    # -------------------------------------------------------------------------
    # DEFINED BENEFIT FUNDING
    # -------------------------------------------------------------------------

    st.subheader(
        "Defined Benefit Funding"
    )


    cols = st.columns(
        4
    )


    with cols[0]:

        show_metric(
            "Combined DB Liability",
            combined_db_liability,
            "currency",
        )


    with cols[1]:

        show_metric(
            "DB Plan Assets",
            combined_db_assets,
            "currency",
        )


    with cols[2]:

        show_metric(
            "Funding Ratio",
            combined_db_funding_ratio,
            "ratio",
        )


    with cols[3]:

        show_metric(
            "Funding Deficit",
            combined_db_funding_deficit,
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
            gti_total_sum_assured,
            "currency",
        )


    with cols[1]:

        show_metric(
            "Expected Claims",
            gti_expected_claims,
            "currency",
        )


    with cols[2]:

        show_metric(
            "Fresh Gross Premium",
            gti_fresh_gross_premium,
            "currency",
        )


    with cols[3]:

        show_metric(
            "FCL Referrals",
            gti_fcl_referrals,
            "integer",
        )


    with cols[4]:

        show_metric(
            "FCL Referral Rate",
            gti_fcl_referral_rate,
            "ratio",
        )


    # -------------------------------------------------------------------------
    # DB PRODUCT CHART
    # -------------------------------------------------------------------------

    st.subheader(
        "Defined Benefit Liability by Product"
    )


    if (

        not products.empty

        and {

            "product_type",
            "actuarial_liability",

        }.issubset(
            products.columns
        )
    ):

        db_products = product_frame(

            products,

            [
                "Gratuity",
                "DB_Pension",
                "DB Pension",
            ],
        )


        chart_df = db_products[

            [
                "product_type",
                "actuarial_liability",
            ]

        ].copy()


        chart_df[
            "actuarial_liability"
        ] = numeric_series(

            chart_df,

            "actuarial_liability",
        )


        chart_df = chart_df.dropna(

            subset=[
                "actuarial_liability",
            ]
        )


    else:

        chart_df = pd.DataFrame()


        if (

            not funded.empty

            and "product_type"
            in funded.columns
        ):

            fallback = funded.copy()


            fallback[
                "actuarial_liability"
            ] = numeric_series(

                fallback,

                "actuarial_liability",
            )


            chart_df = (

                fallback

                .groupby(
                    "product_type",
                    as_index=False,
                )[
                    "actuarial_liability"
                ]

                .sum()
            )


    if not chart_df.empty:


        chart_df[
            "Product"
        ] = chart_df[
            "product_type"
        ].map(
            product_label
        )


        chart_df[
            "Display Value"
        ] = chart_df[
            "actuarial_liability"
        ].map(
            format_inr_compact
        )


        fig = px.bar(

            chart_df,

            x="Product",

            y="actuarial_liability",

            text="Display Value",

            category_orders={

                "Product": [
                    "Gratuity",
                    "DB Pension",
                ]
            },

            labels={

                "actuarial_liability":
                    "Actuarial Liability (INR)"
            },

            title="Gratuity vs DB Pension Liability",
        )


        fig.update_traces(

            textposition="outside",

            hovertemplate=(

                "<b>%{x}</b>"
                "<br>Liability: ₹%{y:,.2f}"
                "<extra></extra>"
            ),
        )


        clean_chart(

            fig,

            height=430,

            y_title="Actuarial Liability (INR)",

            show_legend=False,
        )


        st.plotly_chart(

            fig,

            use_container_width=True,
        )


# =============================================================================
# PAGE 2
# FUNDING & LIABILITIES
# =============================================================================

elif page == "Funding & Liabilities":


    st.header(
        "Defined Benefit Funding & Liabilities"
    )


    # -------------------------------------------------------------------------
    # PORTFOLIO FUNDING KPI CARDS
    # -------------------------------------------------------------------------

    cols = st.columns(
        4
    )


    with cols[0]:

        show_metric(
            "Combined DB Liability",
            combined_db_liability,
            "currency",
        )


    with cols[1]:

        show_metric(
            "DB Plan Assets",
            combined_db_assets,
            "currency",
        )


    with cols[2]:

        show_metric(
            "Funding Ratio",
            combined_db_funding_ratio,
            "ratio",
        )


    with cols[3]:

        show_metric(
            "Funding Deficit",
            combined_db_funding_deficit,
            "currency",
        )


    if funded.empty:


        st.warning(
            "No funded Defined Benefit plans are available "
            "in the dashboard data mart."
        )


    else:


        funded_view = funded.copy()


        if (

            "funding_ratio_pct"
            not in funded_view.columns

            and "funding_ratio"
            in funded_view.columns
        ):

            funded_view[
                "funding_ratio_pct"
            ] = (

                numeric_series(
                    funded_view,
                    "funding_ratio",
                )

                * 100
            )


        # ---------------------------------------------------------------------
        # LIABILITY VS ASSETS
        # ---------------------------------------------------------------------

        st.subheader(
            "Liability vs Plan Assets"
        )


        fig = go.Figure()


        fig.add_bar(

            name="Actuarial Liability",

            x=funded_view[
                "plan_id"
            ],

            y=numeric_series(
                funded_view,
                "actuarial_liability",
            ),

            hovertemplate=(

                "<b>%{x}</b>"
                "<br>Liability: ₹%{y:,.2f}"
                "<extra></extra>"
            ),
        )


        fig.add_bar(

            name="Plan Assets",

            x=funded_view[
                "plan_id"
            ],

            y=numeric_series(
                funded_view,
                "plan_assets",
            ),

            hovertemplate=(

                "<b>%{x}</b>"
                "<br>Assets: ₹%{y:,.2f}"
                "<extra></extra>"
            ),
        )


        fig.update_layout(

            barmode="group",

            xaxis_title="Plan",
        )


        clean_chart(

            fig,

            height=410,

            y_title="INR",
        )


        st.plotly_chart(

            fig,

            use_container_width=True,
        )


        # ---------------------------------------------------------------------
        # FUNDING RATIO BY PLAN
        # ---------------------------------------------------------------------

        if "funding_ratio_pct" in funded_view.columns:


            st.subheader(
                "Funding Ratio by Plan"
            )


            ratio_df = funded_view.copy()


            ratio_df[
                "funding_ratio_pct"
            ] = numeric_series(

                ratio_df,

                "funding_ratio_pct",
            )


            ratio_df[
                "Display Ratio"
            ] = ratio_df[
                "funding_ratio_pct"
            ].map(

                lambda x:

                    format_percent(
                        x,
                        value_is_ratio=False,
                    )
            )


            fig = px.bar(

                ratio_df,

                x="plan_id",

                y="funding_ratio_pct",

                text="Display Ratio",

                labels={

                    "plan_id":
                        "Plan",

                    "funding_ratio_pct":
                        "Funding Ratio (%)",
                },
            )


            fig.update_traces(

                textposition="outside",

                hovertemplate=(

                    "<b>%{x}</b>"
                    "<br>Funding Ratio: %{y:.2f}%"
                    "<extra></extra>"
                ),
            )


            clean_chart(

                fig,

                height=390,

                y_title="Funding Ratio (%)",

                show_legend=False,
            )


            st.plotly_chart(

                fig,

                use_container_width=True,
            )


        # ---------------------------------------------------------------------
        # PROFESSIONAL DB FUNDING TABLE
        # ---------------------------------------------------------------------

        st.subheader(
            "Plan Funding Detail"
        )


        funding_columns = [

            "plan_id",

            "product_type",

            "active_members",

            "actuarial_liability",

            "puc_one_service_year_pv",

            "plan_assets",

            "funding_ratio_pct",

            "funding_deficit",

            "net_funded_position",
        ]


        funding_table = pretty_table(

            funded_view,

            funding_columns,

            money={

                "actuarial_liability",

                "puc_one_service_year_pv",

                "plan_assets",

                "funding_deficit",

                "net_funded_position",
            },

            integers={

                "active_members",
            },

            pct_values={

                "funding_ratio_pct",
            },

            product_columns={

                "product_type",
            },
        )


        st.dataframe(

            funding_table,

            use_container_width=True,

            hide_index=True,
        )


        st.caption(
            "Funding tables intentionally exclude DC, GTI and EDLI "
            "fields because those measures have different financial meanings."
        )


# =============================================================================
# PAGE 3
# DEFINED CONTRIBUTION SUPERANNUATION
# =============================================================================

elif page == "DC Superannuation":


    st.header(
        "Defined Contribution Superannuation"
    )


    # -------------------------------------------------------------------------
    # DC KPI CARDS
    # -------------------------------------------------------------------------

    cols = st.columns(
        4
    )


    with cols[0]:

        show_metric(
            "DC Members",
            dc_members,
            "integer",
        )


    with cols[1]:

        show_metric(
            "Annual Employer Contributions",
            dc_employer_contribution,
            "currency",
        )


    with cols[2]:

        show_metric(
            "Annual Employee Contributions",
            dc_employee_contribution,
            "currency",
        )


    with cols[3]:

        show_metric(
            "Future-Contribution Corpus",
            dc_future_corpus,
            "currency",
        )


    if dc_plans.empty:


        st.warning(
            "No Defined Contribution Superannuation plans are available."
        )


    else:


        # ---------------------------------------------------------------------
        # FUTURE CORPUS CHART
        # ---------------------------------------------------------------------

        st.subheader(
            "Projected Future-Contribution Corpus by DC Plan"
        )


        dc_chart = dc_plans.copy()


        dc_chart[
            "projected_future_contribution_corpus"
        ] = numeric_series(

            dc_chart,

            "projected_future_contribution_corpus",
        )


        dc_chart[
            "Display Corpus"
        ] = dc_chart[
            "projected_future_contribution_corpus"
        ].map(
            format_inr_compact
        )


        fig = px.bar(

            dc_chart,

            x="plan_id",

            y="projected_future_contribution_corpus",

            text="Display Corpus",

            labels={

                "plan_id":
                    "DC Plan",

                "projected_future_contribution_corpus":
                    "Future-Contribution Corpus (INR)",
            },
        )


        fig.update_traces(

            textposition="outside",

            hovertemplate=(

                "<b>%{x}</b>"
                "<br>Future Corpus: ₹%{y:,.2f}"
                "<extra></extra>"
            ),
        )


        clean_chart(

            fig,

            height=420,

            y_title="Future-Contribution Corpus (INR)",

            show_legend=False,
        )


        st.plotly_chart(

            fig,

            use_container_width=True,
        )


        # ---------------------------------------------------------------------
        # PROFESSIONAL DC TABLE
        # ---------------------------------------------------------------------

        st.subheader(
            "DC Plan Detail"
        )


        dc_columns = [

            "plan_id",

            "active_members",

            "annual_employer_contribution",

            "annual_employee_contribution",

            "projected_future_contribution_corpus",
        ]


        dc_table = pretty_table(

            dc_plans,

            dc_columns,

            money={

                "annual_employer_contribution",

                "annual_employee_contribution",

                "projected_future_contribution_corpus",
            },

            integers={

                "active_members",
            },
        )


        st.dataframe(

            dc_table,

            use_container_width=True,

            hide_index=True,
        )


    st.info(
        "Projected DC values represent the future-contribution corpus. "
        "Opening individual member corpus was not available and is not "
        "fabricated or replaced with pooled plan assets."
    )


# =============================================================================
# PAGE 4
# GROUP RISK — GTI & EDLI
# =============================================================================

elif page == "Group Risk — GTI & EDLI":


    st.header(
        "Group Risk — GTI & EDLI"
    )


    # =========================================================================
    # GTI
    # =========================================================================

    st.subheader(
        "Group Term Insurance"
    )


    cols = st.columns(
        5
    )


    with cols[0]:

        show_metric(
            "Total Sum Assured",
            gti_total_sum_assured,
            "currency",
        )


    with cols[1]:

        show_metric(
            "Fresh Expected Claims",
            gti_expected_claims,
            "currency",
        )


    with cols[2]:

        show_metric(
            "Fresh Gross Premium",
            gti_fresh_gross_premium,
            "currency",
        )


    with cols[3]:

        show_metric(
            "FCL Referrals",
            gti_fcl_referrals,
            "integer",
        )


    with cols[4]:

        show_metric(
            "FCL Referral Rate",
            gti_fcl_referral_rate,
            "ratio",
        )


    if not gti_plans.empty:


        # ---------------------------------------------------------------------
        # TWO-COLUMN GTI CHART AREA
        # ---------------------------------------------------------------------

        left, right = st.columns(
            2
        )


        # ---------------------------------------------------------------------
        # SUM ASSURED
        # ---------------------------------------------------------------------

        with left:


            gti_sa = gti_plans.copy()


            gti_sa[
                "total_sum_assured"
            ] = numeric_series(

                gti_sa,

                "total_sum_assured",
            )


            gti_sa[
                "Display SA"
            ] = gti_sa[
                "total_sum_assured"
            ].map(
                format_inr_compact
            )


            fig = px.bar(

                gti_sa,

                x="plan_id",

                y="total_sum_assured",

                text="Display SA",

                labels={

                    "plan_id":
                        "GTI Plan",

                    "total_sum_assured":
                        "Sum Assured (INR)",
                },

                title="Sum Assured by GTI Plan",
            )


            fig.update_traces(

                textposition="outside",

                hovertemplate=(

                    "<b>%{x}</b>"
                    "<br>Sum Assured: ₹%{y:,.2f}"
                    "<extra></extra>"
                ),
            )


            clean_chart(

                fig,

                height=380,

                y_title="Sum Assured (INR)",

                show_legend=False,
            )


            st.plotly_chart(

                fig,

                use_container_width=True,
            )


        # ---------------------------------------------------------------------
        # EXPECTED CLAIMS
        # ---------------------------------------------------------------------

        with right:


            gti_claims = gti_plans.copy()


            gti_claims[
                "fresh_expected_claim_cost"
            ] = numeric_series(

                gti_claims,

                "fresh_expected_claim_cost",
            )


            gti_claims[
                "Display Claims"
            ] = gti_claims[
                "fresh_expected_claim_cost"
            ].map(
                format_inr_compact
            )


            fig = px.bar(

                gti_claims,

                x="plan_id",

                y="fresh_expected_claim_cost",

                text="Display Claims",

                labels={

                    "plan_id":
                        "GTI Plan",

                    "fresh_expected_claim_cost":
                        "Fresh Expected Claims (INR)",
                },

                title="Fresh Expected Claims by GTI Plan",
            )


            fig.update_traces(

                textposition="outside",

                hovertemplate=(

                    "<b>%{x}</b>"
                    "<br>Expected Claims: ₹%{y:,.2f}"
                    "<extra></extra>"
                ),
            )


            clean_chart(

                fig,

                height=380,

                y_title="Expected Claims (INR)",

                show_legend=False,
            )


            st.plotly_chart(

                fig,

                use_container_width=True,
            )


        # ---------------------------------------------------------------------
        # FCL REFERRALS
        # ---------------------------------------------------------------------

        referrals = gti_plans.copy()


        referrals[
            "underwriting_referrals"
        ] = numeric_series(

            referrals,

            "underwriting_referrals",
        )


        referrals[
            "Display Referrals"
        ] = referrals[
            "underwriting_referrals"
        ].map(
            format_integer
        )


        fig = px.bar(

            referrals,

            x="plan_id",

            y="underwriting_referrals",

            text="Display Referrals",

            labels={

                "plan_id":
                    "GTI Plan",

                "underwriting_referrals":
                    "Employees",
            },

            title="Free-Cover-Limit Underwriting Referrals",
        )


        fig.update_traces(

            textposition="outside",

            hovertemplate=(

                "<b>%{x}</b>"
                "<br>Referrals: %{y:,.0f}"
                "<extra></extra>"
            ),
        )


        clean_chart(

            fig,

            height=360,

            y_title="Employees",

            show_legend=False,
        )


        st.plotly_chart(

            fig,

            use_container_width=True,
        )


        # ---------------------------------------------------------------------
        # GTI PLAN SUMMARY
        # ---------------------------------------------------------------------

        st.subheader(
            "GTI Plan Summary"
        )


        gti_summary = gti_plans.copy()


        if "gti_fcl_referral_rate" not in gti_summary.columns:


            members = numeric_series(

                gti_summary,

                "active_members",
            ).replace(
                0,
                np.nan,
            )


            refs = numeric_series(

                gti_summary,

                "underwriting_referrals",
            )


            gti_summary[
                "gti_fcl_referral_rate"
            ] = (

                refs
                /
                members
            )


        gti_columns = [

            "plan_id",

            "active_members",

            "total_sum_assured",

            "fresh_expected_claim_cost",

            "fresh_model_gross_premium",

            "underwriting_referrals",

            "gti_fcl_referral_rate",
        ]


        gti_table = pretty_table(

            gti_summary,

            gti_columns,

            money={

                "total_sum_assured",

                "fresh_expected_claim_cost",

                "fresh_model_gross_premium",
            },

            integers={

                "active_members",

                "underwriting_referrals",
            },

            pct_ratio={

                "gti_fcl_referral_rate",
            },
        )


        st.dataframe(

            gti_table,

            use_container_width=True,

            hide_index=True,
        )


    st.success(
        "Final GTI dashboard premium uses the fresh expected-claims pricing basis. "
        "Historical A/E credibility-adjusted pricing is intentionally excluded "
        "from the final KPI."
    )


    # =========================================================================
    # EDLI
    # =========================================================================

    st.divider()


    st.subheader(
        "Employees' Deposit Linked Insurance"
    )


    edli_lower = safe_sum(

        edli_plans,

        "edli_part_b_lower_if_qualifying",
    )


    edli_upper = safe_sum(

        edli_plans,

        "edli_part_b_upper_if_qualifying",
    )


    cols = st.columns(
        3
    )


    with cols[0]:

        show_metric(
            "EDLI Members",
            edli_members,
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


    st.warning(
        "EDLI is an effective-date-sensitive statutory benefit. "
        "The displayed Part B range is analytical and must not be treated "
        "as the final official settlement amount. "
        "Official calculator verification remains required."
    )


# =============================================================================
# PAGE 5
# WORKFORCE CONCENTRATION
# =============================================================================

elif page == "Workforce Concentration":


    st.header(
        "Workforce Benefit & Risk Concentration"
    )


    if (

        segments.empty

        or "segment_type"
        not in segments.columns

        or "segment_value"
        not in segments.columns
    ):


        st.warning(
            "No segment concentration data are available."
        )


    else:


        segment_types = sorted(

            segments[
                "segment_type"
            ]

            .dropna()

            .astype(
                str
            )

            .unique()

            .tolist()
        )


        selected_segment = st.selectbox(

            "Segment By",

            segment_types,

            format_func=(

                lambda x:

                    x
                    .replace(
                        "_",
                        " ",
                    )
                    .title()
            ),
        )


        # ---------------------------------------------------------------------
        # AVAILABLE RISK MEASURES
        # ---------------------------------------------------------------------

        candidate_risks = [

            (
                "Defined Benefit Liability",
                "combined_db_liability",
            ),

            (
                "DC Future-Contribution Corpus",
                "projected_future_contribution_corpus",
            ),

            (
                "GTI Sum Assured",
                "gti_sum_assured",
            ),

            (
                "GTI Fresh Expected Claims",
                "gti_fresh_expected_claim_cost",
            ),

            (
                "GTI Fresh Gross Premium",
                "gti_fresh_model_gross_premium",
            ),

            (
                "EDLI Part B Lower",
                "edli_part_b_lower_if_qualifying",
            ),

            (
                "EDLI Part B Upper",
                "edli_part_b_upper_if_qualifying",
            ),
        ]


        risk_options = {}


        for (
            label,
            column,
        ) in candidate_risks:


            if (

                column in segments.columns

                and numeric_series(
                    segments,
                    column,
                )
                .notna()
                .any()
            ):


                risk_options[
                    label
                ] = column


        if not risk_options:


            st.warning(
                "No supported risk measures are available in the segment data."
            )


        else:


            selected_label = st.selectbox(

                "Risk Measure",

                list(
                    risk_options.keys()
                ),
            )


            selected_metric = risk_options[
                selected_label
            ]


            segment_view = segments.loc[

                segments[
                    "segment_type"
                ]

                .astype(
                    str
                )

                .eq(
                    selected_segment
                )

            ].copy()


            segment_view[
                selected_metric
            ] = numeric_series(

                segment_view,

                selected_metric,
            )


            segment_view = segment_view.sort_values(

                selected_metric,

                ascending=False,
            )


            total_selected = (

                segment_view[
                    selected_metric
                ]

                .fillna(
                    0
                )

                .sum()
            )


            if total_selected > 0:


                segment_view[
                    "portfolio_share_pct"
                ] = (

                    segment_view[
                        selected_metric
                    ]

                    .fillna(
                        0
                    )

                    /

                    total_selected

                    * 100
                )


            else:


                segment_view[
                    "portfolio_share_pct"
                ] = 0.0


            segment_display_name = (

                selected_segment

                .replace(
                    "_",
                    " ",
                )

                .title()
            )


            # -----------------------------------------------------------------
            # SEGMENT CHART
            # -----------------------------------------------------------------

            st.subheader(

                f"{selected_label} "
                f"by {segment_display_name}"
            )


            chart_df = segment_view.copy()


            chart_df[
                "Display Value"
            ] = chart_df[
                selected_metric
            ].map(
                format_inr_compact
            )


            fig = px.bar(

                chart_df,

                x="segment_value",

                y=selected_metric,

                text="Display Value",

                labels={

                    "segment_value":
                        segment_display_name,

                    selected_metric:
                        f"{selected_label} (INR)",
                },
            )


            fig.update_traces(

                textposition="outside",

                hovertemplate=(

                    "<b>%{x}</b>"
                    "<br>Value: ₹%{y:,.2f}"
                    "<extra></extra>"
                ),
            )


            clean_chart(

                fig,

                height=430,

                y_title=f"{selected_label} (INR)",

                show_legend=False,
            )


            st.plotly_chart(

                fig,

                use_container_width=True,
            )


            # -----------------------------------------------------------------
            # DYNAMIC BUSINESS TABLE
            # -----------------------------------------------------------------

            common_columns = [

                "segment_value",

                "employee_count",
            ]


            custom_labels = {

                "segment_value":
                    segment_display_name,
            }


            if selected_metric == "combined_db_liability":


                table_columns = (

                    common_columns

                    + [

                        "gratuity_dbo",

                        "db_pension_liability",

                        "combined_db_liability",

                        "portfolio_share_pct",
                    ]
                )


                money_columns = {

                    "gratuity_dbo",

                    "db_pension_liability",

                    "combined_db_liability",
                }


            elif selected_metric == "projected_future_contribution_corpus":


                table_columns = (

                    common_columns

                    + [

                        "current_annual_employer_contribution",

                        "current_annual_employee_contribution",

                        "projected_future_contribution_corpus",

                        "portfolio_share_pct",
                    ]
                )


                money_columns = {

                    "current_annual_employer_contribution",

                    "current_annual_employee_contribution",

                    "projected_future_contribution_corpus",
                }


            elif selected_metric in {

                "gti_sum_assured",

                "gti_fresh_expected_claim_cost",

                "gti_fresh_model_gross_premium",

            }:


                table_columns = (

                    common_columns

                    + [

                        "gti_sum_assured",

                        "gti_fresh_expected_claim_cost",

                        "gti_fresh_model_gross_premium",

                        "gti_cover_above_free_cover_limit",

                        "portfolio_share_pct",
                    ]
                )


                money_columns = {

                    "gti_sum_assured",

                    "gti_fresh_expected_claim_cost",

                    "gti_fresh_model_gross_premium",

                    "gti_cover_above_free_cover_limit",
                }


            else:


                table_columns = (

                    common_columns

                    + [

                        "edli_part_b_lower_if_qualifying",

                        "edli_part_b_upper_if_qualifying",

                        "portfolio_share_pct",
                    ]
                )


                money_columns = {

                    "edli_part_b_lower_if_qualifying",

                    "edli_part_b_upper_if_qualifying",
                }


            segment_table = pretty_table(

                segment_view,

                table_columns,

                labels=custom_labels,

                money=money_columns,

                integers={

                    "employee_count",
                },

                pct_values={

                    "portfolio_share_pct",
                },
            )


            st.dataframe(

                segment_table,

                use_container_width=True,

                hide_index=True,
            )


# =============================================================================
# PAGE 6
# EMPLOYEE DRILL-DOWN
# =============================================================================

elif page == "Employee Drill-Down":


    st.header(
        "Employee Benefit Drill-Down"
    )


    if employees.empty:


        st.warning(
            "Employee drill-down data are unavailable."
        )


    else:


        filtered_employees = employees.copy()


        # ---------------------------------------------------------------------
        # EMPLOYEE ID SEARCH + STATUS
        # ---------------------------------------------------------------------

        search_col, status_col = st.columns(

            [
                2,
                1,
            ]
        )


        with search_col:


            employee_search = st.text_input(

                "Employee ID Search",

                placeholder=(
                    "Enter full or partial employee ID"
                ),
            )


        with status_col:


            if "employment_status" in employees.columns:


                status_values = sorted(

                    employees[
                        "employment_status"
                    ]

                    .dropna()

                    .astype(
                        str
                    )

                    .unique()

                    .tolist()
                )


                selected_status = st.multiselect(

                    "Employment Status",

                    status_values,
                )


            else:


                selected_status = []


        if (

            employee_search

            and "employee_id"
            in filtered_employees.columns
        ):


            filtered_employees = filtered_employees.loc[

                filtered_employees[
                    "employee_id"
                ]

                .astype(
                    str
                )

                .str.contains(

                    employee_search.strip(),

                    case=False,

                    na=False,
                )

            ]


        if (

            selected_status

            and "employment_status"
            in filtered_employees.columns
        ):


            filtered_employees = filtered_employees.loc[

                filtered_employees[
                    "employment_status"
                ]

                .astype(
                    str
                )

                .isin(
                    selected_status
                )

            ]


        # ---------------------------------------------------------------------
        # DYNAMIC FILTER CONTROLS
        # ---------------------------------------------------------------------

        available_filters = []


        if "department" in employees.columns:

            available_filters.append(

                (
                    "department",
                    "Department",
                )
            )


        if "location" in employees.columns:

            available_filters.append(

                (
                    "location",
                    "Location",
                )
            )


        if "grade" in employees.columns:

            available_filters.append(

                (
                    "grade",
                    "Grade",
                )
            )


        selected_filter_values = {}


        if available_filters:


            filter_columns = st.columns(

                len(
                    available_filters
                )
            )


            for (
                ui_column,
                filter_definition,
            ) in zip(

                filter_columns,
                available_filters,
            ):


                field_name = filter_definition[
                    0
                ]


                field_label = filter_definition[
                    1
                ]


                values = sorted(

                    employees[
                        field_name
                    ]

                    .dropna()

                    .astype(
                        str
                    )

                    .unique()

                    .tolist()
                )


                with ui_column:


                    selected_filter_values[
                        field_name
                    ] = st.multiselect(

                        field_label,

                        values,
                    )


        for (
            field_name,
            selected_values,
        ) in selected_filter_values.items():


            if selected_values:


                filtered_employees = filtered_employees.loc[

                    filtered_employees[
                        field_name
                    ]

                    .astype(
                        str
                    )

                    .isin(
                        selected_values
                    )

                ]


        # ---------------------------------------------------------------------
        # SELECTION SUMMARY
        # ---------------------------------------------------------------------

        cols = st.columns(
            4
        )


        with cols[0]:

            show_metric(
                "Employees in Selection",
                len(
                    filtered_employees
                ),
                "integer",
            )


        with cols[1]:

            show_metric(
                "Combined DB Liability",
                safe_sum(
                    filtered_employees,
                    "combined_db_liability",
                ),
                "currency",
            )


        with cols[2]:

            show_metric(
                "DC Future Corpus",
                safe_sum(
                    filtered_employees,
                    "projected_future_contribution_corpus",
                ),
                "currency",
            )


        with cols[3]:

            show_metric(
                "GTI Sum Assured",
                safe_sum(
                    filtered_employees,
                    "gti_sum_assured",
                ),
                "currency",
            )


        # ---------------------------------------------------------------------
        # CORE VS FULL TABLE
        # ---------------------------------------------------------------------

        table_view = st.radio(

            "Table View",

            [

                "Core Overview",

                "Full Benefit Detail",
            ],

            horizontal=True,
        )


        # ---------------------------------------------------------------------
        # CORE OVERVIEW
        # ---------------------------------------------------------------------

        if table_view == "Core Overview":


            core_columns = [

                "employee_id",

                "employment_status",

                "department",

                "location",

                "grade",

                "attained_age_years",

                "completed_service_years",

                "combined_db_liability",

                "current_annual_employer_contribution",

                "current_annual_employee_contribution",

                "projected_future_contribution_corpus",

                "gti_sum_assured",
            ]


            employee_table = pretty_table(

                filtered_employees,

                core_columns,

                money={

                    "combined_db_liability",

                    "current_annual_employer_contribution",

                    "current_annual_employee_contribution",

                    "projected_future_contribution_corpus",

                    "gti_sum_assured",
                },

                decimals={

                    "attained_age_years":
                        1,

                    "completed_service_years":
                        1,
                },
            )


        # ---------------------------------------------------------------------
        # FULL BENEFIT DETAIL
        # ---------------------------------------------------------------------

        else:


            referral_flag = first_existing_column(

                filtered_employees,

                [

                    "gti_underwriting_referral_flag",

                    "underwriting_referral_flag",

                    "gti_fcl_referral_flag",
                ],
            )


            full_columns = [

                "employee_id",

                "employment_status",

                "department",

                "location",

                "grade",

                "attained_age_years",

                "completed_service_years",

                "gratuity_plan_id",

                "db_pension_plan_id",

                "dc_superannuation_plan_id",

                "gti_pricing_plan_id",

                "edli_plan_id",

                "gratuity_dbo",

                "db_pension_liability",

                "combined_db_liability",

                "current_annual_employer_contribution",

                "current_annual_employee_contribution",

                "projected_future_contribution_corpus",

                "gti_sum_assured",

                "gti_fresh_expected_claim_cost",

                "gti_fresh_model_gross_premium",

                "gti_cover_above_free_cover_limit",

                "edli_part_b_lower_if_qualifying",

                "edli_part_b_upper_if_qualifying",
            ]


            if referral_flag:

                full_columns.append(
                    referral_flag
                )


            extra_labels = {}


            if referral_flag:

                extra_labels[
                    referral_flag
                ] = "FCL Referral"


            employee_table = pretty_table(

                filtered_employees,

                full_columns,

                labels=extra_labels,

                money={

                    "gratuity_dbo",

                    "db_pension_liability",

                    "combined_db_liability",

                    "current_annual_employer_contribution",

                    "current_annual_employee_contribution",

                    "projected_future_contribution_corpus",

                    "gti_sum_assured",

                    "gti_fresh_expected_claim_cost",

                    "gti_fresh_model_gross_premium",

                    "gti_cover_above_free_cover_limit",

                    "edli_part_b_lower_if_qualifying",

                    "edli_part_b_upper_if_qualifying",
                },

                decimals={

                    "attained_age_years":
                        1,

                    "completed_service_years":
                        1,
                },

                booleans=(

                    {
                        referral_flag
                    }

                    if referral_flag

                    else None
                ),
            )


        # ---------------------------------------------------------------------
        # EMPLOYEE TABLE
        # ---------------------------------------------------------------------

        st.dataframe(

            employee_table,

            use_container_width=True,

            hide_index=True,

            height=540,
        )


        # ---------------------------------------------------------------------
        # DOWNLOAD RAW FILTERED DETAIL
        # ---------------------------------------------------------------------

        st.download_button(

            label="Download Filtered Employee Data",

            data=(

                filtered_employees

                .to_csv(
                    index=False
                )

                .encode(
                    "utf-8"
                )
            ),

            file_name=(
                "employee_benefit_drilldown.csv"
            ),

            mime="text/csv",
        )


# =============================================================================
# PAGE 7
# GOVERNANCE & VALIDATION
# =============================================================================

elif page == "Governance & Validation":


    st.header(
        "Model Governance & Validation"
    )


    # -------------------------------------------------------------------------
    # VALIDATION COUNTS
    # -------------------------------------------------------------------------

    validation_passes = 0

    validation_failures = 0


    if (

        not validation.empty

        and "status"
        in validation.columns
    ):


        status_upper = (

            validation[
                "status"
            ]

            .astype(
                str
            )

            .str.upper()
        )


        validation_passes = int(

            status_upper

            .eq(
                "PASS"
            )

            .sum()
        )


        validation_failures = int(

            status_upper

            .eq(
                "FAIL"
            )

            .sum()
        )


    governance_categories = len(
        governance
    )


    review_categories = 0


    if (

        not governance.empty

        and "dashboard_status"
        in governance.columns
    ):


        review_categories = int(

            governance[
                "dashboard_status"
            ]

            .astype(
                str
            )

            .str.upper()

            .eq(
                "REVIEW"
            )

            .sum()
        )


    # -------------------------------------------------------------------------
    # SUMMARY KPI CARDS
    # -------------------------------------------------------------------------

    cols = st.columns(
        4
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


    with cols[2]:

        show_metric(
            "Governance Categories",
            governance_categories,
            "integer",
        )


    with cols[3]:

        show_metric(
            "Categories Requiring Review",
            review_categories,
            "integer",
        )


    if validation_failures == 0:


        st.success(
            "All Pipeline 10 portfolio validation checks passed."
        )


    else:


        st.error(
            "One or more portfolio validation checks failed."
        )


    # -------------------------------------------------------------------------
    # CLEAN VALIDATION TABLE
    # -------------------------------------------------------------------------

    st.subheader(
        "Portfolio Validation"
    )


    validation_columns = [

        "check",

        "exceptions",

        "status",

        "note",
    ]


    validation_table = pretty_table(

        validation,

        validation_columns,

        integers={

            "exceptions",
        },
    )


    st.dataframe(

        validation_table,

        use_container_width=True,

        hide_index=True,
    )


    # -------------------------------------------------------------------------
    # CLEAN GOVERNANCE TABLE
    # -------------------------------------------------------------------------

    st.subheader(
        "Governance Register"
    )


    governance_view = governance.copy()


    if "review_rows" in governance_view.columns:


        governance_view[
            "review_rows"
        ] = numeric_series(

            governance_view,

            "review_rows",
        ).fillna(
            0
        )


    if "dashboard_status" in governance_view.columns:


        governance_view[
            "_status_order"
        ] = (

            governance_view[
                "dashboard_status"
            ]

            .astype(
                str
            )

            .str.upper()

            .map(

                {

                    "REVIEW":
                        0,

                    "OK":
                        1,
                }
            )

            .fillna(
                2
            )
        )


    else:


        governance_view[
            "_status_order"
        ] = 2


    governance_view = governance_view.sort_values(

        [

            "_status_order",

            "review_rows",
        ],

        ascending=[

            True,

            False,
        ],
    )


    governance_columns = [

        "governance_item",

        "review_rows",

        "treatment",

        "source_pipeline",

        "dashboard_status",
    ]


    governance_table = pretty_table(

        governance_view,

        governance_columns,

        integers={

            "review_rows",
        },
    )


    st.dataframe(

        governance_table,

        use_container_width=True,

        hide_index=True,
    )


    st.info(
        "Governance reviews are documented model limitations, fallbacks "
        "or business-review items. They are not automatically mathematical "
        "validation failures."
    )


# =============================================================================
# FOOTER
# =============================================================================

st.divider()


st.caption(
    f"Hessian-AI · Quantitative Actuarial Employee Benefits Dashboard · "
    f"Valuation Date: {VALUATION_DATE} · "
    f"Dashboard Data Mart: {DASHBOARD_VERSION}"
)