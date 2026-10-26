from collections import Counter
from src.analysis import read_data

rows = read_data("data/311_records_2024_zipcode.csv")

descriptors = Counter()

for row in rows:
    if row["Complaint Type"].strip() == "Rodent":
        descriptor = row["Descriptor"].strip()
        descriptors[descriptor] += 1

for descriptor, count in descriptors.most_common():
    print(descriptor, count)