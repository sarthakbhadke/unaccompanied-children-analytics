# System Capacity & Care Load Analytics for Unaccompanied Children
**Author:** Sarthak | MCA, Amity University Jaipur  
**Internship:** Unified Mentor | AI & Data Analytics  
**Dataset:** U.S. Department of Health & Human Services — UAC Program (2023–2025)

---

## Abstract
This paper presents a data-driven analytical framework for monitoring
the Unaccompanied Alien Children (UAC) care pipeline managed by the
U.S. Department of Health & Human Services. Using daily operational
data spanning January 2023 to December 2025 (720 reporting days),
we quantify care system load, identify periods of capacity strain,
and evaluate the balance between intake and discharge flows.

---

## 1. Introduction
The UAC Program is a federally mandated initiative in which children
apprehended at the U.S. border are transferred from CBP custody to
HHS care facilities for medical screening, shelter, and sponsor
placement. Effective management requires continuous situational
awareness of system load, intake pressure, and discharge capacity.

This study addresses the absence of a centralized analytical
framework by building a structured analytics pipeline and interactive
dashboard using Python, Pandas, Plotly, and Streamlit.

---

## 2. Dataset Description
| Attribute | Detail |
|-----------|--------|
| Source | U.S. Department of Health & Human Services |
| Date range | January 12, 2023 – December 21, 2025 |
| Raw rows | 1,170 (450 empty, 720 valid) |
| Columns | 6 (Date + 5 operational metrics) |
| Granularity | Daily reporting |

### 2.1 Columns
- **Date** — Reporting date
- **CBP Apprehended** — Daily new intake into CBP custody
- **CBP In Custody** — Active CBP care load
- **CBP Transferred** — Daily flow into HHS system
- **HHS In Care** — Active HHS care load
- **HHS Discharged** — Daily sponsor placements

---

## 3. Methodology

### 3.1 Data Cleaning
- Removed 450 completely empty rows
- Converted date strings to datetime format
- Removed comma formatting from numeric fields
- Sorted chronologically (oldest to newest)
- Validated zero missing values post-cleaning

### 3.2 Feature Engineering
Six derived metrics were computed:
1. **Total System Load** = CBP Custody + HHS Care
2. **Net Daily Intake** = CBP Transferred − HHS Discharged
3. **Care Load Growth Rate** = Day-over-day % change in HHS care
4. **7-Day Rolling Average** = Smoothed HHS care trend
5. **7-Day Rolling Net Intake** = Smoothed pressure indicator
6. **Cumulative Backlog** = Running total of net daily intake

### 3.3 Trend Analysis
Data was resampled to weekly and monthly frequencies using
Pandas resample(). Stress periods were identified as days
exceeding the 75th percentile of HHS care load (threshold: 8,010).

---

## 4. Key Findings

### 4.1 Crisis Peak — December 2023
The system reached its maximum care load of **11,516 children**
on December 20, 2023. The entire top-5 highest care load days
occurred in December 2023, indicating a sustained crisis rather
than a single-day anomaly. Total system load including CBP custody
peaked at 11,762 on the same date.

### 4.2 Intake Surge — February 2024
Despite declining HHS care load from January 2024, CBP apprehensions
peaked in February 2024 with 333 children apprehended in a single day
(February 15, 2024). This indicates the pipeline was still receiving
high volumes even as HHS worked to discharge the existing population.

### 4.3 System Collapse — Early 2025
HHS care load underwent a dramatic contraction beginning January 2025:
- January 2025 avg: 4,991
- February 2025 avg: 2,782
- March 2025 avg: 2,165

This 78.4% reduction from peak represents the fastest sustained
decline in the dataset, driven primarily by reduced CBP transfers
rather than increased discharges.

### 4.4 Balance Analysis
| Year | Transfers In | Discharges | Net Pressure |
|------|-------------|------------|--------------|
| 2023 | 36,124 | 66,244 | −30,120 |
| 2024 | 52,552 | 51,689 | +863 |
| 2025 | 3,965 | 6,920 | −2,955 |

The Discharge Offset Ratio of **1.35** across the full timeline
indicates the system discharged 35% more children than it received —
a net positive humanitarian outcome.

### 4.5 Stress Period Analysis
- 180 high-stress days (25% of all reporting days)
- All concentrated in the period August 2023 – January 2024
- Stress threshold: 8,010 children (75th percentile)

---

## 5. Dashboard
An interactive Streamlit dashboard was developed with three analytical
modules:
1. **System Overview** — KPI cards + care load timeline
2. **CBP vs HHS Comparison** — Dual-axis pipeline analysis
3. **Intake & Backlog Trends** — Pressure and relief visualization

Key dashboard features:
- Date range filtering
- Time granularity toggle (Daily / Weekly / Monthly)
- 7-day rolling average overlay
- Expandable raw data tables

---

## 6. Recommendations
1. **Early warning threshold:** Flag when HHS care load exceeds
   8,000 children for proactive resource allocation
2. **Discharge acceleration:** During high-intake months, prioritize
   sponsor matching to prevent backlog accumulation
3. **Seasonal planning:** August–December shows historically elevated
   intake — staff and shelter capacity should be pre-positioned
4. **Pipeline monitoring:** CBP-to-HHS transfer lag should be
   monitored — extended CBP custody indicates HHS capacity constraints

---

## 7. Conclusion
This analytical framework demonstrates that structured data analytics
can transform raw operational counts into actionable capacity insights.
The UAC care system experienced a full crisis arc from 2023 to 2025 —
from peak overload to rapid contraction. Continuous monitoring using
the developed dashboard enables data-driven, proactive humanitarian
response.

---

## References
- U.S. Department of Health & Human Services, Office of Refugee
  Resettlement — UAC Program Data
- Python Software Foundation — Pandas, Plotly, Streamlit documentation