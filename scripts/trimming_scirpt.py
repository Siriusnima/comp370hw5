import csv

input_file = "data/311_Service_Requests_from_2010_to_Present_20250928.csv"
output_file = "data/311_records_2024_zipcode.csv"

with open(input_file, "r", newline="") as infile, \
     open(output_file, "w", newline="") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        created_date = row[1]
        zipcode = row[8]

        if "/2024" in created_date and zipcode.strip() != "": #check the year 2024 and zipcode
            writer.writerow(row)