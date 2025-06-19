import re
import csv

input_file = 'results/infra_results3.txt'
output_file = 'results/infra_results3.csv'

pattern = re.compile(
    r"Infra: (?P<Infra_Upgrade>\d+->\d+), "
    r"Con: (?P<Con_Mod>[0-9.]+), "
    r"Econ: (?P<Econ_Law>.*?), "
    r"CGF=(?P<CGF>[0-9.]+), "
    r"Mils=(?P<Mils>\d+), "
    r"Fac=(?P<Fac>\d+) => Days: (?P<Days>\d+), Infra Fac: (?P<Infra_Fac>\d+)"
)

rows = []

with open(input_file, 'r', encoding='utf-16') as f:
    for line in f:
        match = pattern.search(line)
        if match:
            rows.append(match.groupdict())

with open(output_file, 'w', newline='', encoding='utf-16') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'Infra_Upgrade', 'Con_Mod', 'Econ_Law', 'CGF', 'Mils', 'Fac', 'Days', 'Infra_Fac'
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"Extracted {len(rows)} rows to '{output_file}'")
