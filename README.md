# UAC System Capacity & Care Load Analytics

An interactive data analytics dashboard for monitoring the
Unaccompanied Alien Children (UAC) care pipeline managed by
the U.S. Department of Health & Human Services.

## Live Dashboard
[View on Streamlit Cloud](YOUR_STREAMLIT_URL_HERE)

## Project Structure
unaccompanied-children-analytics/
├── data/
│   └── hhs_data.csv
├── notebooks/
│   ├── eda.py
│   └── test_*.py
├── src/
│   ├── data_loader.py
│   ├── features.py
│   ├── trends.py
│   ├── kpis.py
│   ├── charts.py
│   └── filter_data.py
├── pages/
│   ├── 01_overview.py
│   ├── 02_cbp_hhs.py
│   └── 03_intake_backlog.py
├── app.py
├── requirements.txt
├── research_paper.md
└── executive_summary.md

## Key Findings
- Peak crisis: 11,516 children in HHS care (Dec 20, 2023)
- 78.4% reduction from peak to current (Dec 2025)
- Discharge Offset Ratio: 1.35x across full timeline
- 180 high-stress days (25% of all reporting days)

## Tech Stack
Python | Pandas | Plotly | Streamlit

## Setup
pip install -r requirements.txt
streamlit run app.py

## Author
Sarthak | MCA, Amity University Jaipur
Unified Mentor AI Internship