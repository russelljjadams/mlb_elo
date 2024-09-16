import csv
import re

def process_baseball_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Date', 'Team1', 'Team1_Runs', 'Team2', 'Team2_Runs'])

        date = None

        for line in infile:
            line = line.strip()

            # Skip empty lines or lines that don't contain game data
            if not line or "Standings & Scores" in line:
                continue

            # Check if the line is a date
            if re.match(r'^\w+,\s\w+\s\d{1,2},\s\d{4}$', line):
                date = line
                continue
            
            # Check if the line contains game data
            match = re.match(r'(.+?)\s\((\d+)\)\s@\s(.+?)\s\((\d+)\)', line)
            if match and date:
                team1 = match.group(1).strip()
                team1_runs = match.group(2).strip()
                team2 = match.group(3).strip()
                team2_runs = match.group(4).strip()
                writer.writerow([date, team1, team1_runs, team2, team2_runs])
            else:
                # Suppress error message by removing the print statement
                pass

# Use the script by specifying the input file and output file
input_file = 'mlb.txt'
output_file = 'mlb.csv'
process_baseball_data(input_file, output_file)

print(f"Data has been successfully written to {output_file}")

