import os
import pandas as pd
from datetime import datetime

folder_path = r"C:\Users\user\PycharmProjects\ws3"

file_list = [f for f in os.listdir(folder_path) if f.startswith("dict") and f.endswith(".xlsx")]

all_data = []

for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    try:
        date_str = file_name[4:12]  # 'dict20250711.xlsx' -> '20250711'
        date = datetime.strptime(date_str, "%Y%m%d").date()

        df = pd.read_excel(file_path)
        df['date'] = date  # felülírjuk, hogy biztosan egyezzen a fájlnévbeli dátummal
        df = df.drop_duplicates(subset='data-prof-id', keep='first')

        all_data.append(df)
    except Exception as e:
        print(f"Hiba a fájl feldolgozása során: {file_name}: {e}")

if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)

    combined_df = combined_df.sort_values(by=['data-prof-id', 'date'])

    first_dates = combined_df.groupby('data-prof-id')['date'].first().reset_index()
    first_dates.rename(columns={'date': 'first_date'}, inplace=True)

    last_records = combined_df.groupby('data-prof-id').tail(1).copy()
    last_records = last_records.merge(first_dates, on='data-prof-id', how='left')
    last_records.rename(columns={'date': 'last_date'}, inplace=True)

    output_path = os.path.join(folder_path, 'merged_output.xlsx')
    last_records.to_excel(output_path, index=False)
    print(f"Sikeresen elmentve: {output_path}")
else:
    print("Nincs feldolgozható adat.")
