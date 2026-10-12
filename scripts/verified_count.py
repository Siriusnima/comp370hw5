
import csv
from datetime import datetime

# Input files
input_file = "data/311_records_2024_zipcode.csv"
results_file = "results.csv"

# Date range
start_date = datetime.strptime("2024-01-01", "%Y-%m-%d").date()
end_date = datetime.strptime("2024-02-09", "%Y-%m-%d").date()

# Step 1: Count matching records in the original CSV
original_count = 0

with open(input_file, "r", newline="") as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        created_date = datetime.strptime(
            row["Created Date"], "%m/%d/%Y %I:%M:%S %p"
        ).date()

        if start_date <= created_date <= end_date:
            original_count += 1

# Step 2: Add all counts from results.csv
result_count = 0

with open(results_file, "r", newline="") as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        result_count += int(row["Count"])

# Step 3: Compare the two totals
print("Original matching records:", original_count)
print("Sum of complaint counts:", result_count)

if original_count == result_count:
    print("PASS: The totals match!")
else:
    print("FAIL: The totals do not match!")
