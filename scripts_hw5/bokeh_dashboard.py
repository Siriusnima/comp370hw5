import csv

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import column, row

DATA_FILE = "data/monthly_Average_response.csv"

#Section 1: Read input file into monthly_cost
monthly_data = {}

with open(DATA_FILE, "r", newline="") as infile:
    reader = csv.DictReader(infile)

    for record in reader:
        zipcode = record["Incident Zip"]
        month = record["Created Month"]
        average = float(record["Average Hours"])

        if zipcode not in monthly_data:
            monthly_data[zipcode] = {}

        monthly_data[zipcode][month] = average

# Section 2: Create three ColumnDataSource objects for ALL, ZIP code 1, and ZIP code 2.
# Get the months in chronological order
months = sorted(monthly_data["ALL"].keys())

# Get available ZIP codes, excluding ALL
zipcodes = sorted(zipcode for zipcode in monthly_data if zipcode != "ALL")

# Choose two initial ZIP codes
zip1 = "10001"
zip2 = "10002"

# Function to retrieve monthly averages
def get_monthly_values(zipcode):
    return [monthly_data[zipcode].get(month, float("nan")) for month in months]

# Create data sources for the three lines
source_all = ColumnDataSource(data={
    "month": months,
    "hours": get_monthly_values("ALL")
})

source_zip1 = ColumnDataSource(data={
    "month": months,
    "hours": get_monthly_values(zip1)
})

source_zip2 = ColumnDataSource(data={
    "month": months,
    "hours": get_monthly_values(zip2)
})


# Section 3: plotting
# Create the figure
p = figure(
    title="NYC 311 Monthly Average Response Time (2024)",
    x_range=months,
    width=1000,
    height=500,
    x_axis_label="Created Month",
    y_axis_label="Average Response Time (Hours)"
)

# Plot the overall monthly average
p.line(
    x="month",
    y="hours",
    source=source_all,
    line_width=3,
    color="black",
    legend_label="ALL"
)

# Plot ZIP code 1
line_zip1 = p.line(
    x="month",
    y="hours",
    source=source_zip1,
    line_width=2,
    color="blue",
    legend_label=f"ZIP {zip1}"
)

# Plot ZIP code 2
line_zip2 = p.line(
    x="month",
    y="hours",
    source=source_zip2,
    line_width=2,
    color="red",
    legend_label=f"ZIP {zip2}"
)

# Format the plot
p.xaxis.major_label_orientation = 0.8
p.legend.location = "top_left"
p.legend.click_policy = "hide"

# Section 4: Create ZIP-code dropdowns
select1 = Select(
    title="ZIP Code 1",
    value=zip1,
    options=zipcodes
)

select2 = Select(
    title="ZIP Code 2",
    value=zip2,
    options=zipcodes
)

#Section 5: Update functions
def update_zip1(attr, old, new):
    source_zip1.data = {
        "month": months,
        "hours": get_monthly_values(new)
    }
    p.legend.items[1].label = {"value": f"ZIP {new}"}

def update_zip2(attr, old, new):
    source_zip2.data = {
        "month": months,
        "hours": get_monthly_values(new)
    }
    p.legend.items[2].label = {"value": f"ZIP {new}"}

select1.on_change("value", update_zip1)
select2.on_change("value", update_zip2)

layout = column(
    row(select1, select2),
    p
)

curdoc().add_root(layout)
curdoc().title = "NYC 311 Response Time Dashboard"