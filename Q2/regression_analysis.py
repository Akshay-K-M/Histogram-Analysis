#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_SIZES = np.array([1000, 3000, 5000], dtype=float)
FULL_TABLE_SIZE = 2_528_312

TIMES_MS = {
    "id": np.array([0.365, 0.912, 1.474]),
    "title": np.array([0.457, 1.840, 3.191]),
}


def main():
    # Q2.7 focuses on the measured sample range so the three points are readable.
    fig, ax = plt.subplots(figsize=(8, 5))

    for column, measured_times in TIMES_MS.items():
        slope, intercept = np.polyfit(SAMPLE_SIZES, measured_times, 1)
        full_time = slope * FULL_TABLE_SIZE + intercept
        fitted_sample_times = slope * SAMPLE_SIZES + intercept
        ss_res = np.sum((measured_times - fitted_sample_times) ** 2)
        ss_tot = np.sum((measured_times - np.mean(measured_times)) ** 2)
        r_squared = 1 - ss_res / ss_tot

        print(f"{column}:")
        print(f"  regression in ms: time_ms = {slope:.12e} * sample_size + {intercept:.12e}")
        print(f"  R^2 = {r_squared:.6f}")
        print(f"  extrapolated full-table time ({FULL_TABLE_SIZE} rows) = {full_time:.6f} milliseconds")

        ax.scatter(SAMPLE_SIZES, measured_times, label=f"{column} measured")
        ax.plot(SAMPLE_SIZES, fitted_sample_times, label=f"{column} regression")

    ax.set_xlabel("Sample size")
    ax.set_ylabel("Histogram build time (milliseconds)")
    ax.set_title("Sample size vs histogram build time")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend()
    fig.tight_layout()
    fig.savefig("sample_size_vs_time.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()
