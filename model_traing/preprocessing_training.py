import json
import os
import glob

dataset_dir = "datasets/instruction_dataset"

output_file = "datasets/processed/instruction_data.txt"

os.makedirs("datasets/processed", exist_ok=True)

# -----------------------------------
# STEP 1: LOAD ALL DESCRIPTIONS
# -----------------------------------

descriptions = {}

print("Loading descriptions...")

jsonl_files = glob.glob(f"{dataset_dir}/*.jsonl")

for file_path in jsonl_files:

    with open(file_path, "r", encoding="utf-8") as f:

        for line in f:

            try:

                data = json.loads(line)

                task_id = data.get("task_id", "")

                # Find description fields
                description = ""

                for key in data.keys():

                    if "description" in key.lower():

                        description = data[key]

                if task_id and description:

                    descriptions[task_id] = description

            except:
                pass

print("Descriptions Loaded:", len(descriptions))

# -----------------------------------
# STEP 2: LOAD ALL CODE SAMPLES
# -----------------------------------

all_samples = []

print("Loading Verilog code samples...")

for file_path in jsonl_files:

    with open(file_path, "r", encoding="utf-8") as f:

        for line in f:

            try:

                data = json.loads(line)

                task_id = data.get("task_id", "")

                code = ""

                # Find code/completion fields
                for key in data.keys():

                    if (
                        "completion" in key.lower()
                        or "code" in key.lower()
                        or "solution" in key.lower()
                    ):

                        code = data[key]

                # Match with descriptions
                if task_id in descriptions and code:

                    prompt = descriptions[task_id]

                    sample = f"""
### Prompt:
{prompt}

### Response:
{code}
"""

                    all_samples.append(sample)

            except:
                pass

# Remove duplicates
all_samples = list(set(all_samples))

# -----------------------------------
# STEP 3: SAVE DATASET
# -----------------------------------

with open(output_file, "w", encoding="utf-8") as f:

    for sample in all_samples:

        f.write(sample + "\n")

print("\nInstruction dataset created!")

print("Total Samples:", len(all_samples))
