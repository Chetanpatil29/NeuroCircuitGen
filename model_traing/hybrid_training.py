import os

instruction_file = "datasets/processed/instruction_data.txt"

rtl_file = "datasets/processed/verilog_data.txt"

output_file = "datasets/processed/hybrid_data.txt"

all_data = []

# -----------------------------------
# LOAD INSTRUCTION DATA
# -----------------------------------

print("Loading instruction dataset...")

with open(instruction_file, "r", encoding="utf-8") as f:

    instruction_text = f.read()

    all_data.append(instruction_text)

# -----------------------------------
# LOAD RAW RTL DATA
# -----------------------------------

print("Loading RTL dataset...")

with open(rtl_file, "r", encoding="utf-8") as f:

    rtl_text = f.read()

    all_data.append(rtl_text)

# -----------------------------------
# SAVE HYBRID DATA
# -----------------------------------

combined_text = "\n\n".join(all_data)

with open(output_file, "w", encoding="utf-8") as f:

    f.write(combined_text)

print("\nHybrid dataset created!")

print("Saved to:", output_file)
