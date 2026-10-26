# calculate response time in each zipcode

import csv
from datetime import datetime

input_file = "data/311_records_2024_zipcode.csv"
output_file = "data/response_times.csv"

with open(input_file, "r", newline="") as infile, \
     open(output_file, "w", newline="") as outfile:

    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)

    writer.writerow(["Incident Zip", "Created Month", "Response Hours"])

    for row in reader:
        created = row["Created Date"]
        closed = row["Closed Date"]
        zipcode = row["Incident Zip"].strip()

        if not closed.strip() or not zipcode:
            continue

        created_date = datetime.strptime(
            created, "%m/%d/%Y %I:%M:%S %p"
        )

        closed_date = datetime.strptime(
            closed, "%m/%d/%Y %I:%M:%S %p"
        )

        response_hours = (
            closed_date - created_date
        ).total_seconds() / 3600

        if response_hours < 0:
            continue

        created_month = created_date.strftime("%Y-%m")

        writer.writerow([zipcode, created_month, response_hours])