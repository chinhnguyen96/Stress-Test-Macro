# =============================================================================
# MACROECONOMIC STRESS TESTING DASHBOARD
# =============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import requests
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, date
from io import BytesIO
from pathlib import Path

from groq import Groq


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Macro Stress Testing Dashboard",
    layout="wide",
    initial_sidebar_state="auto"
)


# =============================================================================
# PATH CONFIG
# =============================================================================

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "vietbank_logo.png"


# =============================================================================
# GLOBAL CSS - DARK THEME
# =============================================================================

st.markdown(
    """
    <style>

    /* MAIN APP */
    .stApp {
        background-color: #0E0E0E;
        color: #FFFFFF;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1500px;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #2A2A2A;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF;
    }
    

    /* MAIN TITLE */
    .main-title {
        font-size: 36px;
        font-weight: 750;
        color: #FFFFFF;
        line-height: 1.2;
        margin-top: 5px;
        margin-bottom: 7px;
    }

    /* SUBTITLE */
    .subtitle {
        font-size: 15px;
        color: #B3B3B3;
        margin-bottom: 5px;
    }

    /* SECTION TITLE */
    .section-title {
        font-size: 21px;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    /* GENERAL INFO CARD */
    .info-card {
        background-color: #181818;
        padding: 22px 24px;
        border-radius: 12px;
        border: 1px solid #2A2A2A;
        margin-bottom: 15px;
        color: #E5E5E5;
        font-size: 15px;
        line-height: 1.7;
    }

    /* FEATURE CARD */
    .feature-card {
        background-color: #181818;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #2A2A2A;
        min-height: 190px;
    }

    .feature-title {
        font-size: 17px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 10px;
    }

    .feature-text {
        font-size: 14px;
        color: #BFC3C9;
        line-height: 1.65;
    }

    /* DEVELOPER CARD */
    .developer-card {
        background-color: #181818;
        padding: 22px 25px;
        border-radius: 10px;
        border: 1px solid #2A2A2A;
        margin-bottom: 15px;
    }

    .developer-name {
        font-size: 24px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }

    .developer-position {
        font-size: 13px;
        color: #B3B3B3;
    }

    /* CONTACT */
    .contact-card {
        background-color: #181818;
        padding: 20px 24px;
        border-radius: 12px;
        border: 1px solid #2A2A2A;
        color: #E5E5E5;
        font-size: 14px;
        line-height: 2;
    }

    .contact-label {
        font-weight: 700;
        color: #FFFFFF;
    }

    /* FOOTER */
    .footer-text {
        text-align: center;
        color: #777777;
        font-size: 12px;
        padding-top: 10px;
    }

    /* STREAMLIT TITLES */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    /* NORMAL STREAMLIT TEXT */
    p, span, label {
        color: #E5E5E5;
    }

    /* RADIO BUTTON TEXT */
    div[data-testid="stRadio"] label {
        color: #FFFFFF !important;
    }

    /* DIVIDER */
    hr {
        border-color: #2A2A2A !important;
    }

    /* ALERT / INFO BOX */
    div[data-testid="stAlert"] {
        background-color: #181818;
        color: #FFFFFF;
        border: 1px solid #2A2A2A;
    }

    /* HIDE STREAMLIT DEFAULT ELEMENTS */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def show_logo(width=None):
    """
    Display Vietbank logo if the logo file exists.
    """

    if LOGO_PATH.exists():

        if width is not None:
            st.image(str(LOGO_PATH), width=width)
        else:
            st.image(str(LOGO_PATH), use_container_width=True)

    else:
        st.warning(
            "Logo not found. Please add "
            "`assets/vietbank_logo.png` to the project folder."
        )


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:

    # Logo
    if LOGO_PATH.exists():
        st.image(
            str(LOGO_PATH),
            use_container_width=True
        )
    else:
        st.markdown("### VIETBANK")

    st.markdown("---")

    # Navigation
    menu = st.radio(
        "Navigation",
        [
            "Overview",
            "Macro Data",
            "Data Download",
            "Macro Analysis",
            "Stress Scenario",
            "Stress Test",
            "AI Analyst"
        ],
        index=0
    )

    st.markdown("---")

    st.caption("Macroeconomic Stress Testing Dashboard")
    st.caption("Credit Risk Management")


# =============================================================================
# TAB 0 - OVERVIEW
# =============================================================================

def tab0():

    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------

    col_logo, col_title = st.columns(
        [1.1, 5],
        vertical_alignment="center"
    )

    with col_logo:

        if LOGO_PATH.exists():
            st.image(
                str(LOGO_PATH),
                use_container_width=True
            )
        else:
            st.markdown(
                """
                ## VIETBANK
                """
            )


    with col_title:

        st.markdown(
            """
            <div class="main-title">
                Dashboard Phân tích Vĩ mô & Kiểm tra Sức chịu đựng
            </div>
    
            <div class="subtitle">
                Giám sát kinh tế vĩ mô • Phân tích kịch bản • Stress Test • Phân tích hỗ trợ bởi AI
            </div>
            """,
            unsafe_allow_html=True
        )


    st.divider()


    # =========================================================================
    # ABOUT DASHBOARD
    # =========================================================================
    
    st.markdown(
        """
        <div class="section-title">
            Giới thiệu Dashboard
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="info-card">
    
        <b>Dashboard Phân tích Vĩ mô & Kiểm tra Sức chịu đựng</b>
        được xây dựng nhằm hỗ trợ theo dõi, phân tích và đánh giá
        diễn biến kinh tế vĩ mô có liên quan đến hoạt động quản lý rủi ro tín dụng.
    
        <br><br>
    
        Dashboard tích hợp dữ liệu kinh tế vĩ mô, dữ liệu thị trường tài chính,
        phân tích kịch bản, mô hình Stress Test và công nghệ AI trên một
        nền tảng phân tích tập trung.
    
        <br><br>
    
        Hệ thống hỗ trợ nhận diện các yếu tố rủi ro vĩ mô và đánh giá
        tác động tiềm tàng của các kịch bản bất lợi đến danh mục tín dụng.
    
        </div>
        """,
        unsafe_allow_html=True
    )


    # =========================================================================
    # PURPOSE
    # =========================================================================

    
    
    st.markdown(
        '<div class="section-title">Mục đích Dashboard</div>',
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📊 Giám sát kinh tế vĩ mô")
    
            st.write(
                """
                Theo dõi các chỉ tiêu kinh tế vĩ mô trọng yếu như
                tăng trưởng GDP, lạm phát, lãi suất, tỷ giá,
                tăng trưởng tín dụng và các biến động của thị trường tài chính.
                """
            )
    
    with col2:
        with st.container(border=True):
            st.markdown("### ⚠️ Kiểm tra sức chịu đựng")
    
            st.write(
                """
                Xây dựng các kịch bản cơ sở, bất lợi và bất lợi nghiêm trọng
                nhằm đánh giá tác động của biến động kinh tế vĩ mô
                đến rủi ro tín dụng và danh mục tín dụng.
                """
            )
    
    with col3:
        with st.container(border=True):
            st.markdown("### 🤖 Phân tích hỗ trợ bởi AI")
    
            st.write(
                """
                Ứng dụng AI để hỗ trợ nhận diện rủi ro vĩ mô,
                phân tích xu hướng, xây dựng kịch bản Stress Test
                và diễn giải kết quả phân tích.
                """
            )


    # =========================================================================
    # CORE FUNCTIONS
    # =========================================================================

    
    st.markdown(
        '<div class="section-title">Chức năng chính</div>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="info-card">
    
        <b>01. Dữ liệu vĩ mô</b><br>
        Thu thập, tổng hợp và trực quan hóa các chỉ tiêu kinh tế vĩ mô
        và dữ liệu thị trường tài chính.
    
        <br><br>
    
        <b>02. Tải dữ liệu</b><br>
        Cho phép lựa chọn các chỉ tiêu, khoảng thời gian và tần suất dữ liệu
        để tải xuống dưới định dạng CSV hoặc Excel.
    
        <br><br>
    
        <b>03. Phân tích vĩ mô</b><br>
        Phân tích xu hướng lịch sử, mức độ biến động và mối quan hệ
        giữa các biến kinh tế vĩ mô.
    
        <br><br>
    
        <b>04. Kịch bản Stress Test</b><br>
        Xây dựng kịch bản cơ sở, bất lợi, bất lợi nghiêm trọng
        và các kịch bản tùy chỉnh.
    
        <br><br>
    
        <b>05. Stress Test</b><br>
        Đánh giá tác động của các cú sốc kinh tế vĩ mô
        đến các chỉ tiêu rủi ro tín dụng.
    
        <br><br>
    
        <b>06. Trợ lý AI</b><br>
        Hỗ trợ phân tích diễn biến kinh tế vĩ mô, nhận diện rủi ro,
        xây dựng kịch bản và diễn giải kết quả Stress Test.
    
        </div>
        """,
        unsafe_allow_html=True
    )


    # =========================================================================
    # DEVELOPER
    # =========================================================================

    
    st.markdown("## 👤 Người xây dựng")
    
    with st.container(border=True):
    
        col1, col2 = st.columns([1, 4])
    
        with col1:
            st.markdown("**Họ và tên**")
            st.markdown("**Chức danh**")
            st.markdown("**Đơn vị**")
    
        with col2:
            st.write("Nguyễn Thị Chinh")
            st.write("Chuyên viên cao cấp")
            st.write("Phòng Quản lý rủi ro tín dụng")


    # =========================================================================
    # CONTACT
    # =========================================================================
    
    st.markdown("## 📩 Thông tin liên hệ")
    
    with st.container(border=True):
    
        col1, col2 = st.columns([1, 3])
    
        with col1:
            st.markdown("**Đơn vị**")
            st.markdown("**Ngân hàng**")
            st.markdown("**Người xây dựng**")
            st.markdown("**Email**")
    
        with col2:
            st.write("Phòng Quản lý rủi ro tín dụng")
            st.write("Vietbank")
            st.write("Chinh, Nguyen Thi")
            st.write("nguyenthichinh@vietbank.com.vn")





    # =========================================================================
    # DISCLAIMER
    # =========================================================================

    st.markdown("## ⚠️ Lưu ý sử dụng")

    with st.container(border=True):

        st.write(
            """
            Dashboard được xây dựng nhằm hỗ trợ hoạt động phân tích,
            giám sát các yếu tố kinh tế vĩ mô và thực hiện Stress Test
            phục vụ công tác quản lý rủi ro.

            Các kết quả phân tích, mô hình và nội dung do AI hỗ trợ
            chỉ mang tính chất tham khảo và hỗ trợ quá trình đánh giá,
            không thay thế cho các quyết định chuyên môn.
            """
        )


    # =========================================================================
    # FOOTER
    # =========================================================================

    
    st.divider()
    
    current_year = datetime.now().year
    
    st.caption(
        f"© {current_year} Vietbank • Dashboard Giám sát Vĩ mô & Stress Test "
        "• Phục vụ mục đích phân tích và quản lý rủi ro nội bộ."
    )


# =============================================================================
# SHARED MACRO DATA ENGINE
# TAB 1 / TAB 2 / TAB 3
# =============================================================================


# =============================================================================
# COUNTRY
# =============================================================================

COUNTRIES = {
    "Việt Nam": "VNM",
    "Hoa Kỳ": "USA",
    "Trung Quốc": "CHN",
    "Nhật Bản": "JPN",
    "Hàn Quốc": "KOR",
    "Singapore": "SGP",
    "Thái Lan": "THA",
    "Indonesia": "IDN",
    "Malaysia": "MYS",
    "Philippines": "PHL"
}


# =============================================================================
# ANNUAL MACRO - WORLD BANK
# =============================================================================

ANNUAL_INDICATORS = {

    "Tăng trưởng kinh tế": {

        "Tăng trưởng GDP (%)":
            "NY.GDP.MKTP.KD.ZG",

        "GDP (USD)":
            "NY.GDP.MKTP.CD",

        "GDP bình quân đầu người (USD)":
            "NY.GDP.PCAP.CD"
    },


    "Lạm phát & Giá cả": {

        "Lạm phát CPI (%)":
            "FP.CPI.TOTL.ZG",

        "Chỉ số giá tiêu dùng CPI":
            "FP.CPI.TOTL",

        "GDP Deflator (%)":
            "NY.GDP.DEFL.KD.ZG"
    },


    "Lãi suất & Tiền tệ": {

        "Lãi suất cho vay (%)":
            "FR.INR.LEND",

        "Lãi suất tiền gửi (%)":
            "FR.INR.DPST",

        "Lãi suất thực (%)":
            "FR.INR.RINR",

        "Cung tiền rộng (% GDP)":
            "FM.LBL.BMNY.GD.ZS"
    },


    "Tín dụng": {

        "Tín dụng khu vực tư nhân (% GDP)":
            "FS.AST.PRVT.GD.ZS",

        "Tín dụng nội địa khu vực tư nhân (% GDP)":
            "FS.AST.DOMS.GD.ZS"
    },


    "Lao động": {

        "Tỷ lệ thất nghiệp (%)":
            "SL.UEM.TOTL.ZS",

        "Tỷ lệ tham gia lực lượng lao động (%)":
            "SL.TLF.CACT.ZS"
    },


    "Khu vực đối ngoại": {

        "Tài khoản vãng lai (% GDP)":
            "BN.CAB.XOKA.GD.ZS",

        "FDI ròng (% GDP)":
            "BX.KLT.DINV.WD.GD.ZS",

        "Dự trữ ngoại hối (USD)":
            "FI.RES.TOTL.CD",

        "Nợ nước ngoài (% GNI)":
            "DT.DOD.DECT.GN.ZS"
    }
}


# =============================================================================
# MONTHLY / QUARTERLY MARKET INDICATORS
# =============================================================================
#
# Yahoo Finance
#
# Dữ liệu daily được tổng hợp thành:
# - Monthly: giá trị cuối tháng
# - Quarterly: giá trị cuối quý
#
# =============================================================================

MARKET_INDICATORS = {

    "Thị trường & Tỷ giá": {

        "USD/VND":
            "VND=X",

        "VN-Index":
            "^VNINDEX",

        "Giá dầu WTI":
            "CL=F",

        "Giá vàng":
            "GC=F",

        "S&P 500":
            "^GSPC",

        "NASDAQ":
            "^IXIC"
    }
}


# =============================================================================
# FLAT INDICATOR DICTIONARY
# =============================================================================

def flatten_indicators(indicator_groups):

    result = {}

    for group_name, group_items in indicator_groups.items():

        for indicator_name, code in group_items.items():

            result[indicator_name] = code

    return result


ANNUAL_INDICATORS_FLAT = flatten_indicators(
    ANNUAL_INDICATORS
)

MARKET_INDICATORS_FLAT = flatten_indicators(
    MARKET_INDICATORS
)


# =============================================================================
# FORMAT VALUE
# =============================================================================

def format_macro_value(value):

    if pd.isna(value):
        return "N/A"

    if abs(value) >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:,.2f} nghìn tỷ"

    elif abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:,.2f} tỷ"

    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:,.2f} triệu"

    return f"{value:,.2f}"


# =============================================================================
# WORLD BANK ANNUAL
# =============================================================================

@st.cache_data(ttl=3600)
def get_world_bank_annual(
    country_names,
    indicator_names,
    start_year,
    end_year
):

    records = []


    for country_name in country_names:

        country_code = COUNTRIES[
            country_name
        ]


        for indicator_name in indicator_names:

            indicator_code = ANNUAL_INDICATORS_FLAT[
                indicator_name
            ]


            url = (
                "https://api.worldbank.org/v2/"
                f"country/{country_code}/"
                f"indicator/{indicator_code}"
            )


            params = {
                "format": "json",
                "date":
                    f"{int(start_year)}:{int(end_year)}",
                "per_page": 5000
            }


            try:

                response = requests.get(
                    url,
                    params=params,
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()


                if (
                    not isinstance(data, list)
                    or len(data) < 2
                    or data[1] is None
                ):

                    continue


                for item in data[1]:

                    value = item.get(
                        "value"
                    )


                    if value is None:

                        continue


                    try:

                        year = int(
                            item.get("date")
                        )

                    except Exception:

                        continue


                    records.append(
                        {
                            "Quốc gia":
                                country_name,

                            "Mã quốc gia":
                                country_code,

                            "Thời gian":
                                str(year),

                            "Ngày":
                                pd.Timestamp(
                                    year=year,
                                    month=1,
                                    day=1
                                ),

                            "Tần suất":
                                "Năm",

                            "Chỉ tiêu":
                                indicator_name,

                            "Mã chỉ tiêu":
                                indicator_code,

                            "Giá trị":
                                value,

                            "Nguồn":
                                "World Bank"
                        }
                    )


            except Exception:

                continue


    df = pd.DataFrame(
        records
    )


    if df.empty:
        return df


    df["Giá trị"] = pd.to_numeric(
        df["Giá trị"],
        errors="coerce"
    )


    df = df.dropna(
        subset=[
            "Ngày",
            "Giá trị"
        ]
    )


    return (
        df
        .sort_values(
            [
                "Quốc gia",
                "Chỉ tiêu",
                "Ngày"
            ]
        )
        .reset_index(
            drop=True
        )
    )


# =============================================================================
# YAHOO FINANCE MARKET DATA
# =============================================================================

@st.cache_data(ttl=3600)
def get_market_data(
    indicator_names,
    frequency,
    start_date,
    end_date
):

    records = []


    for indicator_name in indicator_names:

        ticker = MARKET_INDICATORS_FLAT[
            indicator_name
        ]


        try:

            market_df = yf.download(
                ticker,
                start=start_date,
                end=end_date + pd.Timedelta(days=1),
                interval="1d",
                auto_adjust=False,
                progress=False
            )


            if market_df.empty:
                continue


            # =============================================================
            # FIX MULTIINDEX FROM YFINANCE
            # =============================================================

            if isinstance(
                market_df.columns,
                pd.MultiIndex
            ):

                if "Close" in market_df.columns.get_level_values(0):

                    close_series = (
                        market_df["Close"]
                    )

                    if isinstance(
                        close_series,
                        pd.DataFrame
                    ):

                        close_series = (
                            close_series.iloc[:, 0]
                        )

                else:

                    continue


            else:

                if "Close" not in market_df.columns:
                    continue

                close_series = (
                    market_df["Close"]
                )


            temp = pd.DataFrame(
                {
                    "Ngày":
                        pd.to_datetime(
                            close_series.index
                        ),

                    "Giá trị":
                        pd.to_numeric(
                            close_series.values,
                            errors="coerce"
                        )
                }
            )


            temp = temp.dropna(
                subset=[
                    "Ngày",
                    "Giá trị"
                ]
            )


            temp = (
                temp
                .set_index("Ngày")
                .sort_index()
            )


            # =============================================================
            # MONTHLY
            # =============================================================

            if frequency == "Theo tháng":

                temp = (
                    temp
                    .resample("ME")
                    .last()
                    .dropna()
                )


                temp["Thời gian"] = (
                    temp.index.strftime(
                        "%Y-%m"
                    )
                )


                frequency_name = "Tháng"


            # =============================================================
            # QUARTERLY
            # =============================================================

            else:

                temp = (
                    temp
                    .resample("QE")
                    .last()
                    .dropna()
                )


                temp["Thời gian"] = (
                    temp.index.to_period("Q")
                    .astype(str)
                )


                frequency_name = "Quý"


            # =============================================================
            # OUTPUT
            # =============================================================

            for date_index, row in temp.iterrows():

                records.append(
                    {
                        "Quốc gia":
                            (
                                "Việt Nam"
                                if indicator_name
                                in [
                                    "USD/VND",
                                    "VN-Index"
                                ]
                                else "Thị trường quốc tế"
                            ),

                        "Mã quốc gia":
                            (
                                "VNM"
                                if indicator_name
                                in [
                                    "USD/VND",
                                    "VN-Index"
                                ]
                                else "GLOBAL"
                            ),

                        "Thời gian":
                            row["Thời gian"],

                        "Ngày":
                            date_index,

                        "Tần suất":
                            frequency_name,

                        "Chỉ tiêu":
                            indicator_name,

                        "Mã chỉ tiêu":
                            ticker,

                        "Giá trị":
                            row["Giá trị"],

                        "Nguồn":
                            "Yahoo Finance"
                    }
                )


        except Exception:

            continue


    df = pd.DataFrame(
        records
    )


    if df.empty:
        return df


    return (
        df
        .sort_values(
            [
                "Chỉ tiêu",
                "Ngày"
            ]
        )
        .reset_index(
            drop=True
        )
    )


# =============================================================================
# UNIVERSAL DATA FUNCTION
# =============================================================================

def get_macro_dataset(
    frequency,
    countries,
    indicators,
    start_year,
    end_year,
    start_month=1,
    end_month=12,
    start_quarter=1,
    end_quarter=4
):


    # =========================================================================
    # ANNUAL
    # =========================================================================

    if frequency == "Theo năm":

        return get_world_bank_annual(
            countries,
            indicators,
            start_year,
            end_year
        )


    # =========================================================================
    # MONTHLY
    # =========================================================================

    elif frequency == "Theo tháng":

        start_date = pd.Timestamp(
            year=int(start_year),
            month=int(start_month),
            day=1
        )


        end_date = (
            pd.Timestamp(
                year=int(end_year),
                month=int(end_month),
                day=1
            )
            + pd.offsets.MonthEnd(0)
        )


        return get_market_data(
            indicators,
            "Theo tháng",
            start_date,
            end_date
        )


    # =========================================================================
    # QUARTERLY
    # =========================================================================

    else:

        start_month_q = (
            (int(start_quarter) - 1) * 3
            + 1
        )


        end_month_q = (
            int(end_quarter) * 3
        )


        start_date = pd.Timestamp(
            year=int(start_year),
            month=start_month_q,
            day=1
        )


        end_date = (
            pd.Timestamp(
                year=int(end_year),
                month=end_month_q,
                day=1
            )
            + pd.offsets.MonthEnd(0)
        )


        return get_market_data(
            indicators,
            "Theo quý",
            start_date,
            end_date
        )





# =============================================================================
# TAB 1 - MACRO DATA
# =============================================================================

def tab1():

    st.title("Dữ liệu vĩ mô")

    st.caption(
        "Theo dõi các chỉ tiêu kinh tế vĩ mô và thị trường tài chính "
        "theo tần suất tháng, quý hoặc năm."
    )

    st.divider()


    # =========================================================================
    # FREQUENCY
    # =========================================================================

    st.subheader("Bộ lọc dữ liệu")


    frequency = st.selectbox(
        "Tần suất báo cáo",
        [
            "Theo tháng",
            "Theo quý",
            "Theo năm"
        ],
        index=2,
        key="tab1_frequency"
    )


    # =========================================================================
    # ANNUAL FILTER
    # =========================================================================

    if frequency == "Theo năm":

        c1, c2, c3 = st.columns(3)


        with c1:

            selected_countries = st.multiselect(
                "Quốc gia",
                options=list(
                    COUNTRIES.keys()
                ),
                default=[
                    "Việt Nam"
                ],
                key="tab1_country_annual"
            )


        with c2:

            selected_group = st.selectbox(
                "Nhóm chỉ tiêu",
                options=list(
                    ANNUAL_INDICATORS.keys()
                ),
                key="tab1_group_annual"
            )


        with c3:

            selected_indicator = st.selectbox(
                "Chỉ tiêu",
                options=list(
                    ANNUAL_INDICATORS[
                        selected_group
                    ].keys()
                ),
                key="tab1_indicator_annual"
            )


        selected_indicators = [
            selected_indicator
        ]


    # =========================================================================
    # MONTHLY / QUARTERLY FILTER
    # =========================================================================

    else:

        selected_countries = [
            "Việt Nam"
        ]


        c1, c2 = st.columns(2)


        with c1:

            selected_group = st.selectbox(
                "Nhóm chỉ tiêu",
                options=list(
                    MARKET_INDICATORS.keys()
                ),
                key=f"tab1_group_{frequency}"
            )


        with c2:

            selected_indicator = st.selectbox(
                "Chỉ tiêu",
                options=list(
                    MARKET_INDICATORS[
                        selected_group
                    ].keys()
                ),
                key=f"tab1_indicator_{frequency}"
            )


        selected_indicators = [
            selected_indicator
        ]


    # =========================================================================
    # PERIOD
    # =========================================================================

    current_year = datetime.now().year
    current_month = datetime.now().month


    # -------------------------------------------------------------------------
    # YEAR
    # -------------------------------------------------------------------------

    if frequency == "Theo năm":

        c1, c2 = st.columns(2)


        with c1:

            start_year = st.number_input(
                "Từ năm",
                1960,
                current_year,
                2000,
                key="tab1_start_year"
            )


        with c2:

            end_year = st.number_input(
                "Đến năm",
                1960,
                current_year,
                current_year,
                key="tab1_end_year"
            )


        start_month = 1
        end_month = 12
        start_quarter = 1
        end_quarter = 4


    # -------------------------------------------------------------------------
    # MONTH
    # -------------------------------------------------------------------------

    elif frequency == "Theo tháng":

        c1, c2, c3, c4 = (
            st.columns(4)
        )


        with c1:

            start_year = st.number_input(
                "Từ năm",
                2000,
                current_year,
                2015,
                key="tab1_m_start_y"
            )


        with c2:

            start_month = st.selectbox(
                "Từ tháng",
                range(1, 13),
                index=0,
                key="tab1_m_start_m"
            )


        with c3:

            end_year = st.number_input(
                "Đến năm",
                2000,
                current_year,
                current_year,
                key="tab1_m_end_y"
            )


        with c4:

            end_month = st.selectbox(
                "Đến tháng",
                range(1, 13),
                index=current_month - 1,
                key="tab1_m_end_m"
            )


        start_quarter = 1
        end_quarter = 4


    # -------------------------------------------------------------------------
    # QUARTER
    # -------------------------------------------------------------------------

    else:

        c1, c2, c3, c4 = (
            st.columns(4)
        )


        with c1:

            start_year = st.number_input(
                "Từ năm",
                2000,
                current_year,
                2015,
                key="tab1_q_start_y"
            )


        with c2:

            start_quarter = st.selectbox(
                "Từ quý",
                [1, 2, 3, 4],
                index=0,
                key="tab1_q_start_q"
            )


        with c3:

            end_year = st.number_input(
                "Đến năm",
                2000,
                current_year,
                current_year,
                key="tab1_q_end_y"
            )


        with c4:

            end_quarter = st.selectbox(
                "Đến quý",
                [1, 2, 3, 4],
                index=3,
                key="tab1_q_end_q"
            )


        start_month = 1
        end_month = 12


    # =========================================================================
    # VALIDATION
    # =========================================================================

    if not selected_countries:

        st.warning(
            "Vui lòng chọn ít nhất một quốc gia."
        )

        return


    if start_year > end_year:

        st.error(
            "Thời gian bắt đầu không hợp lệ."
        )

        return


    # =========================================================================
    # LOAD
    # =========================================================================

    with st.spinner(
        "Đang tải dữ liệu..."
    ):

        df = get_macro_dataset(
            frequency,
            selected_countries,
            selected_indicators,
            start_year,
            end_year,
            start_month,
            end_month,
            start_quarter,
            end_quarter
        )


    if df.empty:

        st.warning(
            "Không tìm thấy dữ liệu phù hợp."
        )

        return


    # =========================================================================
    # SUMMARY
    # =========================================================================

    st.subheader(
        "Tổng quan chỉ tiêu"
    )


    # -------------------------------------------------------------------------
    # ONE SERIES
    # -------------------------------------------------------------------------

    series_df = (
        df[
            df["Chỉ tiêu"]
            == selected_indicator
        ]
        .sort_values("Ngày")
    )


    latest = (
        series_df.iloc[-1]
    )


    latest_value = (
        latest["Giá trị"]
    )


    latest_period = (
        latest["Thời gian"]
    )


    if len(series_df) >= 2:

        previous = (
            series_df.iloc[-2]
        )


        previous_value = (
            previous["Giá trị"]
        )


        absolute_change = (
            latest_value
            - previous_value
        )


        percentage_change = (
            (
                latest_value
                / previous_value
                - 1
            )
            * 100

            if previous_value != 0

            else np.nan
        )


    else:

        absolute_change = np.nan
        percentage_change = np.nan


    historical_average = (
        series_df["Giá trị"].mean()
    )


    volatility = (
        series_df["Giá trị"].std()
    )


    k1, k2, k3, k4 = (
        st.columns(4)
    )


    with k1:

        st.metric(
            f"Giá trị mới nhất ({latest_period})",
            format_macro_value(
                latest_value
            )
        )


    with k2:

        st.metric(
            "Thay đổi kỳ trước",

            format_macro_value(
                absolute_change
            ),

            (
                f"{percentage_change:+.2f}%"
                if pd.notna(
                    percentage_change
                )
                else None
            )
        )


    with k3:

        st.metric(
            "Trung bình giai đoạn",
            format_macro_value(
                historical_average
            )
        )


    with k4:

        st.metric(
            "Độ biến động",
            format_macro_value(
                volatility
            )
        )


    # =========================================================================
    # CHART
    # =========================================================================

    st.subheader(
        f"Xu hướng {selected_indicator}"
    )


    fig = go.Figure()


    # Annual supports multiple countries
    if frequency == "Theo năm":

        groups = (
            df.groupby("Quốc gia")
        )


        for country, temp in groups:

            fig.add_trace(
                go.Scatter(
                    x=temp["Ngày"],
                    y=temp["Giá trị"],
                    mode="lines+markers",
                    name=country
                )
            )


    else:

        fig.add_trace(
            go.Scatter(
                x=series_df["Ngày"],
                y=series_df["Giá trị"],
                mode=(
                    "lines"
                    if frequency == "Theo tháng"
                    else "lines+markers"
                ),
                name=selected_indicator
            )
        )


    fig.update_layout(
        template="plotly_dark",
        height=520,
        paper_bgcolor="#0E0E0E",
        plot_bgcolor="#0E0E0E",
        hovermode="x unified",
        xaxis_title=frequency.replace(
            "Theo ",
            ""
        ),
        yaxis_title=selected_indicator,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )


    fig.update_yaxes(
        gridcolor="#2A2A2A"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =========================================================================
    # HISTORICAL STATISTICS
    # =========================================================================

    st.subheader(
        "Thống kê lịch sử"
    )


    s1, s2, s3, s4 = (
        st.columns(4)
    )


    with s1:

        st.metric(
            "Thấp nhất",
            format_macro_value(
                series_df[
                    "Giá trị"
                ].min()
            )
        )


    with s2:

        st.metric(
            "Cao nhất",
            format_macro_value(
                series_df[
                    "Giá trị"
                ].max()
            )
        )


    with s3:

        st.metric(
            "Trung bình",
            format_macro_value(
                historical_average
            )
        )


    with s4:

        st.metric(
            "Độ lệch chuẩn",
            format_macro_value(
                volatility
            )
        )


    # =========================================================================
    # DETAIL
    # =========================================================================

    st.subheader(
        "Dữ liệu chi tiết"
    )


    display_df = (
        df.copy()
        .sort_values(
            [
                "Chỉ tiêu",
                "Ngày"
            ]
        )
    )


    display_df[
        "Thay đổi kỳ trước (%)"
    ] = (

        display_df
        .groupby(
            [
                "Quốc gia",
                "Chỉ tiêu"
            ]
        )["Giá trị"]
        .pct_change()
        * 100

    )


    display_df = (
        display_df
        .sort_values(
            "Ngày",
            ascending=False
        )
    )


    st.dataframe(
        display_df[
            [
                "Quốc gia",
                "Thời gian",
                "Chỉ tiêu",
                "Giá trị",
                "Thay đổi kỳ trước (%)",
                "Nguồn"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


    # =========================================================================
    # DOWNLOAD
    # =========================================================================

    csv = (
        display_df
        .drop(
            columns=["Ngày"]
        )
        .to_csv(
            index=False
        )
        .encode(
            "utf-8-sig"
        )
    )


    st.download_button(
        "Tải dữ liệu CSV",
        csv,
        file_name=(
            f"MACRO_{frequency}_"
            f"{selected_indicator}.csv"
            .replace("/", "_")
            .replace(" ", "_")
        ),
        mime="text/csv",
        use_container_width=True
    )


    st.caption(
        f"Nguồn: {', '.join(df['Nguồn'].unique())} • "
        f"Tần suất: {frequency.replace('Theo ', '')}"
    )


# =============================================================================
# TAB 2 - DATA DOWNLOAD
# =============================================================================

def tab2():

    st.title("Tải dữ liệu")

    st.caption(
        "Tạo bộ dữ liệu vĩ mô theo tần suất tháng, quý hoặc năm "
        "để phục vụ phân tích và Stress Test."
    )

    st.divider()


    # =========================================================================
    # FREQUENCY
    # =========================================================================

    frequency = st.selectbox(
        "Tần suất dữ liệu",
        [
            "Theo tháng",
            "Theo quý",
            "Theo năm"
        ],
        index=2,
        key="tab2_frequency"
    )


    # =========================================================================
    # FILTER
    # =========================================================================

    if frequency == "Theo năm":

        selected_countries = st.multiselect(
            "Quốc gia",
            list(
                COUNTRIES.keys()
            ),
            default=["Việt Nam"],
            key="tab2_countries"
        )


        selected_indicators = (
            st.multiselect(
                "Chỉ tiêu",
                list(
                    ANNUAL_INDICATORS_FLAT.keys()
                ),
                default=[
                    "Tăng trưởng GDP (%)",
                    "Lạm phát CPI (%)"
                ],
                key="tab2_annual_indicators"
            )
        )


    else:

        selected_countries = [
            "Việt Nam"
        ]


        selected_indicators = (
            st.multiselect(
                "Chỉ tiêu",
                list(
                    MARKET_INDICATORS_FLAT.keys()
                ),
                default=[
                    "USD/VND",
                    "VN-Index",
                    "Giá dầu WTI",
                    "Giá vàng"
                ],
                key=f"tab2_market_{frequency}"
            )
        )


    # =========================================================================
    # PERIOD
    # =========================================================================

    current_year = (
        datetime.now().year
    )

    current_month = (
        datetime.now().month
    )


    if frequency == "Theo năm":

        c1, c2 = st.columns(2)


        with c1:

            start_year = st.number_input(
                "Từ năm",
                1960,
                current_year,
                2000,
                key="tab2_a_sy"
            )


        with c2:

            end_year = st.number_input(
                "Đến năm",
                1960,
                current_year,
                current_year,
                key="tab2_a_ey"
            )


        start_month = 1
        end_month = 12
        start_quarter = 1
        end_quarter = 4


    elif frequency == "Theo tháng":

        c1, c2, c3, c4 = (
            st.columns(4)
        )


        with c1:

            start_year = st.number_input(
                "Từ năm",
                2000,
                current_year,
                2015,
                key="tab2_m_sy"
            )


        with c2:

            start_month = st.selectbox(
                "Từ tháng",
                range(1, 13),
                key="tab2_m_sm"
            )


        with c3:

            end_year = st.number_input(
                "Đến năm",
                2000,
                current_year,
                current_year,
                key="tab2_m_ey"
            )


        with c4:

            end_month = st.selectbox(
                "Đến tháng",
                range(1, 13),
                index=current_month - 1,
                key="tab2_m_em"
            )


        start_quarter = 1
        end_quarter = 4


    else:

        c1, c2, c3, c4 = (
            st.columns(4)
        )


        with c1:

            start_year = st.number_input(
                "Từ năm",
                2000,
                current_year,
                2015,
                key="tab2_q_sy"
            )


        with c2:

            start_quarter = st.selectbox(
                "Từ quý",
                [1, 2, 3, 4],
                key="tab2_q_sq"
            )


        with c3:

            end_year = st.number_input(
                "Đến năm",
                2000,
                current_year,
                current_year,
                key="tab2_q_ey"
            )


        with c4:

            end_quarter = st.selectbox(
                "Đến quý",
                [1, 2, 3, 4],
                index=3,
                key="tab2_q_eq"
            )


        start_month = 1
        end_month = 12


    # =========================================================================
    # VALIDATE
    # =========================================================================

    if not selected_indicators:

        st.warning(
            "Vui lòng chọn ít nhất một chỉ tiêu."
        )

        return


    if (
        frequency == "Theo năm"
        and not selected_countries
    ):

        st.warning(
            "Vui lòng chọn ít nhất một quốc gia."
        )

        return


    # =========================================================================
    # SUMMARY
    # =========================================================================

    a, b, c = st.columns(3)


    with a:

        st.metric(
            "Số chỉ tiêu",
            len(selected_indicators)
        )


    with b:

        st.metric(
            "Tần suất",
            frequency.replace(
                "Theo ",
                ""
            )
        )


    with c:

        st.metric(
            "Nguồn",
            (
                "World Bank"
                if frequency == "Theo năm"
                else "Yahoo Finance"
            )
        )


    # =========================================================================
    # LOAD BUTTON
    # =========================================================================

    if st.button(
        "Tải dữ liệu",
        type="primary",
        use_container_width=True,
        key="tab2_load"
    ):


        with st.spinner(
            "Đang tải và tổng hợp dữ liệu..."
        ):

            download_df = get_macro_dataset(
                frequency,
                selected_countries,
                selected_indicators,
                start_year,
                end_year,
                start_month,
                end_month,
                start_quarter,
                end_quarter
            )


        st.session_state[
            "macro_download_data"
        ] = download_df


        st.session_state[
            "macro_download_frequency"
        ] = frequency


    # =========================================================================
    # SESSION
    # =========================================================================

    download_df = (
        st.session_state.get(
            "macro_download_data",
            pd.DataFrame()
        )
    )


    saved_frequency = (
        st.session_state.get(
            "macro_download_frequency"
        )
    )


    if download_df.empty:

        st.info(
            "Chọn bộ lọc và nhấn "
            "'Tải dữ liệu' để tạo dataset."
        )

        return


    if saved_frequency != frequency:

        st.info(
            "Tần suất đã thay đổi. "
            "Nhấn 'Tải dữ liệu' để cập nhật dataset."
        )

        return


    # =========================================================================
    # RAW
    # =========================================================================

    st.success(
        f"Đã tải {len(download_df):,} quan sát."
    )


    st.subheader(
        "Dữ liệu gốc"
    )


    st.dataframe(
        download_df.drop(
            columns=["Ngày"]
        ),
        use_container_width=True,
        hide_index=True
    )


    # =========================================================================
    # WIDE
    # =========================================================================

    st.subheader(
        "Dataset phục vụ Stress Test"
    )


    if frequency == "Theo năm":

        index_columns = [
            "Quốc gia",
            "Mã quốc gia",
            "Thời gian"
        ]


    else:

        index_columns = [
            "Thời gian"
        ]


    wide_df = (
        download_df
        .pivot_table(
            index=index_columns,
            columns="Chỉ tiêu",
            values="Giá trị",
            aggfunc="first"
        )
        .reset_index()
    )


    wide_df.columns.name = None


    st.dataframe(
        wide_df,
        use_container_width=True,
        hide_index=True
    )


    # =========================================================================
    # QUALITY
    # =========================================================================

    st.subheader(
        "Kiểm tra chất lượng dữ liệu"
    )


    missing_records = []


    for indicator in selected_indicators:

        if indicator in wide_df.columns:

            missing_count = (
                wide_df[
                    indicator
                ].isna().sum()
            )

        else:

            missing_count = (
                len(wide_df)
            )


        missing_records.append(
            {
                "Chỉ tiêu":
                    indicator,

                "Số giá trị thiếu":
                    missing_count,

                "Tỷ lệ thiếu (%)":
                    (
                        missing_count
                        / len(wide_df)
                        * 100
                        if len(wide_df)
                        else 0
                    )
            }
        )


    missing_df = pd.DataFrame(
        missing_records
    )


    q1, q2, q3 = (
        st.columns(3)
    )


    total_missing = (
        missing_df[
            "Số giá trị thiếu"
        ].sum()
    )


    total_possible = (
        len(wide_df)
        * len(selected_indicators)
    )


    with q1:

        st.metric(
            "Số kỳ",
            len(wide_df)
        )


    with q2:

        st.metric(
            "Giá trị thiếu",
            int(total_missing)
        )


    with q3:

        st.metric(
            "Tỷ lệ thiếu",
            (
                f"{total_missing / total_possible * 100:.2f}%"
                if total_possible
                else "0.00%"
            )
        )


    with st.expander(
        "Chi tiết dữ liệu thiếu"
    ):

        st.dataframe(
            missing_df,
            use_container_width=True,
            hide_index=True
        )


    # =========================================================================
    # EXPORT
    # =========================================================================

    st.subheader(
        "Xuất dữ liệu"
    )


    csv = (
        wide_df
        .to_csv(
            index=False
        )
        .encode(
            "utf-8-sig"
        )
    )


    excel_buffer = BytesIO()


    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:


        wide_df.to_excel(
            writer,
            index=False,
            sheet_name="Macro Dataset"
        )


        download_df.drop(
            columns=["Ngày"]
        ).to_excel(
            writer,
            index=False,
            sheet_name="Raw Data"
        )


        missing_df.to_excel(
            writer,
            index=False,
            sheet_name="Data Quality"
        )


    c1, c2 = st.columns(2)


    file_frequency = (
        frequency.replace(
            "Theo ",
            ""
        )
        .upper()
    )


    with c1:

        st.download_button(
            "Tải CSV",
            csv,
            file_name=(
                f"MACRO_DATA_"
                f"{file_frequency}.csv"
            ),
            mime="text/csv",
            use_container_width=True
        )


    with c2:

        st.download_button(
            "Tải Excel",
            excel_buffer.getvalue(),
            file_name=(
                f"MACRO_DATA_"
                f"{file_frequency}.xlsx"
            ),
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True
        )


# =============================================================================
# TAB 3 - MACRO ANALYSIS
# =============================================================================

def tab3():

    st.title("Phân tích vĩ mô")

    st.caption(
        "Phân tích xu hướng, thống kê mô tả, tương quan và "
        "mối quan hệ giữa các biến vĩ mô và thị trường."
    )

    st.divider()


    # =========================================================================
    # FREQUENCY
    # =========================================================================

    frequency = st.selectbox(
        "Tần suất phân tích",
        [
            "Theo tháng",
            "Theo quý",
            "Theo năm"
        ],
        index=2,
        key="tab3_frequency"
    )


    # =========================================================================
    # INDICATORS
    # =========================================================================

    if frequency == "Theo năm":

        selected_country = st.selectbox(
            "Quốc gia",
            list(
                COUNTRIES.keys()
            ),
            index=0,
            key="tab3_country"
        )


        selected_countries = [
            selected_country
        ]


        selected_indicators = (
            st.multiselect(
                "Chỉ tiêu phân tích",
                list(
                    ANNUAL_INDICATORS_FLAT.keys()
                ),
                default=[
                    "Tăng trưởng GDP (%)",
                    "Lạm phát CPI (%)",
                    "Lãi suất thực (%)",
                    "Tín dụng khu vực tư nhân (% GDP)"
                ],
                key="tab3_indicators_a"
            )
        )


    else:

        selected_country = (
            "Việt Nam / Thị trường quốc tế"
        )


        selected_countries = [
            "Việt Nam"
        ]


        selected_indicators = (
            st.multiselect(
                "Chỉ tiêu phân tích",
                list(
                    MARKET_INDICATORS_FLAT.keys()
                ),
                default=[
                    "USD/VND",
                    "VN-Index",
                    "Giá dầu WTI",
                    "Giá vàng"
                ],
                key=f"tab3_indicators_{frequency}"
            )
        )


    if not selected_indicators:

        st.warning(
            "Vui lòng chọn ít nhất một chỉ tiêu."
        )

        return


    # =========================================================================
    # PERIOD
    # =========================================================================

    current_year = (
        datetime.now().year
    )

    current_month = (
        datetime.now().month
    )


    if frequency == "Theo năm":

        c1, c2 = st.columns(2)


        with c1:

            start_year = st.number_input(
                "Từ năm",
                1960,
                current_year,
                2000,
                key="tab3_a_sy"
            )


        with c2:

            end_year = st.number_input(
                "Đến năm",
                1960,
                current_year,
                current_year,
                key="tab3_a_ey"
            )


        start_month = 1
        end_month = 12
        start_quarter = 1
        end_quarter = 4


    elif frequency == "Theo tháng":

        c1, c2, c3, c4 = (
            st.columns(4)
        )


        with c1:

            start_year = st.number_input(
                "Từ năm",
                2000,
                current_year,
                2015,
                key="tab3_m_sy"
            )


        with c2:

            start_month = st.selectbox(
                "Từ tháng",
                range(1, 13),
                key="tab3_m_sm"
            )


        with c3:

            end_year = st.number_input(
                "Đến năm",
                2000,
                current_year,
                current_year,
                key="tab3_m_ey"
            )


        with c4:

            end_month = st.selectbox(
                "Đến tháng",
                range(1, 13),
                index=current_month - 1,
                key="tab3_m_em"
            )


        start_quarter = 1
        end_quarter = 4


    else:

        c1, c2, c3, c4 = (
            st.columns(4)
        )


        with c1:

            start_year = st.number_input(
                "Từ năm",
                2000,
                current_year,
                2015,
                key="tab3_q_sy"
            )


        with c2:

            start_quarter = st.selectbox(
                "Từ quý",
                [1, 2, 3, 4],
                key="tab3_q_sq"
            )


        with c3:

            end_year = st.number_input(
                "Đến năm",
                2000,
                current_year,
                current_year,
                key="tab3_q_ey"
            )


        with c4:

            end_quarter = st.selectbox(
                "Đến quý",
                [1, 2, 3, 4],
                index=3,
                key="tab3_q_eq"
            )


        start_month = 1
        end_month = 12


    # =========================================================================
    # LOAD
    # =========================================================================

    with st.spinner(
        "Đang tải dữ liệu phân tích..."
    ):

        raw_df = get_macro_dataset(
            frequency,
            selected_countries,
            selected_indicators,
            start_year,
            end_year,
            start_month,
            end_month,
            start_quarter,
            end_quarter
        )


    if raw_df.empty:

        st.warning(
            "Không tìm thấy dữ liệu phù hợp."
        )

        return


    # =========================================================================
    # PIVOT
    # =========================================================================

    analysis_df = (
        raw_df
        .pivot_table(
            index=[
                "Ngày",
                "Thời gian"
            ],
            columns="Chỉ tiêu",
            values="Giá trị",
            aggfunc="first"
        )
        .reset_index()
        .sort_values("Ngày")
    )


    analysis_df.columns.name = None


    available_indicators = [
        x
        for x in selected_indicators
        if x in analysis_df.columns
    ]


    # =========================================================================
    # OVERVIEW KPI
    # =========================================================================

    st.subheader(
        f"Tổng quan – {selected_country}"
    )


    metric_cols = st.columns(
        min(
            4,
            len(available_indicators)
        )
    )


    for i, indicator in enumerate(
        available_indicators[:4]
    ):


        series = (
            analysis_df[
                [
                    "Thời gian",
                    indicator
                ]
            ]
            .dropna()
        )


        if series.empty:
            continue


        latest = series.iloc[-1]


        delta = None


        if len(series) >= 2:

            delta = (
                latest[indicator]
                - series.iloc[-2][indicator]
            )


        with metric_cols[i]:

            st.metric(
                f"{indicator} ({latest['Thời gian']})",
                f"{latest[indicator]:,.2f}",
                (
                    f"{delta:+.2f}"
                    if delta is not None
                    else None
                )
            )


    # =========================================================================
    # TREND
    # =========================================================================

    st.subheader(
        "Xu hướng các chỉ tiêu"
    )


    normalize = st.toggle(
        "Chuẩn hóa dữ liệu (Z-score)",
        value=True,
        key=f"tab3_normalize_{frequency}"
    )


    chart_df = (
        analysis_df.copy()
    )


    if normalize:

        for indicator in available_indicators:

            mean = (
                chart_df[
                    indicator
                ].mean()
            )


            std = (
                chart_df[
                    indicator
                ].std()
            )


            if (
                pd.notna(std)
                and std != 0
            ):

                chart_df[
                    indicator
                ] = (

                    chart_df[
                        indicator
                    ]
                    - mean

                ) / std


    fig = go.Figure()


    for indicator in available_indicators:

        temp = (
            chart_df[
                [
                    "Ngày",
                    indicator
                ]
            ]
            .dropna()
        )


        fig.add_trace(
            go.Scatter(
                x=temp["Ngày"],
                y=temp[indicator],
                mode="lines",
                name=indicator
            )
        )


    fig.update_layout(
        template="plotly_dark",
        height=550,
        paper_bgcolor="#0E0E0E",
        plot_bgcolor="#0E0E0E",
        hovermode="x unified",
        yaxis_title=(
            "Z-score"
            if normalize
            else "Giá trị"
        ),
        xaxis_title=(
            frequency.replace(
                "Theo ",
                ""
            )
        )
    )


    fig.update_yaxes(
        gridcolor="#2A2A2A"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =========================================================================
    # DESCRIPTIVE
    # =========================================================================

    st.subheader(
        "Thống kê mô tả"
    )


    descriptive = []


    for indicator in available_indicators:

        x = (
            analysis_df[
                indicator
            ]
            .dropna()
        )


        descriptive.append(
            {
                "Chỉ tiêu":
                    indicator,

                "Số quan sát":
                    len(x),

                "Trung bình":
                    x.mean(),

                "Trung vị":
                    x.median(),

                "Thấp nhất":
                    x.min(),

                "Cao nhất":
                    x.max(),

                "Độ lệch chuẩn":
                    x.std()
            }
        )


    descriptive_df = (
        pd.DataFrame(
            descriptive
        )
        .round(3)
    )


    st.dataframe(
        descriptive_df,
        use_container_width=True,
        hide_index=True
    )


    # =========================================================================
    # CORRELATION
    # =========================================================================

    st.subheader(
        "Ma trận tương quan"
    )


    st.caption(
        "Tương quan phản ánh mối liên hệ thống kê "
        "và không đồng nghĩa với quan hệ nhân quả."
    )


    if len(
        available_indicators
    ) >= 2:


        corr_df = (
            analysis_df[
                available_indicators
            ]
            .corr(
                min_periods=3
            )
        )


        heatmap = go.Figure(
            data=go.Heatmap(
                z=corr_df.values,
                x=corr_df.columns,
                y=corr_df.index,
                zmin=-1,
                zmax=1,
                text=np.round(
                    corr_df.values,
                    2
                ),
                texttemplate="%{text}"
            )
        )


        heatmap.update_layout(
            template="plotly_dark",
            height=520,
            paper_bgcolor="#0E0E0E",
            plot_bgcolor="#0E0E0E"
        )


        st.plotly_chart(
            heatmap,
            use_container_width=True
        )


        # =====================================================================
        # TWO VARIABLES
        # =====================================================================

        st.subheader(
            "Phân tích quan hệ giữa hai biến"
        )


        c1, c2 = st.columns(2)


        with c1:

            variable_x = st.selectbox(
                "Biến X",
                available_indicators,
                key=f"tab3_x_{frequency}"
            )


        with c2:

            variable_y = st.selectbox(
                "Biến Y",
                available_indicators,
                index=(
                    1
                    if len(
                        available_indicators
                    ) > 1
                    else 0
                ),
                key=f"tab3_y_{frequency}"
            )


        if variable_x != variable_y:


            pair_df = (
                analysis_df[
                    [
                        "Thời gian",
                        variable_x,
                        variable_y
                    ]
                ]
                .dropna()
            )


            if len(pair_df) >= 3:


                correlation = (
                    pair_df[
                        variable_x
                    ]
                    .corr(
                        pair_df[
                            variable_y
                        ]
                    )
                )


                x = (
                    pair_df[
                        variable_x
                    ].values
                )


                y = (
                    pair_df[
                        variable_y
                    ].values
                )


                slope, intercept = (
                    np.polyfit(
                        x,
                        y,
                        1
                    )
                )


                predicted = (
                    slope * x
                    + intercept
                )


                ss_res = np.sum(
                    (
                        y
                        - predicted
                    ) ** 2
                )


                ss_tot = np.sum(
                    (
                        y
                        - np.mean(y)
                    ) ** 2
                )


                r_squared = (
                    1 - ss_res / ss_tot
                    if ss_tot != 0
                    else np.nan
                )


                m1, m2, m3 = (
                    st.columns(3)
                )


                with m1:

                    st.metric(
                        "Tương quan",
                        f"{correlation:.3f}"
                    )


                with m2:

                    st.metric(
                        "Hệ số hồi quy",
                        f"{slope:.3f}"
                    )


                with m3:

                    st.metric(
                        "R²",
                        f"{r_squared:.3f}"
                    )


                scatter = (
                    go.Figure()
                )


                scatter.add_trace(
                    go.Scatter(
                        x=x,
                        y=y,
                        mode="markers",
                        text=pair_df[
                            "Thời gian"
                        ],
                        name="Quan sát"
                    )
                )


                order = np.argsort(
                    x
                )


                scatter.add_trace(
                    go.Scatter(
                        x=x[order],
                        y=predicted[
                            order
                        ],
                        mode="lines",
                        name="Đường hồi quy"
                    )
                )


                scatter.update_layout(
                    template="plotly_dark",
                    height=500,
                    paper_bgcolor="#0E0E0E",
                    plot_bgcolor="#0E0E0E",
                    xaxis_title=variable_x,
                    yaxis_title=variable_y
                )


                st.plotly_chart(
                    scatter,
                    use_container_width=True
                )


                # =============================================================
                # INTERPRETATION
                # =============================================================

                abs_corr = abs(
                    correlation
                )


                if abs_corr >= 0.7:
                    strength = "mạnh"

                elif abs_corr >= 0.4:
                    strength = "trung bình"

                elif abs_corr >= 0.2:
                    strength = "yếu"

                else:
                    strength = "rất yếu"


                direction = (
                    "cùng chiều"
                    if correlation > 0
                    else
                    "ngược chiều"
                    if correlation < 0
                    else
                    "không đáng kể"
                )


                st.info(
                    f"{variable_x} và {variable_y} "
                    f"có tương quan {direction} "
                    f"ở mức {strength} "
                    f"(r = {correlation:.3f}). "
                    "Kết quả chỉ phản ánh mối liên hệ thống kê."
                )


            else:

                st.warning(
                    "Không đủ số quan sát chung."
                )


    else:

        st.info(
            "Chọn ít nhất hai chỉ tiêu "
            "để phân tích tương quan."
        )


    # =========================================================================
    # DETAIL DATA
    # =========================================================================

    with st.expander(
        "Xem dữ liệu sử dụng trong phân tích"
    ):

        st.dataframe(
            analysis_df
            .drop(columns=["Ngày"])
            .sort_values(
                "Thời gian",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )


    # =========================================================================
    # SOURCE
    # =========================================================================

    st.divider()


    st.caption(
        f"Tần suất: {frequency.replace('Theo ', '')} • "
        f"Nguồn: {', '.join(raw_df['Nguồn'].unique())}"
    )


# =============================================================================
# TAB 4 - STRESS SCENARIO
# =============================================================================


def tab4():

    st.title("Kịch bản Stress Test")

    st.caption(
        "Xây dựng và điều chỉnh các kịch bản kinh tế vĩ mô "
        "phục vụ đánh giá mức độ chịu đựng của danh mục tín dụng."
    )

    st.divider()


    # =========================================================================
    # KỊCH BẢN MẪU
    # =========================================================================

    scenario_templates = {

        "Cơ sở": {
            "GDP Growth (%)": 6.5,
            "Inflation (%)": 3.5,
            "Interest Rate (%)": 5.0,
            "FX Shock (%)": 2.0,
            "Credit Growth (%)": 12.0,
            "Unemployment (%)": 2.3,
            "VN-Index Shock (%)": 0.0
        },

        "Bất lợi": {
            "GDP Growth (%)": 3.0,
            "Inflation (%)": 5.0,
            "Interest Rate (%)": 7.0,
            "FX Shock (%)": 8.0,
            "Credit Growth (%)": 7.0,
            "Unemployment (%)": 3.5,
            "VN-Index Shock (%)": -20.0
        },

        "Bất lợi nghiêm trọng": {
            "GDP Growth (%)": -1.0,
            "Inflation (%)": 7.5,
            "Interest Rate (%)": 9.0,
            "FX Shock (%)": 15.0,
            "Credit Growth (%)": 2.0,
            "Unemployment (%)": 5.0,
            "VN-Index Shock (%)": -35.0
        }
    }


    # =========================================================================
    # CHỌN KỊCH BẢN
    # =========================================================================

    st.subheader("Lựa chọn kịch bản")

    scenario_type = st.selectbox(
        "Loại kịch bản",
        [
            "Cơ sở",
            "Bất lợi",
            "Bất lợi nghiêm trọng",
            "Tùy chỉnh"
        ],
        index=0
    )


    # =========================================================================
    # LOAD GIÁ TRỊ MẶC ĐỊNH
    # =========================================================================

    if scenario_type != "Tùy chỉnh":

        default_values = scenario_templates[
            scenario_type
        ]

    else:

        default_values = {
            "GDP Growth (%)": 5.0,
            "Inflation (%)": 4.0,
            "Interest Rate (%)": 6.0,
            "FX Shock (%)": 5.0,
            "Credit Growth (%)": 10.0,
            "Unemployment (%)": 3.0,
            "VN-Index Shock (%)": -10.0
        }


    # =========================================================================
    # THÔNG TIN KỊCH BẢN
    # =========================================================================

    if scenario_type == "Cơ sở":

        st.info(
            "Kịch bản cơ sở phản ánh điều kiện kinh tế kỳ vọng "
            "trong trường hợp không xảy ra cú sốc lớn."
        )

    elif scenario_type == "Bất lợi":

        st.warning(
            "Kịch bản bất lợi phản ánh môi trường kinh tế suy yếu, "
            "lạm phát và lãi suất tăng, đồng thời thị trường tài chính giảm."
        )

    elif scenario_type == "Bất lợi nghiêm trọng":

        st.error(
            "Kịch bản bất lợi nghiêm trọng mô phỏng suy thoái mạnh, "
            "biến động tỷ giá lớn và suy giảm mạnh trên thị trường tài chính."
        )

    else:

        st.info(
            "Kịch bản tùy chỉnh cho phép người dùng tự thiết lập "
            "toàn bộ các giả định Stress Test."
        )


    # =========================================================================
    # THIẾT LẬP BIẾN VĨ MÔ
    # =========================================================================

    st.subheader("Thiết lập giả định vĩ mô")

    col1, col2 = st.columns(2)


    # -------------------------------------------------------------------------
    # GDP
    # -------------------------------------------------------------------------

    with col1:

        gdp_growth = st.slider(
            "Tăng trưởng GDP (%)",
            min_value=-10.0,
            max_value=15.0,
            value=float(
                default_values["GDP Growth (%)"]
            ),
            step=0.1
        )


    # -------------------------------------------------------------------------
    # INFLATION
    # -------------------------------------------------------------------------

    with col2:

        inflation = st.slider(
            "Lạm phát CPI (%)",
            min_value=-2.0,
            max_value=20.0,
            value=float(
                default_values["Inflation (%)"]
            ),
            step=0.1
        )


    # -------------------------------------------------------------------------
    # INTEREST RATE
    # -------------------------------------------------------------------------

    with col1:

        interest_rate = st.slider(
            "Lãi suất (%)",
            min_value=0.0,
            max_value=20.0,
            value=float(
                default_values["Interest Rate (%)"]
            ),
            step=0.1
        )


    # -------------------------------------------------------------------------
    # FX
    # -------------------------------------------------------------------------

    with col2:

        fx_shock = st.slider(
            "Cú sốc tỷ giá (%)",
            min_value=-20.0,
            max_value=40.0,
            value=float(
                default_values["FX Shock (%)"]
            ),
            step=0.5
        )


    # -------------------------------------------------------------------------
    # CREDIT GROWTH
    # -------------------------------------------------------------------------

    with col1:

        credit_growth = st.slider(
            "Tăng trưởng tín dụng (%)",
            min_value=-10.0,
            max_value=30.0,
            value=float(
                default_values["Credit Growth (%)"]
            ),
            step=0.5
        )


    # -------------------------------------------------------------------------
    # UNEMPLOYMENT
    # -------------------------------------------------------------------------

    with col2:

        unemployment = st.slider(
            "Tỷ lệ thất nghiệp (%)",
            min_value=0.0,
            max_value=15.0,
            value=float(
                default_values["Unemployment (%)"]
            ),
            step=0.1
        )


    # -------------------------------------------------------------------------
    # VNINDEX
    # -------------------------------------------------------------------------

    vnindex_shock = st.slider(
        "Cú sốc VN-Index (%)",
        min_value=-70.0,
        max_value=30.0,
        value=float(
            default_values["VN-Index Shock (%)"]
        ),
        step=1.0
    )


    # =========================================================================
    # TẠO DATAFRAME KỊCH BẢN
    # =========================================================================

    scenario_df = pd.DataFrame(
        {
            "Biến vĩ mô": [
                "Tăng trưởng GDP",
                "Lạm phát CPI",
                "Lãi suất",
                "Tỷ giá",
                "Tăng trưởng tín dụng",
                "Tỷ lệ thất nghiệp",
                "VN-Index"
            ],

            "Giá trị kịch bản": [
                gdp_growth,
                inflation,
                interest_rate,
                fx_shock,
                credit_growth,
                unemployment,
                vnindex_shock
            ],

            "Đơn vị": [
                "%",
                "%",
                "%",
                "%",
                "%",
                "%",
                "%"
            ]
        }
    )


    # =========================================================================
    # HIỂN THỊ KỊCH BẢN
    # =========================================================================

    st.subheader("Tóm tắt kịch bản")

    st.dataframe(
        scenario_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Giá trị kịch bản":
                st.column_config.NumberColumn(
                    "Giá trị kịch bản",
                    format="%.2f"
                )
        }
    )


    # =========================================================================
    # KPI TÓM TẮT
    # =========================================================================

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(
            "GDP Growth",
            f"{gdp_growth:.1f}%"
        )

    with k2:

        st.metric(
            "Inflation",
            f"{inflation:.1f}%"
        )

    with k3:

        st.metric(
            "Interest Rate",
            f"{interest_rate:.1f}%"
        )

    with k4:

        st.metric(
            "FX Shock",
            f"{fx_shock:+.1f}%"
        )


    # =========================================================================
    # BIỂU ĐỒ KỊCH BẢN
    # =========================================================================

    st.subheader("Biểu đồ kịch bản")

    fig = go.Figure()


    fig.add_trace(
        go.Bar(
            x=scenario_df["Biến vĩ mô"],
            y=scenario_df["Giá trị kịch bản"],
            text=[
                f"{x:.1f}%"
                for x in scenario_df["Giá trị kịch bản"]
            ],
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Giá trị: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )


    fig.update_layout(
        template="plotly_dark",
        height=500,
        paper_bgcolor="#0E0E0E",
        plot_bgcolor="#0E0E0E",
        xaxis_title="Biến vĩ mô",
        yaxis_title="Giá trị (%)",
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )


    fig.update_xaxes(
        showgrid=False
    )


    fig.update_yaxes(
        gridcolor="#2A2A2A"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =========================================================================
    # ĐÁNH GIÁ MỨC ĐỘ STRESS
    # =========================================================================

    st.subheader("Đánh giá mức độ căng thẳng")


    stress_score = 0


    # GDP thấp -> stress cao
    if gdp_growth < 0:
        stress_score += 3

    elif gdp_growth < 3:
        stress_score += 2

    elif gdp_growth < 5:
        stress_score += 1


    # Inflation
    if inflation >= 8:
        stress_score += 3

    elif inflation >= 6:
        stress_score += 2

    elif inflation >= 4.5:
        stress_score += 1


    # Interest rate
    if interest_rate >= 10:
        stress_score += 3

    elif interest_rate >= 8:
        stress_score += 2

    elif interest_rate >= 6.5:
        stress_score += 1


    # FX
    if fx_shock >= 15:
        stress_score += 3

    elif fx_shock >= 10:
        stress_score += 2

    elif fx_shock >= 5:
        stress_score += 1


    # Unemployment
    if unemployment >= 6:
        stress_score += 3

    elif unemployment >= 4:
        stress_score += 2

    elif unemployment >= 3:
        stress_score += 1


    # Stock market
    if vnindex_shock <= -40:
        stress_score += 3

    elif vnindex_shock <= -25:
        stress_score += 2

    elif vnindex_shock <= -10:
        stress_score += 1


    # =========================================================================
    # PHÂN LOẠI
    # =========================================================================

    if stress_score >= 12:

        stress_level = "Rất cao"

        st.error(
            f"Mức độ Stress: {stress_level} "
            f"(Stress Score = {stress_score})"
        )

    elif stress_score >= 8:

        stress_level = "Cao"

        st.warning(
            f"Mức độ Stress: {stress_level} "
            f"(Stress Score = {stress_score})"
        )

    elif stress_score >= 4:

        stress_level = "Trung bình"

        st.warning(
            f"Mức độ Stress: {stress_level} "
            f"(Stress Score = {stress_score})"
        )

    else:

        stress_level = "Thấp"

        st.success(
            f"Mức độ Stress: {stress_level} "
            f"(Stress Score = {stress_score})"
        )


    # =========================================================================
    # GỢI Ý DIỄN GIẢI
    # =========================================================================

    st.subheader("Nhận định kịch bản")


    comments = []


    if gdp_growth < 0:

        comments.append(
            "Nền kinh tế rơi vào trạng thái suy giảm, "
            "có thể làm gia tăng rủi ro tín dụng."
        )

    elif gdp_growth < 3:

        comments.append(
            "Tăng trưởng GDP ở mức thấp, "
            "phản ánh môi trường kinh doanh suy yếu."
        )


    if inflation >= 6:

        comments.append(
            "Lạm phát ở mức cao có thể tạo áp lực "
            "lên chi phí hoạt động và sức mua."
        )


    if interest_rate >= 8:

        comments.append(
            "Mặt bằng lãi suất cao có thể làm tăng "
            "nghĩa vụ trả nợ của khách hàng."
        )


    if fx_shock >= 10:

        comments.append(
            "Biến động tỷ giá lớn có thể ảnh hưởng "
            "đến khách hàng có nghĩa vụ ngoại tệ."
        )


    if credit_growth <= 5:

        comments.append(
            "Tăng trưởng tín dụng thấp có thể phản ánh "
            "suy giảm nhu cầu tín dụng hoặc điều kiện tín dụng thắt chặt."
        )


    if unemployment >= 4:

        comments.append(
            "Tỷ lệ thất nghiệp tăng có thể làm suy giảm "
            "khả năng trả nợ của khách hàng cá nhân."
        )


    if vnindex_shock <= -25:

        comments.append(
            "Thị trường chứng khoán giảm mạnh có thể phản ánh "
            "sự suy giảm kỳ vọng và mức độ chấp nhận rủi ro của thị trường."
        )


    if comments:

        for comment in comments:

            st.write(
                f"• {comment}"
            )

    else:

        st.write(
            "Các giả định hiện tại chưa cho thấy mức độ căng thẳng lớn "
            "đối với môi trường kinh tế vĩ mô."
        )


    # =========================================================================
    # LƯU KỊCH BẢN
    # =========================================================================

    st.divider()

    st.subheader("Lưu kịch bản")


    scenario_name = st.text_input(
        "Tên kịch bản",
        value=scenario_type
    )


    if st.button(
        "Lưu kịch bản để chạy Stress Test",
        type="primary",
        use_container_width=True
    ):

        scenario_data = {

            "Tên kịch bản":
                scenario_name,

            "Loại kịch bản":
                scenario_type,

            "GDP Growth":
                gdp_growth,

            "Inflation":
                inflation,

            "Interest Rate":
                interest_rate,

            "FX Shock":
                fx_shock,

            "Credit Growth":
                credit_growth,

            "Unemployment":
                unemployment,

            "VNIndex Shock":
                vnindex_shock,

            "Stress Score":
                stress_score,

            "Stress Level":
                stress_level
        }


        st.session_state[
            "stress_scenario"
        ] = scenario_data


        st.success(
            f"Đã lưu kịch bản '{scenario_name}'. "
            "Bạn có thể chuyển sang tab Stress Test để sử dụng."
        )


    # =========================================================================
    # HIỂN THỊ KỊCH BẢN ĐÃ LƯU
    # =========================================================================

    if "stress_scenario" in st.session_state:

        with st.expander(
            "Xem kịch bản đang được lưu"
        ):

            saved_scenario = (
                st.session_state[
                    "stress_scenario"
                ]
            )

            saved_df = pd.DataFrame(
                saved_scenario.items(),
                columns=[
                    "Thông tin",
                    "Giá trị"
                ]
            )

            st.dataframe(
                saved_df,
                use_container_width=True,
                hide_index=True
            )


# =============================================================================
# TAB 5 - STRESS TEST
# =============================================================================

def tab5():

    st.title("Stress Test")

    st.caption(
        "Đánh giá tác động của các kịch bản kinh tế vĩ mô "
        "đến rủi ro tín dụng và các chỉ tiêu danh mục."
    )

    st.divider()


    # =========================================================================
    # KIỂM TRA KỊCH BẢN ĐÃ LƯU
    # =========================================================================

    if "stress_scenario" not in st.session_state:

        st.warning(
            "Chưa có kịch bản Stress Test được lưu. "
            "Vui lòng chuyển sang tab 'Stress Scenario' "
            "để thiết lập và lưu kịch bản trước."
        )

        return


    scenario = st.session_state["stress_scenario"]


    # =========================================================================
    # THÔNG TIN KỊCH BẢN
    # =========================================================================

    st.subheader("Kịch bản đang sử dụng")


    scenario_name = scenario.get(
        "Tên kịch bản",
        "Không xác định"
    )

    scenario_type = scenario.get(
        "Loại kịch bản",
        "Không xác định"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Tên kịch bản",
            scenario_name
        )


    with col2:

        st.metric(
            "Loại kịch bản",
            scenario_type
        )


    with col3:

        st.metric(
            "Mức độ Stress",
            scenario.get(
                "Stress Level",
                "N/A"
            )
        )


    # =========================================================================
    # HIỂN THỊ CÁC BIẾN VĨ MÔ
    # =========================================================================

    st.subheader("Giả định kinh tế vĩ mô")


    macro_df = pd.DataFrame(
        {
            "Biến vĩ mô": [
                "Tăng trưởng GDP",
                "Lạm phát CPI",
                "Lãi suất",
                "Cú sốc tỷ giá",
                "Tăng trưởng tín dụng",
                "Tỷ lệ thất nghiệp",
                "Cú sốc VN-Index"
            ],

            "Giá trị": [
                scenario.get("GDP Growth", 0),
                scenario.get("Inflation", 0),
                scenario.get("Interest Rate", 0),
                scenario.get("FX Shock", 0),
                scenario.get("Credit Growth", 0),
                scenario.get("Unemployment", 0),
                scenario.get("VNIndex Shock", 0)
            ],

            "Đơn vị": [
                "%",
                "%",
                "%",
                "%",
                "%",
                "%",
                "%"
            ]
        }
    )


    st.dataframe(
        macro_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Giá trị":
                st.column_config.NumberColumn(
                    "Giá trị",
                    format="%.2f"
                )
        }
    )


    st.divider()


    # =========================================================================
    # INPUT DANH MỤC
    # =========================================================================

    st.subheader("Thông số danh mục tín dụng")


    col1, col2 = st.columns(2)


    # -------------------------------------------------------------------------
    # EAD
    # -------------------------------------------------------------------------

    with col1:

        ead = st.number_input(
            "Tổng dư nợ / EAD (tỷ VND)",
            min_value=0.0,
            value=10000.0,
            step=100.0
        )


    # -------------------------------------------------------------------------
    # BASE PD
    # -------------------------------------------------------------------------

    with col2:

        base_pd = st.number_input(
            "PD cơ sở (%)",
            min_value=0.0,
            max_value=100.0,
            value=2.0,
            step=0.1
        )


    # -------------------------------------------------------------------------
    # LGD
    # -------------------------------------------------------------------------

    with col1:

        lgd = st.number_input(
            "LGD (%)",
            min_value=0.0,
            max_value=100.0,
            value=45.0,
            step=1.0
        )


    # -------------------------------------------------------------------------
    # NPL
    # -------------------------------------------------------------------------

    with col2:

        base_npl = st.number_input(
            "Tỷ lệ NPL hiện tại (%)",
            min_value=0.0,
            max_value=100.0,
            value=2.0,
            step=0.1
        )


    # -------------------------------------------------------------------------
    # CAR
    # -------------------------------------------------------------------------

    with col1:

        base_car = st.number_input(
            "CAR hiện tại (%)",
            min_value=0.0,
            max_value=100.0,
            value=11.0,
            step=0.1
        )


    # -------------------------------------------------------------------------
    # CAPITAL
    # -------------------------------------------------------------------------

    with col2:

        capital = st.number_input(
            "Vốn tự có (tỷ VND)",
            min_value=0.0,
            value=1500.0,
            step=50.0
        )


    # =========================================================================
    # LẤY BIẾN VĨ MÔ
    # =========================================================================

    gdp = scenario.get(
        "GDP Growth",
        0
    )

    inflation = scenario.get(
        "Inflation",
        0
    )

    interest_rate = scenario.get(
        "Interest Rate",
        0
    )

    fx_shock = scenario.get(
        "FX Shock",
        0
    )

    credit_growth = scenario.get(
        "Credit Growth",
        0
    )

    unemployment = scenario.get(
        "Unemployment",
        0
    )

    vnindex_shock = scenario.get(
        "VNIndex Shock",
        0
    )


    # =========================================================================
    # STRESS MODEL - PROTOTYPE
    # =========================================================================
    #
    # Đây là mô hình minh họa.
    # Sau này có thể thay bằng regression / ML model.
    #
    # PD stress =
    # base PD
    # + GDP effect
    # + inflation effect
    # + rate effect
    # + FX effect
    # + unemployment effect
    # + market effect
    #
    # =========================================================================


    # -------------------------------------------------------------------------
    # GDP EFFECT
    # GDP thấp hơn 6% -> tăng PD
    # -------------------------------------------------------------------------

    gdp_effect = max(
        0,
        6.0 - gdp
    ) * 0.20


    # -------------------------------------------------------------------------
    # INFLATION EFFECT
    # Inflation > 4% -> tăng PD
    # -------------------------------------------------------------------------

    inflation_effect = max(
        0,
        inflation - 4.0
    ) * 0.08


    # -------------------------------------------------------------------------
    # INTEREST RATE EFFECT
    # Rate > 5% -> tăng PD
    # -------------------------------------------------------------------------

    rate_effect = max(
        0,
        interest_rate - 5.0
    ) * 0.12


    # -------------------------------------------------------------------------
    # FX EFFECT
    # -------------------------------------------------------------------------

    fx_effect = max(
        0,
        fx_shock
    ) * 0.03


    # -------------------------------------------------------------------------
    # UNEMPLOYMENT EFFECT
    # -------------------------------------------------------------------------

    unemployment_effect = max(
        0,
        unemployment - 2.5
    ) * 0.25


    # -------------------------------------------------------------------------
    # STOCK MARKET EFFECT
    # Chỉ tính khi VNIndex giảm
    # -------------------------------------------------------------------------

    market_effect = max(
        0,
        -vnindex_shock
    ) * 0.015


    # =========================================================================
    # STRESSED PD
    # =========================================================================

    stressed_pd = (
        base_pd
        + gdp_effect
        + inflation_effect
        + rate_effect
        + fx_effect
        + unemployment_effect
        + market_effect
    )


    stressed_pd = min(
        stressed_pd,
        100
    )


    # =========================================================================
    # EXPECTED LOSS
    # =========================================================================

    base_expected_loss = (
        ead
        * (base_pd / 100)
        * (lgd / 100)
    )


    stressed_expected_loss = (
        ead
        * (stressed_pd / 100)
        * (lgd / 100)
    )


    incremental_loss = (
        stressed_expected_loss
        - base_expected_loss
    )


    # =========================================================================
    # STRESSED NPL
    # =========================================================================

    npl_increase = (
        max(
            0,
            stressed_pd - base_pd
        )
        * 0.65
    )


    stressed_npl = (
        base_npl
        + npl_increase
    )


    stressed_npl = min(
        stressed_npl,
        100
    )


    # =========================================================================
    # STRESSED CAPITAL
    # =========================================================================

    stressed_capital = max(
        0,
        capital - incremental_loss
    )


    # =========================================================================
    # CAR
    # Simplified approximation:
    # CAR stress giảm theo mức tổn thất tăng thêm
    # =========================================================================

    if capital > 0:

        car_reduction = (
            incremental_loss
            / capital
            * base_car
        )

    else:

        car_reduction = 0


    stressed_car = max(
        0,
        base_car - car_reduction
    )


    # =========================================================================
    # KẾT QUẢ STRESS TEST
    # =========================================================================

    st.divider()

    st.subheader("Kết quả Stress Test")


    k1, k2, k3, k4 = st.columns(4)


    # -------------------------------------------------------------------------
    # PD
    # -------------------------------------------------------------------------

    with k1:

        st.metric(
            "PD sau Stress",
            f"{stressed_pd:.2f}%",
            delta=(
                f"{stressed_pd - base_pd:+.2f} điểm %"
            ),
            delta_color="inverse"
        )


    # -------------------------------------------------------------------------
    # NPL
    # -------------------------------------------------------------------------

    with k2:

        st.metric(
            "NPL sau Stress",
            f"{stressed_npl:.2f}%",
            delta=(
                f"{stressed_npl - base_npl:+.2f} điểm %"
            ),
            delta_color="inverse"
        )


    # -------------------------------------------------------------------------
    # EXPECTED LOSS
    # -------------------------------------------------------------------------

    with k3:

        st.metric(
            "Expected Loss",
            f"{stressed_expected_loss:,.2f} tỷ",
            delta=(
                f"{incremental_loss:+,.2f} tỷ"
            ),
            delta_color="inverse"
        )


    # -------------------------------------------------------------------------
    # CAR
    # -------------------------------------------------------------------------

    with k4:

        st.metric(
            "CAR sau Stress",
            f"{stressed_car:.2f}%",
            delta=(
                f"{stressed_car - base_car:+.2f} điểm %"
            )
        )


    # =========================================================================
    # SO SÁNH BASELINE / STRESS
    # =========================================================================

    st.subheader("So sánh trước và sau Stress")


    comparison_df = pd.DataFrame(
        {
            "Chỉ tiêu": [
                "PD (%)",
                "NPL (%)",
                "Expected Loss (tỷ VND)",
                "CAR (%)",
                "Vốn tự có (tỷ VND)"
            ],

            "Trước Stress": [
                base_pd,
                base_npl,
                base_expected_loss,
                base_car,
                capital
            ],

            "Sau Stress": [
                stressed_pd,
                stressed_npl,
                stressed_expected_loss,
                stressed_car,
                stressed_capital
            ]
        }
    )


    comparison_df["Thay đổi"] = (
        comparison_df["Sau Stress"]
        - comparison_df["Trước Stress"]
    )


    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Trước Stress":
                st.column_config.NumberColumn(
                    "Trước Stress",
                    format="%.2f"
                ),

            "Sau Stress":
                st.column_config.NumberColumn(
                    "Sau Stress",
                    format="%.2f"
                ),

            "Thay đổi":
                st.column_config.NumberColumn(
                    "Thay đổi",
                    format="%+.2f"
                )
        }
    )


    # =========================================================================
    # BIỂU ĐỒ SO SÁNH
    # =========================================================================

    st.subheader("Tác động của Stress Test")


    chart_df = pd.DataFrame(
        {
            "Chỉ tiêu": [
                "PD",
                "NPL",
                "CAR"
            ],

            "Trước Stress": [
                base_pd,
                base_npl,
                base_car
            ],

            "Sau Stress": [
                stressed_pd,
                stressed_npl,
                stressed_car
            ]
        }
    )


    fig = go.Figure()


    fig.add_trace(
        go.Bar(
            name="Trước Stress",
            x=chart_df["Chỉ tiêu"],
            y=chart_df["Trước Stress"],
            text=[
                f"{x:.2f}%"
                for x in chart_df["Trước Stress"]
            ],
            textposition="outside"
        )
    )


    fig.add_trace(
        go.Bar(
            name="Sau Stress",
            x=chart_df["Chỉ tiêu"],
            y=chart_df["Sau Stress"],
            text=[
                f"{x:.2f}%"
                for x in chart_df["Sau Stress"]
            ],
            textposition="outside"
        )
    )


    fig.update_layout(
        template="plotly_dark",
        height=500,
        barmode="group",
        paper_bgcolor="#0E0E0E",
        plot_bgcolor="#0E0E0E",
        xaxis_title="Chỉ tiêu",
        yaxis_title="%",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )


    fig.update_xaxes(
        showgrid=False
    )


    fig.update_yaxes(
        gridcolor="#2A2A2A"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =========================================================================
    # EXPECTED LOSS CHART
    # =========================================================================

    st.subheader("Tác động đến Expected Loss")


    loss_df = pd.DataFrame(
        {
            "Trạng thái": [
                "Trước Stress",
                "Sau Stress"
            ],

            "Expected Loss": [
                base_expected_loss,
                stressed_expected_loss
            ]
        }
    )


    loss_fig = go.Figure()


    loss_fig.add_trace(
        go.Bar(
            x=loss_df["Trạng thái"],
            y=loss_df["Expected Loss"],
            text=[
                f"{x:,.2f}"
                for x in loss_df["Expected Loss"]
            ],
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Expected Loss: %{y:,.2f} tỷ VND"
                "<extra></extra>"
            )
        )
    )


    loss_fig.update_layout(
        template="plotly_dark",
        height=450,
        paper_bgcolor="#0E0E0E",
        plot_bgcolor="#0E0E0E",
        yaxis_title="Tỷ VND",
        xaxis_title="",
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )


    loss_fig.update_xaxes(
        showgrid=False
    )


    loss_fig.update_yaxes(
        gridcolor="#2A2A2A"
    )


    st.plotly_chart(
        loss_fig,
        use_container_width=True
    )


    # =========================================================================
    # PHÂN RÃ TÁC ĐỘNG LÊN PD
    # =========================================================================

    st.subheader("Phân rã tác động lên PD")


    pd_driver_df = pd.DataFrame(
        {
            "Yếu tố": [
                "GDP",
                "Lạm phát",
                "Lãi suất",
                "Tỷ giá",
                "Thất nghiệp",
                "VN-Index"
            ],

            "Tác động lên PD": [
                gdp_effect,
                inflation_effect,
                rate_effect,
                fx_effect,
                unemployment_effect,
                market_effect
            ]
        }
    )


    pd_driver_df = pd_driver_df.sort_values(
        "Tác động lên PD",
        ascending=False
    )


    driver_fig = go.Figure()


    driver_fig.add_trace(
        go.Bar(
            x=pd_driver_df["Tác động lên PD"],
            y=pd_driver_df["Yếu tố"],
            orientation="h",
            text=[
                f"{x:.2f}"
                for x in pd_driver_df["Tác động lên PD"]
            ],
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Tác động PD: %{x:.2f} điểm %"
                "<extra></extra>"
            )
        )
    )


    driver_fig.update_layout(
        template="plotly_dark",
        height=450,
        paper_bgcolor="#0E0E0E",
        plot_bgcolor="#0E0E0E",
        xaxis_title="Tác động lên PD (điểm %)",
        yaxis_title="",
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )


    driver_fig.update_xaxes(
        gridcolor="#2A2A2A"
    )


    driver_fig.update_yaxes(
        showgrid=False
    )


    st.plotly_chart(
        driver_fig,
        use_container_width=True
    )


    # =========================================================================
    # ĐÁNH GIÁ RỦI RO
    # =========================================================================

    st.subheader("Đánh giá kết quả")


    if stressed_pd >= 10:

        st.error(
            "PD tăng lên mức rất cao dưới kịch bản Stress. "
            "Danh mục có dấu hiệu chịu tác động đáng kể từ các yếu tố vĩ mô."
        )

    elif stressed_pd >= 5:

        st.warning(
            "PD tăng đáng kể dưới kịch bản Stress. "
            "Cần theo dõi các phân khúc hoặc khách hàng nhạy cảm "
            "với biến động kinh tế vĩ mô."
        )

    else:

        st.success(
            "PD sau Stress vẫn ở mức tương đối kiểm soát "
            "theo các giả định của mô hình hiện tại."
        )


    if stressed_car < 8:

        st.error(
            "CAR sau Stress giảm xuống mức thấp. "
            "Cần đánh giá thêm khả năng hấp thụ tổn thất và nhu cầu vốn."
        )

    elif stressed_car < base_car:

        st.warning(
            "CAR suy giảm dưới tác động của tổn thất tín dụng tăng thêm."
        )


    # =========================================================================
    # MODEL DETAILS
    # =========================================================================

    with st.expander(
        "Xem chi tiết mô hình Stress Test"
    ):

        st.markdown(
            """
            **Mô hình hiện tại là phiên bản prototype.**

            PD sau Stress được ước tính từ PD cơ sở và tác động của:

            - Tăng trưởng GDP
            - Lạm phát
            - Lãi suất
            - Tỷ giá
            - Tỷ lệ thất nghiệp
            - Thị trường chứng khoán

            Expected Loss được tính theo:

            **Expected Loss = EAD × PD × LGD**

            NPL và CAR hiện được ước tính bằng các quan hệ đơn giản để
            minh họa luồng Stress Test.

            Khi triển khai mô hình chính thức, các hệ số tác động cần được
            ước lượng và hiệu chỉnh bằng dữ liệu lịch sử thực tế.
            """
        )


    # =========================================================================
    # LƯU KẾT QUẢ
    # =========================================================================

    stress_result = {

        "Scenario":
            scenario_name,

        "EAD":
            ead,

        "Base PD":
            base_pd,

        "Stressed PD":
            stressed_pd,

        "LGD":
            lgd,

        "Base NPL":
            base_npl,

        "Stressed NPL":
            stressed_npl,

        "Base EL":
            base_expected_loss,

        "Stressed EL":
            stressed_expected_loss,

        "Incremental Loss":
            incremental_loss,

        "Base CAR":
            base_car,

        "Stressed CAR":
            stressed_car,

        "Base Capital":
            capital,

        "Stressed Capital":
            stressed_capital
    }


    st.session_state[
        "stress_test_result"
    ] = stress_result


    # =========================================================================
    # DOWNLOAD RESULT
    # =========================================================================

    st.divider()

    st.subheader("Tải kết quả Stress Test")


    result_df = pd.DataFrame(
        stress_result.items(),
        columns=[
            "Chỉ tiêu",
            "Giá trị"
        ]
    )


    csv_data = result_df.to_csv(
        index=False
    ).encode(
        "utf-8-sig"
    )


    st.download_button(
        label="Tải kết quả CSV",
        data=csv_data,
        file_name="stress_test_result.csv",
        mime="text/csv",
        use_container_width=True
    )


    # =========================================================================
    # DISCLAIMER
    # =========================================================================

    st.caption(
        "Lưu ý: Kết quả Stress Test hiện tại được tính từ mô hình prototype "
        "và chỉ phục vụ mục đích xây dựng, thử nghiệm và minh họa dashboard."
    )





# =============================================================================
# TAB 6 - AI ANALYST
# =============================================================================

def tab6():

    st.title("AI Analysis")

    st.caption(
        "AI hỗ trợ diễn giải kịch bản và kết quả Stress Test, "
        "nhận diện các yếu tố rủi ro trọng yếu và tổng hợp nhận định quản trị."
    )

    st.divider()


    # =========================================================================
    # IMPORT GROQ
    # =========================================================================

    try:
        from groq import Groq

    except ImportError:

        st.error(
            "Chưa cài đặt thư viện Groq. "
            "Vui lòng chạy: python -m pip install groq"
        )

        return


    # =========================================================================
    # API KEY
    # =========================================================================

    try:

        api_key = st.secrets["GROQ_API_KEY"]

    except Exception:

        st.warning(
            "Chưa tìm thấy GROQ_API_KEY trong file "
            ".streamlit/secrets.toml"
        )

        return


    # =========================================================================
    # GROQ CLIENT
    # =========================================================================

    client = Groq(
        api_key=api_key
    )


    # =========================================================================
    # LOAD DATA FROM PREVIOUS TABS
    # =========================================================================

    scenario = st.session_state.get(
        "stress_scenario"
    )

    stress_result = st.session_state.get(
        "stress_test_result"
    )


    # =========================================================================
    # VALIDATE DATA
    # =========================================================================

    if scenario is None:

        st.warning(
            "Chưa có kịch bản Stress Test. "
            "Vui lòng thiết lập và lưu kịch bản tại tab "
            "'Kịch bản Stress Test' trước."
        )

        return


    if stress_result is None:

        st.warning(
            "Chưa có kết quả Stress Test. "
            "Vui lòng chạy Stress Test trước khi sử dụng AI Analysis."
        )

        return


    # =========================================================================
    # CURRENT ANALYSIS CONTEXT
    # =========================================================================

    st.subheader("Dữ liệu đầu vào cho AI")


    scenario_name = scenario.get(
        "Tên kịch bản",
        "Không xác định"
    )

    scenario_type = scenario.get(
        "Loại kịch bản",
        "Không xác định"
    )

    stress_level = scenario.get(
        "Stress Level",
        "Không xác định"
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Kịch bản",
            scenario_name
        )


    with c2:

        st.metric(
            "Loại kịch bản",
            scenario_type
        )


    with c3:

        st.metric(
            "Mức độ Stress",
            stress_level
        )


    st.caption(
        "AI sử dụng trực tiếp kịch bản và kết quả Stress Test "
        "đã được tạo tại các tab trước. AI không tính toán lại mô hình."
    )


    # =========================================================================
    # OPTIONAL DATA VIEW
    # =========================================================================

    with st.expander(
        "Xem dữ liệu AI đang sử dụng"
    ):

        st.markdown("#### Kịch bản vĩ mô")

        scenario_df = pd.DataFrame(
            scenario.items(),
            columns=[
                "Thông tin",
                "Giá trị"
            ]
        )

        st.dataframe(
            scenario_df,
            use_container_width=True,
            hide_index=True
        )


        st.markdown("#### Kết quả Stress Test")

        result_df = pd.DataFrame(
            stress_result.items(),
            columns=[
                "Chỉ tiêu",
                "Giá trị"
            ]
        )

        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True
        )


    st.divider()


    # =========================================================================
    # BUILD CONTEXT FOR AI
    # =========================================================================

    scenario_context = ""

    for key, value in scenario.items():

        scenario_context += (
            f"- {key}: {value}\n"
        )


    stress_context = ""

    for key, value in stress_result.items():

        if isinstance(
            value,
            (
                int,
                float,
                np.integer,
                np.floating
            )
        ):

            stress_context += (
                f"- {key}: {float(value):.4f}\n"
            )

        else:

            stress_context += (
                f"- {key}: {value}\n"
            )


    data_context = f"""
DỮ LIỆU ĐẦU VÀO

1. KỊCH BẢN STRESS TEST

{scenario_context}


2. KẾT QUẢ STRESS TEST

{stress_context}
"""


    # =========================================================================
    # SYSTEM PROMPT
    # =========================================================================

    system_prompt = """
Bạn là chuyên gia phân tích rủi ro tín dụng và Stress Testing
trong lĩnh vực ngân hàng tại Việt Nam.

Bạn đang hỗ trợ diễn giải kết quả Stress Test đã được tính toán
bởi một mô hình định lượng trong dashboard.

NGUYÊN TẮC:

1. Luôn trả lời bằng tiếng Việt.
2. Sử dụng văn phong chuyên nghiệp, rõ ràng và phù hợp báo cáo quản trị.
3. Không tính toán lại mô hình Stress Test.
4. Không thay đổi hoặc tự tạo số liệu.
5. Chỉ sử dụng dữ liệu được cung cấp.
6. Phân biệt rõ:
   - giả định kịch bản;
   - kết quả mô hình;
   - nhận định phân tích của AI.
7. Không khẳng định quan hệ nhân quả nếu dữ liệu không đủ để chứng minh.
8. Không đưa ra quyết định tín dụng thay cho người có thẩm quyền.
9. Nếu mô hình là prototype, phải xem kết quả là kết quả mô phỏng.
10. Ưu tiên phân tích:
    - PD;
    - NPL;
    - Expected Loss;
    - Capital;
    - CAR;
    - các yếu tố kinh tế vĩ mô có liên quan.

Mục tiêu của bạn là biến kết quả định lượng thành nhận định
có ý nghĩa đối với công tác quản trị rủi ro.
"""


    # =========================================================================
    # FUNCTION CALL AI
    # =========================================================================

    def run_ai_analysis(
        user_prompt
    ):

        try:

            response = (
            client
            .chat
            .completions
            .create(
                model="openai/gpt-oss-20b",
        
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": (
                            data_context
                            + "\n\n"
                            + user_prompt
                        )
                    }
                ],
        
                temperature=0.2,
                max_tokens=1800
            )
        )


            return (
                response
                .choices[0]
                .message
                .content
            )


        except Exception as e:

            st.error(
                "Không thể kết nối đến AI."
            )

            st.caption(
                str(e)
            )

            return None


    # =========================================================================
    # AI ANALYSIS TYPE
    # =========================================================================

    st.subheader("Phân tích tự động")


    analysis_type = st.selectbox(

        "Loại phân tích",

        [
            "Tổng quan điều hành",
            "Yếu tố rủi ro trọng yếu",
            "Phân tích tác động",
            "Đánh giá khả năng chịu đựng",
            "Chỉ tiêu cần giám sát",
            "Báo cáo tổng hợp"
        ],

        key="ai_analysis_type"
    )


    # =========================================================================
    # PROMPTS
    # =========================================================================

    prompts = {


        # ---------------------------------------------------------------------
        # EXECUTIVE SUMMARY
        # ---------------------------------------------------------------------

        "Tổng quan điều hành":
        """
Hãy viết phần tổng quan điều hành về kết quả Stress Test.

Cấu trúc:

1. Mức độ nghiêm trọng của kịch bản.
2. Các yếu tố vĩ mô đáng chú ý.
3. Những thay đổi quan trọng trong kết quả Stress Test.
4. Rủi ro trọng yếu đối với danh mục.
5. Kết luận ngắn gọn.

Yêu cầu:
- Viết ngắn gọn.
- Phù hợp để trình bày cho cấp quản lý.
- Không tạo thêm số liệu.
""",


        # ---------------------------------------------------------------------
        # RISK DRIVERS
        # ---------------------------------------------------------------------

        "Yếu tố rủi ro trọng yếu":
        """
Hãy xác định các yếu tố rủi ro vĩ mô trọng yếu trong kịch bản.

Phân tích các yếu tố sau nếu có dữ liệu:

- tăng trưởng GDP;
- lạm phát;
- lãi suất;
- tỷ giá;
- tăng trưởng tín dụng;
- thất nghiệp;
- VN-Index.

Với mỗi yếu tố:

1. Mô tả giả định trong kịch bản.
2. Giải thích chiều tác động tiềm năng đến rủi ro tín dụng.
3. Cho biết chỉ tiêu Stress Test nào có thể chịu ảnh hưởng.
4. Xác định yếu tố nào đáng chú ý nhất.

Không tạo số liệu mới.
""",


        # ---------------------------------------------------------------------
        # IMPACT
        # ---------------------------------------------------------------------

        "Phân tích tác động":
        """
Hãy diễn giải kết quả Stress Test.

Phân tích lần lượt:

1. PD trước và sau Stress.
2. NPL trước và sau Stress.
3. Expected Loss trước và sau Stress.
4. Mức tổn thất tăng thêm.
5. Vốn trước và sau Stress.
6. CAR trước và sau Stress.

Không tính lại các chỉ tiêu.

Giải thích ý nghĩa quản trị rủi ro của những thay đổi đã được mô hình tính toán.
""",


        # ---------------------------------------------------------------------
        # RESILIENCE
        # ---------------------------------------------------------------------

        "Đánh giá khả năng chịu đựng":
        """
Dựa trên kết quả Stress Test đã cung cấp,
hãy đánh giá khả năng chịu đựng của danh mục dưới kịch bản hiện tại.

Tập trung vào:

1. Mức tăng PD và NPL.
2. Mức tăng Expected Loss.
3. Mức suy giảm vốn.
4. Mức thay đổi CAR.
5. Các dấu hiệu cho thấy khả năng hấp thụ tổn thất suy giảm.

Không tự đặt ngưỡng pháp lý hoặc ngưỡng nội bộ nếu dữ liệu không cung cấp.

Kết luận theo góc độ:
- tương đối ổn định;
- cần theo dõi;
- chịu áp lực đáng kể;
- chịu áp lực rất cao.

Giải thích cơ sở của nhận định.
""",


        # ---------------------------------------------------------------------
        # MONITORING
        # ---------------------------------------------------------------------

        "Chỉ tiêu cần giám sát":
        """
Dựa trên kịch bản và kết quả Stress Test,
hãy đề xuất các nhóm chỉ tiêu cần được theo dõi.

Chia thành:

1. Chỉ tiêu kinh tế vĩ mô.
2. Chỉ tiêu chất lượng tín dụng.
3. Chỉ tiêu tổn thất tín dụng.
4. Chỉ tiêu vốn.
5. Chỉ báo cảnh báo sớm.

Đối với từng nhóm, giải thích tại sao cần theo dõi.

Không đưa ra quyết định tín dụng.
""",


        # ---------------------------------------------------------------------
        # FULL REPORT
        # ---------------------------------------------------------------------

        "Báo cáo tổng hợp":
        """
Hãy tạo một báo cáo phân tích Stress Test ngắn gọn với cấu trúc:

1. Tóm tắt điều hành
2. Mô tả kịch bản
3. Yếu tố rủi ro vĩ mô trọng yếu
4. Tác động đến PD và NPL
5. Tác động đến Expected Loss
6. Tác động đến vốn và CAR
7. Đánh giá khả năng chịu đựng
8. Chỉ tiêu cần theo dõi
9. Kết luận

Yêu cầu:
- Văn phong phù hợp báo cáo quản trị rủi ro ngân hàng.
- Không tạo thêm số liệu.
- Không tính toán lại mô hình.
"""
    }


    # =========================================================================
    # RUN AI
    # =========================================================================

    if st.button(
        "Phân tích bằng AI",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "AI đang phân tích kết quả Stress Test..."
        ):

            ai_result = run_ai_analysis(
                prompts[
                    analysis_type
                ]
            )


        if ai_result:

            st.session_state[
                "ai_analysis_result"
            ] = ai_result

            st.session_state[
                "ai_analysis_result_type"
            ] = analysis_type


    # =========================================================================
    # DISPLAY RESULT
    # =========================================================================

    if (
        "ai_analysis_result"
        in st.session_state
    ):

        st.divider()

        st.subheader(
            st.session_state.get(
                "ai_analysis_result_type",
                "Kết quả phân tích"
            )
        )


        with st.container(
            border=True
        ):

            st.markdown(
                st.session_state[
                    "ai_analysis_result"
                ]
            )


    # =========================================================================
    # CUSTOM ANALYSIS
    # =========================================================================

    st.divider()

    st.subheader(
        "Phân tích theo yêu cầu"
    )

    st.caption(
        "Đặt câu hỏi cụ thể dựa trên kịch bản và "
        "kết quả Stress Test hiện tại."
    )


    custom_question = st.text_area(

        "Nội dung cần phân tích",

        placeholder=(
            "Ví dụ: Hãy phân tích yếu tố nào có khả năng "
            "tạo áp lực lớn nhất lên chất lượng tín dụng."
        ),

        height=120,

        key="ai_custom_question"
    )


    if st.button(
        "Gửi yêu cầu phân tích",
        use_container_width=True
    ):

        if not custom_question.strip():

            st.warning(
                "Vui lòng nhập nội dung cần phân tích."
            )

        else:

            with st.spinner(
                "AI đang xử lý yêu cầu..."
            ):

                custom_result = run_ai_analysis(
                    custom_question
                )


            if custom_result:

                st.session_state[
                    "ai_custom_result"
                ] = custom_result


    # =========================================================================
    # CUSTOM RESULT
    # =========================================================================

    if (
        "ai_custom_result"
        in st.session_state
    ):

        st.markdown(
            "### Kết quả phân tích theo yêu cầu"
        )


        with st.container(
            border=True
        ):

            st.markdown(
                st.session_state[
                    "ai_custom_result"
                ]
            )


    # =========================================================================
    # RESET AI RESULT
    # =========================================================================

    st.divider()


    if st.button(
        "Xóa kết quả AI"
    ):

        st.session_state.pop(
            "ai_analysis_result",
            None
        )

        st.session_state.pop(
            "ai_analysis_result_type",
            None
        )

        st.session_state.pop(
            "ai_custom_result",
            None
        )

        st.rerun()


    # =========================================================================
    # DISCLAIMER
    # =========================================================================

    st.caption(
        "AI Analysis chỉ hỗ trợ diễn giải kết quả mô hình. "
        "Nội dung do AI tạo ra cần được rà soát trước khi sử dụng "
        "trong báo cáo hoặc quá trình ra quyết định."
    )



# =============================================================================
# MAIN APPLICATION
# =============================================================================

if menu == "Overview":
    tab0()

elif menu == "Macro Data":
    tab1()

elif menu == "Data Download":
    tab2()

elif menu == "Macro Analysis":
    tab3()

elif menu == "Stress Scenario":
    tab4()

elif menu == "Stress Test":
    tab5()

elif menu == "AI Analyst":
    tab6()