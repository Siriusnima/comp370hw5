
import csv

input_file = "data/response_times.csv"
output_file = "data/monthly_Average_response.csv"

monthly_totals = {}
zipcode_totals = {}

with open(input_file, "r", newline="") as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        zipcode = row["Incident Zip"]
        month = row["Created Month"]
        hours = float(row["Response Hours"])

        # All ZIP codes combined
        if month not in monthly_totals:
            monthly_totals[month] = [0, 0]

        monthly_totals[month][0] += hours
        monthly_totals[month][1] += 1

        # Each ZIP code separately
        key = (zipcode, month)

        if key not in zipcode_totals:
            zipcode_totals[key] = [0, 0]

        zipcode_totals[key][0] += hours
        zipcode_totals[key][1] += 1

with open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Incident Zip", "Created Month", "Average Hours"])

    for month, (total, count) in sorted(monthly_totals.items()):
        writer.writerow(["ALL", month, total / count])

    for (zipcode, month), (total, count) in sorted(zipcode_totals.items()):
        writer.writerow([zipcode, month, total / count])
