import subprocess
import csv
from datetime import datetime

# Base command to run the model with default settings
BASE_CMD = [
    "python", "main.py",
    "--model", "meta-llama/Llama-2-7b-hf",
    "--rotate",
    "--a_bits", "4",
    "--v_bits", "4",
    "--k_bits", "4",
    "--w_bits", "4",
    "--w_clip",
    "--eval_dataset", "wikitext2"
]

# Different configurations to test
configs = {
    "baseline_fp16": BASE_CMD[:-9] + ["--a_bits", "16"],
    "symmetric": BASE_CMD + ["--no-a_asym"],
    "asymmetric": BASE_CMD + ["--a_asym"],
    "auto_asym": BASE_CMD + ["--a_auto_asym"]
}

results = []

# Run each configuration and collect output
for name, cmd in configs.items():
    print(f"\nRunning: {name}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = []

    perplexity = "N/A"
    for line in proc.stdout:
        print(line.strip())
        output.append(line.strip())

        # Extract perplexity value from the output
        if "Perplexity" in line or "ppl/" in line:
            perplexity = line.strip()

    # Append result to list
    results.append({
        "config": name,
        "perplexity_output": perplexity,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Write results to a CSV file
csv_filename = "quantization_results.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["config", "perplexity_output", "timestamp"])
    writer.writeheader()
    writer.writerows(results)

print(f"\n Results written to: {csv_filename}")
