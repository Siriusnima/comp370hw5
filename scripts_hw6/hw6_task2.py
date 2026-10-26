from src.analysis import read_data, count_rodent_by_property

rows = read_data("data/311_records_2024_zipcode.csv")

property_counts = count_rodent_by_property(rows)

for property_type, descriptors in property_counts.items():

    print(f"\n{property_type}")

    for descriptor, count in descriptors.most_common():
        print(f"    {descriptor}: {count}")