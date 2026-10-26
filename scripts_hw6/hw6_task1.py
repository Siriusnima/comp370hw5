import argparse
import calendar

from src.analysis import read_data, count_noise_month, write_noise_csv

def main():
    parser = argparse.ArgumentParser(
        description = "Analyze NYC 311 noise complaints by month in 2024"
    )

    parser.add_argument(
        "-i",
        "--input",
        required = True,
        help = "Path to the input CSV file"
    )

    parser.add_argument(
        "-o",
        "--output",
        default = None,
        help = "Path to the output CSV file"
    )

    args = parser.parse_args()

    rows = read_data(args.input)
    
    monthly_counts = count_noise_month(rows)

    if args.output:
        write_noise_csv(monthly_counts, args.output)

    else:
        for month in sorted(monthly_counts):
            print(f"\n{calendar.month_name[month]}")

            for descriptor, count in monthly_counts[month].most_common():
                print(f" {descriptor}: {count}")

if __name__ == "__main__":
    main()
