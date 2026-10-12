import csv

input_file = "data/311_records_2024.csv"
output_file = "data/311_records_2024_zipcode.csv"

with open(input_file, "r", newline="") as infile, \
     open(output_file, "w", newline="") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        if row[8].strip() != "":
            writer.writerow(row)