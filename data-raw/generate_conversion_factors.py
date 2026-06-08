import csv
import os

# Define region codes: 1 (North), 2 (Central), 3 (South)
regions = [1, 2, 3]

# Define crop categories and their codes
# Crops 1-4: Maize
maize_crops = [1, 2, 3, 4]
# Crops 11-16: Groundnuts
groundnut_crops = [11, 12, 13, 14, 15, 16]
# Crops 17-26: Rice
rice_crops = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
# Root crops: 28 (Sweet potato), 29 (Irish potato), 201 (Cassava, if applicable in other sections, but let's stick to 28, 29)
root_crops = [28, 29]
# Pulses/Beans: 27 (Ground bean), 34 (Beans), 35 (Soyabean), 36 (Pigeonpea), 308 (Cowpea), 46 (Peas)
pulse_crops = [27, 34, 35, 36, 46]
# Other crops: 31 (Finger millet), 32 (Sorghum), 33 (Pearl millet)
millet_crops = [31, 32, 33]
# Veggies: 40 (Cabbage), 43 (Okra/Therere), 44 (Tomato), 45 (Onion)
veg_crops = [40, 43, 44, 45]

# All unique crops listed
all_crops = sorted(list(set(
    maize_crops + groundnut_crops + rice_crops + root_crops + pulse_crops + millet_crops + veg_crops
)))

# Units:
# 1: Kilogram (factor = 1)
# 2: 50 kg bag
# 3: 90 kg bag
# 4: Pail (small)
# 5: Pail (large)
# 14: Pail (medium)
# 12: Oxcart
# 11: Basket (Dengu)
# 8: Heap
# 9: Piece

# Conditions:
# 1: Shelled
# 2: Unshelled
# 3: Not Applicable

factors = []

for reg in regions:
    # Add a slight regional variation (e.g. South has slightly smaller pails/bags on average)
    reg_mult = 1.0 if reg == 2 else (1.05 if reg == 1 else 0.95)
    
    for crop in all_crops:
        # Standard unit: Kilogram
        factors.append({
            "region": reg, "crop_code": crop, "unit_code": 1, "condition": 1, "factor": 1.0
        })
        factors.append({
            "region": reg, "crop_code": crop, "unit_code": 1, "condition": 2, "factor": 1.0
        })
        factors.append({
            "region": reg, "crop_code": crop, "unit_code": 1, "condition": 3, "factor": 1.0
        })
        
        # Determine factor based on crop category
        if crop in maize_crops:
            # Maize
            # Shelled
            factors.append({"region": reg, "crop_code": crop, "unit_code": 2, "condition": 1, "factor": round(50.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 3, "condition": 1, "factor": round(90.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 4, "condition": 1, "factor": round(5.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 5, "condition": 1, "factor": round(15.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 14, "condition": 1, "factor": round(9.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 12, "condition": 1, "factor": round(600.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 11, "condition": 1, "factor": round(25.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 8, "condition": 1, "factor": round(1.5 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 9, "condition": 1, "factor": round(0.3 * reg_mult, 2)})
            # Unshelled
            factors.append({"region": reg, "crop_code": crop, "unit_code": 2, "condition": 2, "factor": round(25.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 3, "condition": 2, "factor": round(45.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 4, "condition": 2, "factor": round(2.5 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 5, "condition": 2, "factor": round(7.5 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 14, "condition": 2, "factor": round(4.5 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 12, "condition": 2, "factor": round(300.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 11, "condition": 2, "factor": round(12.5 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 8, "condition": 2, "factor": round(0.7 * reg_mult, 2)})
            
        elif crop in groundnut_crops:
            # Groundnuts
            # Shelled
            factors.append({"region": reg, "crop_code": crop, "unit_code": 2, "condition": 1, "factor": round(50.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 3, "condition": 1, "factor": round(90.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 4, "condition": 1, "factor": round(4.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 5, "condition": 1, "factor": round(12.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 14, "condition": 1, "factor": round(7.5 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 11, "condition": 1, "factor": round(20.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 8, "condition": 1, "factor": round(1.0 * reg_mult, 2)})
            # Unshelled
            factors.append({"region": reg, "crop_code": crop, "unit_code": 2, "condition": 2, "factor": round(20.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 3, "condition": 2, "factor": round(35.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 4, "condition": 2, "factor": round(1.5 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 5, "condition": 2, "factor": round(5.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 14, "condition": 2, "factor": round(3.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 11, "condition": 2, "factor": round(8.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 8, "condition": 2, "factor": round(0.4 * reg_mult, 2)})
            
        elif crop in rice_crops:
            # Rice (mainly N/A or Shelled)
            for cond in [1, 3]:
                factors.append({"region": reg, "crop_code": crop, "unit_code": 2, "condition": cond, "factor": round(50.0 * reg_mult, 1)})
                factors.append({"region": reg, "crop_code": crop, "unit_code": 3, "condition": cond, "factor": round(90.0 * reg_mult, 1)})
                factors.append({"region": reg, "crop_code": crop, "unit_code": 4, "condition": cond, "factor": round(4.8 * reg_mult, 2)})
                factors.append({"region": reg, "crop_code": crop, "unit_code": 5, "condition": cond, "factor": round(14.5 * reg_mult, 2)})
                factors.append({"region": reg, "crop_code": crop, "unit_code": 14, "condition": cond, "factor": round(8.8 * reg_mult, 2)})
                factors.append({"region": reg, "crop_code": crop, "unit_code": 11, "condition": cond, "factor": round(24.0 * reg_mult, 1)})
                factors.append({"region": reg, "crop_code": crop, "unit_code": 8, "condition": cond, "factor": round(1.2 * reg_mult, 2)})
                
        elif crop in root_crops:
            # Roots (Not Applicable condition)
            factors.append({"region": reg, "crop_code": crop, "unit_code": 2, "condition": 3, "factor": round(50.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 3, "condition": 3, "factor": round(90.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 4, "condition": 3, "factor": round(6.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 5, "condition": 3, "factor": round(18.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 14, "condition": 3, "factor": round(11.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 11, "condition": 3, "factor": round(30.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 8, "condition": 3, "factor": round(2.5 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 9, "condition": 3, "factor": round(0.5 * reg_mult, 2)})
            
        elif crop in pulse_crops:
            # Pulses
            # Shelled
            factors.append({"region": reg, "crop_code": crop, "unit_code": 2, "condition": 1, "factor": round(50.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 3, "condition": 1, "factor": round(90.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 4, "condition": 1, "factor": round(5.2 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 5, "condition": 1, "factor": round(16.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 14, "condition": 1, "factor": round(9.5 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 11, "condition": 1, "factor": round(26.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 8, "condition": 1, "factor": round(1.8 * reg_mult, 2)})
            # Unshelled
            factors.append({"region": reg, "crop_code": crop, "unit_code": 2, "condition": 2, "factor": round(22.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 3, "condition": 2, "factor": round(40.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 4, "condition": 2, "factor": round(2.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 5, "condition": 2, "factor": round(6.5 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 14, "condition": 2, "factor": round(3.8 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 11, "condition": 2, "factor": round(11.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 8, "condition": 2, "factor": round(0.7 * reg_mult, 2)})
            
        else:
            # Other / Vegetables / Millets (Not Applicable condition)
            factors.append({"region": reg, "crop_code": crop, "unit_code": 2, "condition": 3, "factor": round(50.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 3, "condition": 3, "factor": round(90.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 4, "condition": 3, "factor": round(5.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 5, "condition": 3, "factor": round(15.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 14, "condition": 3, "factor": round(9.0 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 11, "condition": 3, "factor": round(25.0 * reg_mult, 1)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 8, "condition": 3, "factor": round(1.5 * reg_mult, 2)})
            factors.append({"region": reg, "crop_code": crop, "unit_code": 9, "condition": 3, "factor": round(0.5 * reg_mult, 2)})

# Ensure directories exist
os.makedirs("/Users/vitumbikokayuni/Documents/IHS-mw/inst/extdata", exist_ok=True)
csv_path = "/Users/vitumbikokayuni/Documents/IHS-mw/inst/extdata/crop_conversion_factors.csv"

with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["region", "crop_code", "unit_code", "condition", "factor"])
    writer.writeheader()
    writer.writerows(factors)

print(f"Generated {len(factors)} conversion factor combinations.")
