# Macro Stress Testing Dashboard

link dashboard:
https://stress-test-ntc.streamlit.app/

A **Streamlit-based macroeconomic stress testing and credit risk analytics dashboard** designed to monitor macroeconomic conditions, develop stress scenarios, assess potential impacts on credit risk, and support result interpretation using AI.

The dashboard provides an integrated analytical environment combining **macroeconomic data, scenario analysis, stress testing, visualization, and AI-assisted analytics**.

## Key Features

### Macroeconomic Data

Monitor and visualize key macroeconomic indicators, including:

* GDP growth
* Inflation
* Interest rates
* Credit growth
* Unemployment
* External sector indicators
* Other macro-financial variables

### Data Download

Build customized macroeconomic datasets by selecting:

* Countries
* Economic indicators
* Time periods
* Data frequency

Datasets can be exported to **CSV or Excel** for further analysis.

### Macro Analysis

Analyze macroeconomic conditions through:

* Historical trend analysis
* Descriptive statistics
* Volatility analysis
* Correlation analysis
* Relationships between macroeconomic variables

### Stress Scenarios

Develop and compare multiple macroeconomic scenarios:

* Baseline
* Adverse
* Severely Adverse
* Custom Scenario

These scenarios provide macroeconomic shocks used as inputs for stress testing.

### Stress Testing

Estimate the potential impact of adverse macroeconomic conditions on key credit risk and capital indicators, including:

* Probability of Default (PD)
* Non-Performing Loan Ratio (NPL)
* Expected Loss (EL)
* Capital
* Capital Adequacy Ratio (CAR)

### AI Analysis

AI-assisted analytics support the interpretation of macroeconomic conditions and stress testing results by:

* Summarizing stress test results
* Identifying key macroeconomic risk drivers
* Interpreting potential credit risk impacts
* Highlighting vulnerabilities
* Suggesting key indicators for monitoring
* Supporting executive-level risk summaries

## Data Sources

The dashboard primarily uses publicly available macroeconomic and financial data sources, including:

* World Bank Indicators API
* Additional macroeconomic and financial market data sources can be integrated in future versions

## Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* Plotly
* Requests
* OpenPyXL
* Groq API
* World Bank API

## Project Structure

```text
Macro_VB/
│
├── app.py
├── requirements.txt
├── vietbank_logo.png
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

## Use Cases

The dashboard is designed to support:

* Macroeconomic risk monitoring
* Identification of key macroeconomic risk drivers
* Development and comparison of stress scenarios
* Assessment of potential credit portfolio deterioration
* Evaluation of credit risk and capital impacts
* Stress testing and scenario-based risk analysis
* AI-assisted interpretation of analytical results
* Risk management reporting and decision support

## Disclaimer

This dashboard is currently developed as an **analytical prototype**.

Stress testing models, assumptions, coefficients, and scenario parameters should be properly calibrated and validated using relevant historical and portfolio data before being used for official risk management or decision-making purposes.

AI-generated analysis is intended to support analytical workflows and should be reviewed by qualified professionals before being used in formal reports or decisions.

