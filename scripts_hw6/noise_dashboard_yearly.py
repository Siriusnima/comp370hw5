
import calendar
import argparse

from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    Range1d
)
from bokeh.palettes import Category20

from src.analysis import (
    read_data,
    count_noise_month,
    calculate_noise_percentage
)


def create_dashboard(monthly_counts, percentages):

    p = figure(
        title="NYC Noise Complaints by Month (2024)",
        width=1100,
        height=600,
        x_range=Range1d(0.5, 12.5),
        y_range=Range1d(0, 100),
        x_axis_label="Month",
        y_axis_label="Percentage of Monthly Noise Complaints (%)",
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )

    # Display January through December
    p.xaxis.ticker = list(range(1, 13))

    p.xaxis.major_label_overrides = {
        month: calendar.month_abbr[month]
        for month in range(1, 13)
    }

    # Collect all unique descriptors appearing
    # in the monthly top 10 during 2024
    descriptors = []

    for month in range(1, 13):
        for descriptor in percentages.get(month, {}):
            if descriptor not in descriptors:
                descriptors.append(descriptor)

    # Store scatter renderers for hover
    points = []

    # Draw a line for each descriptor
    for i, descriptor in enumerate(descriptors):

        x_values = []
        month_names = []
        percentage_values = []
        count_values = []

        for month in range(1, 13):

            x_values.append(month)
            month_names.append(
                calendar.month_name[month]
            )

            percentage_values.append(
                percentages.get(month, {}).get(
                    descriptor,
                    float("nan")
                )
            )

            count_values.append(
                monthly_counts.get(month, {}).get(
                    descriptor, 0
                )
            )

        source = ColumnDataSource(data={
            "x": x_values,
            "month": month_names,
            "percentage": percentage_values,
            "count": count_values,
            "descriptor": [descriptor] * 12
        })

        color = Category20[20][i % 20]

        p.line(
            x="x",
            y="percentage",
            source=source,
            line_width=2,
            color=color,
            legend_label=descriptor
        )

        point = p.scatter(
            x="x",
            y="percentage",
            source=source,
            size=7,
            color=color
        )

        points.append(point)

    # Show details when hovering over a point
    hover = HoverTool(
        renderers=points,
        tooltips=[
            ("Descriptor", "@descriptor"),
            ("Month", "@month"),
            ("Count", "@count{0,0}"),
            ("Percentage", "@percentage{0.00}%")
        ],
        mode="mouse"
    )

    p.add_tools(hover)

    # Legend settings
    if p.legend:
        legend = p.legend[0]
        legend.location = "top_left"
        legend.click_policy = "hide"
        p.add_layout(legend, "right")

    return column(p)


def main():

    parser = argparse.ArgumentParser(
        description="NYC Noise Complaints Dashboard"
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input CSV file"
    )

    args = parser.parse_args()

    rows = read_data(args.input)

    monthly_counts = count_noise_month(rows)

    percentages = calculate_noise_percentage(
        monthly_counts
    )

    dashboard = create_dashboard(
        monthly_counts,
        percentages
    )

    curdoc().add_root(dashboard)
    curdoc().title = "NYC Noise Dashboard"


main()
