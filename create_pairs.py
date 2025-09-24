import os
import csv

csv_file = "../mentors_mentees.csv"
pairs_folder = "pairings"
project_csv_file = "project_cards.csv"

os.makedirs(pairs_folder, exist_ok=True)

with open(project_csv_file, "w", newline='') as project_csv:
    writer = csv.writer(project_csv)
    writer.writerow(["Pair", "Mentor", "Mentee", "Goals", "Progress", "Meetings", "Deliverables"])

    with open(csv_file, newline='', encoding='utf-8-sig') as f:
        # encoding='utf-8-sig' removes BOM automatically
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            mentor_email = row['mentor_email']
            mentee_email = row['mentee_email']

            mentor_name = mentor_email.split('@')[0]
            mentee_name = mentee_email.split('@')[0]
            pair_folder = os.path.join(pairs_folder, f"pair-{i}-{mentor_name}-{mentee_name}")
            os.makedirs(pair_folder, exist_ok=True)

            with open(os.path.join(pair_folder, "README.md"), "w") as readme:
                readme.write(f"# Pair {i}: {mentor_name} & {mentee_name}\n\n")
                readme.write("## Goals\n- \n\n## Progress\n- \n\n## Meetings\n- \n\n## Deliverables\n- \n")

            writer.writerow([f"Pair {i}", mentor_email, mentee_email, "", "Not Started", "", ""])

print(f"Created {pairs_folder} folder with pair placeholders.")
print(f"Generated {project_csv_file} for GitHub Project import.")
