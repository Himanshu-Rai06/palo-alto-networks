# Employee Engagement, Satisfaction & Burnout Diagnostic Analysis
### Palo Alto Networks — HR Analytics Project

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://palo-alto-networks-dashboard.streamlit.app/)
&nbsp;
[![ResearchGate](https://img.shields.io/badge/ResearchGate-Paper-00CCBB?logo=researchgate&logoColor=white)](https://www.researchgate.net/publication/409281248_Employee_Engagement_Satisfaction_and_Burnout_Diagnostic_Analysis_at_Palo_Alto_Networks)
&nbsp;
[![DOI](https://img.shields.io/badge/DOI-10.13140%2FRG.2.2.26940.81286-blue)](https://doi.org/10.13140/RG.2.2.26940.81286)
&nbsp;
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
&nbsp;
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

This project presents a preventive HR analytics diagnostic for Palo Alto Networks, shifting the organisational approach from **reactive attrition reporting** to **early-warning employee experience monitoring**. Rather than explaining why employees have already left, five composite KPIs are engineered directly from raw workforce data to detect disengagement and burnout risk before departure decisions are made.

The analysis is conducted on a structured dataset of **1,470 employees across 31 features**, with zero missing values. Fifteen empirical findings are documented, and all KPIs are validated against the `Attrition` outcome variable.

**The central finding:** The most overloaded employees simultaneously report the highest engagement scores and the highest attrition rates — a pattern invisible to conventional engagement surveys, termed the **Bright Burn phenomenon**.

---

## Live Links

| Resource | Link |
|---|---|
| 🚀 Interactive Dashboard | [palo-alto-networks-dashboard.streamlit.app](https://palo-alto-networks-dashboard.streamlit.app/) |
| 📄 Research Paper (ResearchGate) | [doi.org/10.13140/RG.2.2.26940.81286](https://doi.org/10.13140/RG.2.2.26940.81286) |
| 💻 GitHub Repository | [github.com/Himanshu-Rai06/palo-alto-networks](https://github.com/Himanshu-Rai06/palo-alto-networks) |

---

## Repository Structure

```
palo-alto-networks/
│
├── app.py                                        # Streamlit dashboard (4 modules)
├── Palo_Alto_Networks.csv                        # Source dataset (1,470 employees, 31 columns)
├── Palo_Alto_Networks_HR_Analytics_Diagnostic.pptx  # Executive summary presentation
├── requirements.txt                              # Python dependencies
└── README.md
```

---

## The Five KPIs

All five indicators are engineered from scratch — none exist in the raw dataset.

| # | KPI | Construction | Key Finding |
|---|---|---|---|
| 1 | **Engagement Index** | Mean of 4 normalised satisfaction dimensions | Leavers score 14.2% lower than stayers |
| 2 | **Burnout Risk Score** | Rule-based: overtime, WLB, engagement, travel | High-risk employees leave at 4× the rate of low-risk |
| 3 | **Work-Life Balance Index** | Raw `WorkLifeBalance` column (1–4), disaggregated | WLB=4 ("Best") has *higher* attrition than WLB=3 |
| 4 | **Satisfaction Stability Score** | Std. deviation across 4 satisfaction dimensions | Modest signal; treated as supplementary indicator |
| 5 | **Workload Stress Indicator** | Weighted: (3×overtime) + travel + long commute flag | High-stress employees leave at 31.5%; r = 0.278 |

---

## Key Findings at a Glance

- **73.4%** of employees sit in the Medium engagement tier — quietly coasting, not thriving
- Employees working overtime leave at **30.5%** vs **10.4%** for non-overtime employees (nearly 3×)
- Combining frequent travel *and* overtime elevates attrition to **41.9%** — a multiplicative stress interaction, not additive
- New employees (0–2 yr tenure) leave at **29.8%** — 3.7× the rate of senior employees — despite near-average engagement scores
- The **Danger Zone** (High Burnout + Low Engagement): 11 employees, **54.5% attrition** — the highest rate of any segment
- The **Bright Burn paradox**: Workload Stress Score 6 employees → Engagement Index 0.635 (highest) → Attrition 50.0% (highest)

---

## Dashboard Modules

The Streamlit app (`app.py`) is structured into four tabs, with a global sidebar filter (department, role, overtime toggle, engagement threshold, tenure range):

| Tab | Module | What It Shows |
|---|---|---|
| 🟢 | **Engagement Health** | Org-wide engagement gauge, tier donut, attrition by tier, satisfaction radar (stayed vs left), department breakdown |
| 🔴 | **Burnout Risk** | Burnout tier KPIs, attrition by tier, burnout by job role, overtime comparison, WLB chart, Travel × Overtime heatmap, Engagement-Stress Paradox dual-axis chart |
| 📈 | **Role & Career Stage** | Engagement by job role and level, attrition by tenure band, scatter of tenure vs engagement, promotion stagnation curve, years in role analysis |
| 🎯 | **Manager Action Panel** | Priority intervention table (Critical / High / Medium / Monitor), low-engagement alerts by department, recommended actions by timeframe, raw data explorer |

---

## Running Locally

**Requirements:** Python 3.10+

```bash
# 1. Clone the repository
git clone https://github.com/Himanshu-Rai06/palo-alto-networks.git
cd palo-alto-networks

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run app.py
```

The app expects `Palo_Alto_Networks.csv` in the same directory as `app.py`.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Pandas, NumPy | Data processing and KPI engineering |
| Plotly | Interactive visualisations |
| Streamlit ≥ 1.49 | Dashboard framework and deployment |
| Google Colaboratory | Exploratory data analysis and modelling |
| LaTeX | Research paper typesetting |

---

## Research Paper

The full analysis is documented in a peer-reviewed research paper published on ResearchGate.

> Rai, H. (2025). *Employee engagement, satisfaction, and burnout diagnostic analysis at Palo Alto Networks: From reactive attrition analysis to preventive employee experience diagnostics.* DOI: [10.13140/RG.2.2.26940.81286](https://doi.org/10.13140/RG.2.2.26940.81286)

The paper covers:
- Six-step methodology (validation → KPI engineering → analysis)
- Fifteen numbered empirical findings with supporting tables
- Related work situating the study within HR analytics literature
- Department-, role-, and career-stage-level analysis
- Evidence-based recommendations across three timeframes (0–3 months, 3–12 months, 12+ months)

---

## Author

**Himanshu Rai**
Data Science Intern | B.Sc. Data Science (2nd → 3rd Year)

[![GitHub](https://img.shields.io/badge/GitHub-Himanshu--Rai06-181717?logo=github)](https://github.com/Himanshu-Rai06)

---

## Acknowledgements

The dataset pertaining to Palo Alto Networks workforce records was made available through the internship organisation that facilitated this project. All analyses were independently conducted by the author.

---

*This project is part of a Data Analytics Internship Programme. All findings are associative and descriptive in nature; no causal claims are made.*
