import argparse
import csv
from datetime import datetime
import sys

# Step 1: define command-line arguments
parser =  argparse.ArgumentParser(
    description = "Count complaint types by borough within a date range."
)

parser.add_argument("-i", required = True, help = "Input CSV file")
parser.add_argument("-s", required = True, help = "Start date (YYYY-MM-DD)")
parser.add_argument("-e", required = True, help = "End date (YYYY-MM-DD)")
parser.add_argument("-o", help = "Output CSV file (optional)")

args = parser.parse_args()


# Step 2: get input file name and convert date
input_file = args.i
start_date = datetime.strptime(args.s, "%Y-%m-%d").date() # strptime() converts the text into a Python date/time object
end_date = datetime.strptime(args.e, "%Y-%m-%d").date()

# Step 3: Create a dictionary to store counts
counts = {}

# Step 4: Read the CSV file one record at a time
with open(input_file, "r", newline = "") as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        created_date = datetime.strptime(
            row["Created Date"], "%m/%d/%Y %I:%M:%S %p"
        ).date()

        # Step 5: keep the complaint date within specific date range
        if start_date <= created_date <= end_date:
            borough = row["Borough"]
            complaint_type = row["Complaint Type"]
            
            # Step 6: Count complaints by borough and type
            key = (borough, complaint_type)
            counts[key] = counts.get(key, 0) + 1
# Step 7: Print the counts or export output csv file
if args.o:
    outfile =  open(args.o, "w", newline = "")
else:
    outfile = sys.stdout

writer = csv.writer(outfile)
writer.writerow(["Borough", "Complaint Type", "Count"])

for (borough, complaint_type), count in counts.items():
        writer.writerow([borough, complaint_type, count])

if args.o:
    outfile.close()
          
            # print(row["Borough"], row["Complaint Type"])  test codes, commented when done
            # break

#print(args)