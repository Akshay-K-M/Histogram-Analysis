#!/usr/bin/env python3
import matplotlib.pyplot as plt

sample_sizes = [1000, 3000, 5000]
id_error_percent = [0.0, 0.0, 0.0]
title_error_percent = [0.0, 0.025, 0.024]

print("Maximum histogram selectivity error for equality queries")
for n, id_err, title_err in zip(sample_sizes, id_error_percent, title_error_percent):
    print(f"{n} samples: id = {id_err:.3f}%, title = {title_err:.3f}%")

plt.figure(figsize=(8, 5))
plt.plot(sample_sizes, id_error_percent, marker="o", linewidth=2, label="id")
plt.plot(sample_sizes, title_error_percent, marker="o", linewidth=2, label="title")
for x, y in zip(sample_sizes, title_error_percent):
    plt.annotate(f"{y:.3f}%", (x, y), xytext=(0, 8),
                 textcoords="offset points", ha="center")
plt.xlabel("Sample size")
plt.ylabel("Maximum selectivity error (%)")
plt.title("Sample size vs maximum selectivity error")
plt.xticks(sample_sizes)
plt.ylim(bottom=-0.001)
plt.grid(True, linestyle=":", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("sample_size_vs_max_selectivity_error.png", dpi=200)
plt.close()
