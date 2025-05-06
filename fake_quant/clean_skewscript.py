# import subprocess
# import re
# from datetime import datetime
# import csv

# # Base command to run the model with default settings
# BASE_CMD = [
#     "python", "main.py",
#     "--model", "meta-llama/Llama-2-7b-hf",
#     "--v_bits", "4",
#     "--k_bits", "4",
#     # "--w_bits", "4",
#     "--w_clip",
#     "--eval_dataset", "wikitext2",
#     "--a_auto_asym"  # enable auto-asym
# ]

# # Sweep over a broader range of threshold values
# mean_std_range = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1]
# skew_range = [0.2, 0.5, 1.0, 1.5, 2.0, 3.0]

# # set this up to collect things 
# results = []

# for mean_thresh in mean_std_range:
#     for skew_thresh in skew_range:
#         print(f"\n Testing mean/std={mean_thresh}, skew={skew_thresh}")
        
#         cmd = BASE_CMD + [
#             f"--mean_std_thresh={mean_thresh}",
#             f"--skew_thresh={skew_thresh}"
#         ]

#         proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
#         output = []
#         perplexity = "N/A"

#         for line in proc.stdout:
#             print(line.strip())
#             output.append(line.strip())
#             match = re.search(r"WIKITEXT2 PPL:\s*([0-9.]+)", line)
#             if match:
#                 perplexity = float(match.group(1))

#         results.append({
#             "mean_std_thresh": mean_thresh,
#             "skew_thresh": skew_thresh,
#             "perplexity": perplexity,
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         })

# # Summary
# print("\n Threshold Sweep Results:")
# for r in results:
#     print(f"{r['timestamp']} | mean/std={r['mean_std_thresh']} | skew={r['skew_thresh']} → PPL: {r['perplexity']}")


# with open("threshold_sweep_results.csv", "w", newline="") as csvfile:
#     fieldnames = ["timestamp", "mean_std_thresh", "skew_thresh", "perplexity"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for r in results:
#         writer.writerow(r)