
import argparse

from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    FactorRange
)
from bokeh.palettes import Category20

from src.analysis import (
    read_data,
    count_rodent_by_property
)


def create_dashboard(property_counts):

    # Sort property types by total complaint count
    property_types = sorted(
        property_counts,
        key=lambda location: sum(property_counts[location].values()),
        reverse=True
    )

    # Find all unique rodent descriptors
    descriptors = sorted({
        descriptor
        for counts in property_counts.values()
        for descriptor in counts
    })

    # Prepare data for the stacked bars
    data = {
        "property_type": property_types
    }

    total_counts = {}

    for property_type in property_types:
        total_counts[property_type] = sum(
            property_counts[property_type].values()
        )

    for descriptor in descriptors:
        data[descriptor] = [
            property_counts[property_type].get(descriptor, 0)
            for property_type in property_types
        ]

    source = ColumnDataSource(data=data)

    # Create the figure
    p = figure(
        title="NYC Rodent Complaints by Property Type (2024)",
        x_range=FactorRange(factors=property_types),
        width=1150,
        height=650,
        x_axis_label="Property Type",
        y_axis_label="Number of Rodent Complaints",
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )

    colors = [
        Category20[20][i % 20]
        for i in range(len(descriptors))
    ]

    # Draw stacked bars
    renderers = p.vbar_stack(
        stackers=descriptors,
        x="property_type",
        width=0.8,
        color=colors,
        source=source,
        legend_label=descriptors
    )

    # Add hover tool for each descriptor
    for descriptor, renderer in zip(descriptors, renderers):

        hover = HoverTool(
            renderers=[renderer],
            tooltips=[
                ("Property Type", "@property_type"),
                ("Descriptor", descriptor),
                ("Count", f"@{{{descriptor}}}{{0,0}}")
            ]
        )

        p.add_tools(hover)

    # Format chart
    p.xaxis.major_label_orientation = 0.8
    p.y_range.start = 0

    if p.legend:
        p.legend.location = "top_right"
        p.legend.click_policy = "hide"

    return column(p)


def main():

    parser = argparse.ArgumentParser(
        description="NYC Rodent Complaints Dashboard"
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input CSV file"
    )

    args = parser.parse_args()

    rows = read_data(args.input)

    property_counts = count_rodent_by_property(rows)

    dashboard = create_dashboard(property_counts)

    curdoc().add_root(dashboard)
    curdoc().title = "NYC Rodent Dashboard"


main()
