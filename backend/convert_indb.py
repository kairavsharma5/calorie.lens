import openpyxl

wb    = openpyxl.load_workbook('Anuvaad_INDB_2024.11.xlsx', data_only=True)
sheet = wb['Sheet1']

headers      = [cell.value for cell in sheet[1]]
name_idx     = headers.index('food_name')
calories_idx = headers.index('energy_kcal')
protein_idx  = headers.index('protein_g')
carbs_idx    = headers.index('carb_g')
fat_idx      = headers.index('fat_g')

lines = []
lines.append("# Auto-generated from INDB 2024 dataset")
lines.append("# 1014 Indian recipes with nutrition per 100g")
lines.append("")
lines.append("INDB_FOODS = {")

for row in sheet.iter_rows(min_row=2, values_only=True):
    name     = row[name_idx]
    calories = row[calories_idx]
    protein  = row[protein_idx]
    carbs    = row[carbs_idx]
    fat      = row[fat_idx]

    if not name or calories is None:
        continue

    clean_name = str(name).lower().strip()
    calories   = round(float(calories), 1) if calories else 0
    protein    = round(float(protein),  1) if protein  else 0
    carbs      = round(float(carbs),    1) if carbs    else 0
    fat        = round(float(fat),      1) if fat      else 0

    lines.append(f'    "{clean_name}": {{"calories": {calories}, "protein": {protein}, "carbs": {carbs}, "fat": {fat}}},')

lines.append("}")

# write directly to file with proper UTF-8 encoding
with open('data/indb_foods.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Done! data/indb_foods.py created successfully.")