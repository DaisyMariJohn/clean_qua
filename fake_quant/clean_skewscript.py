import subprocess

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
    "baseline_fp16": BASE_CMD[:-9] + ["--a_bits", "16"],  # No quantization on activations
    "symmetric": BASE_CMD + ["--no-a_asym"],              # Force symmetric quantization
    "asymmetric": BASE_CMD + ["--a_asym"],                # Force asymmetric quantization
    "auto_asym": BASE_CMD + ["--a_auto_asym"]             # Dynamically decide using skew
}

results = {}

# Run each configuration and collect output
for name, cmd in configs.items():
    print(f"\n Running: {name}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = []

    for line in proc.stdout:
        print(line.strip())
        output.append(line.strip())

        # Look for perplexity result in output
        if "Perplexity" in line or "ppl/" in line:
            results[name] = line.strip()

# Summary of results
print("\n Final Perplexity Results:")
for name, result in results.items():
    print(f"{name}: {result}")
