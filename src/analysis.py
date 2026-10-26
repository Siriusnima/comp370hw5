import csv
import calendar
from collections import Counter, defaultdict
from datetime import datetime



def read_data(filepath):
    with open(filepath, "r", encoding = "utf-8-sig", newline = "") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            yield row

def count_by_category(rows, category):
    count = 0

    for row in rows:
        if row["Complaint Type"] == category:
            count += 1

    return count

def count_noise_types(rows):
    counts = Counter()

    for row in rows:
        complaint = row["Complaint Type"]

        if not complaint.startswith("Noise"):
            continue
        counts[complaint] += 1
        
    return counts

def count_noise_month(rows):
    counts = defaultdict(Counter)

    for row in rows:
        complaint = row ["Complaint Type"]

        if not complaint.startswith("Noise"):
            continue
        
        date = datetime.strptime(
            row["Created Date"],
            "%m/%d/%Y %I:%M:%S %p"
        )

        if date.year != 2024:
            continue

        month = date.month
        descriptor = row["Descriptor"].strip()

        if not descriptor:
            descriptor = "Unspecified"

        counts[month][descriptor] += 1

    return counts

def write_noise_csv(monthly_counts, output_file):
    with open(output_file, "w", newline ="", encoding = "utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Month", "Descriptor", "Count"])

        for month in sorted(monthly_counts):
            for descriptor, count in monthly_counts[month].most_common():
                writer.writerow([calendar.month_name[month], descriptor, count])


def calculate_noise_percentage(monthly_counts):
    percentages = {}

    for month, complaints in monthly_counts.items():
        total = sum(complaints.values())

        percentages[month] = {}

        for descriptor, count in complaints.most_common(10):
            if total > 0:
                percentage = count / total * 100
            else:
                percentage = 0

            percentages[month][descriptor] = percentage

    return percentages

def count_rodent_location(rows):
    counts = Counter()

    for row in rows:
        if row["Complaint Type"].strip() == "Rodent":
            location = row["Location Type"].strip()

            if location == "":
                location = "Unknown"

            counts[location] += 1

    return counts

def count_rodent_by_property(rows):

    counts = defaultdict(Counter)

    for row in rows:

        complaint = row["Complaint Type"].strip()

        if complaint != "Rodent":
            continue

        property_type = row["Location Type"].strip()
        descriptor = row["Descriptor"].strip()

        if not property_type:
            property_type = "Unknown"

        if not descriptor:
            descriptor = "Unspecified"

        counts[property_type][descriptor] += 1

    return counts