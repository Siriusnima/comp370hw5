import calendar
import argparse

from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    Button,
    Div,
    Range1d
)
from bokeh.palettes import Category20

from src.analysis import (
    read_data,
    count_noise_month,
    calculate_noise_percentage
)


def create_dashboard(monthly_counts, percentages):

    seasons = [
        ("Winter", [1, 2, 3]),
        ("Spring", [4, 5, 6]),
        ("Summer", [7, 8, 9]),
        ("Fall", [10, 11, 12])
    ]

    current_season = 0

    season_label = Div(
        text="<h2>Winter: January - March</h2>"
    )

    p = figure(
        title="NYC Noise Complaints by Season (2024)",
        width=1050,
        height=550,
        x_range=Range1d(0.5, 3.5),
        y_range=Range1d(0, 100),
        x_axis_label="Month",
        y_axis_label="Percentage of Monthly Noise Complaints (%)",
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )

    p.xaxis.ticker = [1, 2, 3]

    hover = HoverTool(
        tooltips=[
            ("Descriptor", "@descriptor"),
            ("Month", "@month"),
            ("Count", "@count{0,0}"),
            ("Percentage", "@percentage{0.00}%")
        ],
        mode="mouse"
    )

    p.add_tools(hover)

    previous_button = Button(
        label="Previous Season",
        button_type="default",
        width=150
    )

    next_button = Button(
        label="Next Season",
        button_type="primary",
        width=150
    )

    def update_chart(season_index):

        # Remove existing plotted lines and legends
        p.renderers = []
        p.legend.items = []

        season_name, months = seasons[season_index]

        season_label.text = (
            f"<h2>{season_name}: "
            f"{calendar.month_name[months[0]]} - "
            f"{calendar.month_name[months[-1]]}</h2>"
        )

        # Find all descriptors that appear in the
        # monthly top 10 for this season
        descriptors = []

        for month in months:
            for descriptor in percentages.get(month, {}):
                if descriptor not in descriptors:
                    descriptors.append(descriptor)

        # Plot each descriptor across the three months
        for i, descriptor in enumerate(descriptors):

            x_values = []
            month_names = []
            percentage_values = []
            count_values = []

            for position, month in enumerate(months, start=1):

                x_values.append(position)
                month_names.append(calendar.month_name[month])

                percentage_values.append(
                    percentages.get(month, {}).get(
                        descriptor, float("nan")
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
                "descriptor": [descriptor] * 3
            })

            color = Category20[20][i % 20]

            line = p.line(
                x="x",
                y="percentage",
                source=source,
                line_width=2,
                color=color,
                legend_label=descriptor
            )

            p.scatter(
                x="x",
                y="percentage",
                source=source,
                size=7,
                color=color
            )

        p.xaxis.major_label_overrides = {
            1: calendar.month_name[months[0]],
            2: calendar.month_name[months[1]],
            3: calendar.month_name[months[2]]
        }

        p.legend.location = "top_left"
        p.legend.click_policy = "hide"

        if p.legend:
            p.add_layout(p.legend[0], "right")

    def next_season():
        nonlocal current_season

        current_season = (current_season + 1) % 4
        update_chart(current_season)

    def previous_season():
        nonlocal current_season

        current_season = (current_season - 1) % 4
        update_chart(current_season)

    next_button.on_click(next_season)
    previous_button.on_click(previous_season)

    update_chart(current_season)

    return column(
        season_label,
        p,
        row(previous_button, next_button)
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input CSV file"
    )

    args = parser.parse_args()

    rows = read_data(args.input)

    monthly_counts = count_noise_month(rows)

    percentages = calculate_noise_percentage(monthly_counts)

    dashboard = create_dashboard(
        monthly_counts,
        percentages
    )

    curdoc().add_root(dashboard)
    curdoc().title = "NYC Noise Dashboard"


main()