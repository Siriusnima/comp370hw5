# COMP370 – Homework 5

## Project Description

This project analyzes New York City 311 service request data to investigate complaint patterns and response times.

The project uses Python for data processing and Bokeh to create an interactive dashboard for visualizing service request trends.

## Project Structure

```text
HW5/
├── data/
│   └── monthly_response.csv
├── scripts/
│   └── dashboard.py
├── src/
├── README.md
└── .gitignore
```

## Requirements

- Python 3
- pandas
- Bokeh

Install the required packages:

```bash
pip install pandas bokeh
```

## Dataset

The project uses NYC 311 service request records.

The dataset contains information such as:

- Complaint creation and closing dates
- Complaint types
- Boroughs
- Incident ZIP codes
- Service response times

The data is processed to examine complaint trends and response times.

## Running the Dashboard

Navigate to the project directory:

```bash
cd HW5
```

Start the Bokeh server:

```bash
bokeh serve scripts/dashboard.py
```

Open the following URL in your browser:

```text
http://localhost:5006/dashboard
```

The dashboard will be displayed in your browser.

Alternatively, launch the dashboard automatically:

```bash
bokeh serve scripts/dashboard.py --show
```

## Dashboard Features

The interactive dashboard provides:

1. **Monthly Response Time Visualization** – Displays monthly service response time trends.
2. **Data Filtering** – Allows users to explore data using available dashboard controls.
3. **Multiple Data Series** – Supports comparisons between different data selections.
4. **2020 Data Overview** – Includes an "All 2020 Data" series that remains visible for comparison.
5. **Interactive Visualization** – Uses Bokeh for interactive plots.

## Implementation

### Data Processing

Python is used to read and process CSV files containing NYC 311 service request data.

The processed data is organized for visualization and analysis.

### Bokeh Dashboard

The `dashboard.py` script creates the interactive visualization using Bokeh.

The dashboard loads the processed CSV data, generates plots, and updates the visualization based on user selections.

### File Paths

The dashboard constructs data file paths relative to the script location:

```python
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    current_dir,
    "../data/monthly_response.csv"
)
```

This allows the script to locate the dataset without requiring an absolute file path.

## Notes

- The dashboard requires the processed CSV file to be available in the `data/` directory.
- The Bokeh server must be running to access the dashboard.
- Missing or invalid records should be handled during data preprocessing.
- The project structure and input filenames may need adjustment depending on the final implementation.