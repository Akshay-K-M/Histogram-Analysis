#!/usr/bin/env python3
import argparse
import csv
import time
from collections import Counter

import matplotlib.pyplot as plt

MAX_BUCKETS = 10


def interval_cost(groups, left, right):
    """Weighted n_i * variance for frequency groups [left, right)."""
    weight = sum(groups[i][1] for i in range(left, right))
    total = sum(groups[i][0] * groups[i][1] for i in range(left, right))
    squares = sum(groups[i][0] ** 2 * groups[i][1] for i in range(left, right))
    return squares - (total * total / weight)


def build_serial_histogram(values, max_buckets=MAX_BUCKETS):
    value_frequencies = Counter(values)

    # Keep equal-frequency values together, so redundant buckets cannot occur.
    by_frequency = {}
    for value, frequency in value_frequencies.items():
        by_frequency.setdefault(frequency, []).append(value)

    frequencies = sorted(by_frequency)
    groups = [(f, len(by_frequency[f])) for f in frequencies]
    group_count = len(groups)
    limit = min(max_buckets, group_count)

    dp = [[float("inf")] * (group_count + 1) for _ in range(limit + 1)]
    cut = [[-1] * (group_count + 1) for _ in range(limit + 1)]
    dp[0][0] = 0.0

    for bucket_count in range(1, limit + 1):
        for right in range(bucket_count, group_count + 1):
            for left in range(bucket_count - 1, right):
                candidate = dp[bucket_count - 1][left] + interval_cost(groups, left, right)
                if candidate < dp[bucket_count][right]:
                    dp[bucket_count][right] = candidate
                    cut[bucket_count][right] = left

    # Minimum error; if tied, prefer fewer buckets.
    best_count = min(range(1, limit + 1), key=lambda b: (dp[b][group_count], b))

    intervals = []
    right = group_count
    for bucket_count in range(best_count, 0, -1):
        left = cut[bucket_count][right]
        intervals.append((left, right))
        right = left
    intervals.reverse()

    buckets = []
    for left, right in intervals:
        bucket_frequencies = frequencies[left:right]
        bucket_values = []
        tuple_total = 0
        weighted_total = 0

        for frequency in bucket_frequencies:
            current_values = sorted(by_frequency[frequency])
            bucket_values.extend(current_values)
            tuple_total += frequency * len(current_values)
            weighted_total += frequency * len(current_values)

        buckets.append({
            "min_frequency": bucket_frequencies[0],
            "max_frequency": bucket_frequencies[-1],
            "average_frequency": weighted_total / len(bucket_values),
            "values": bucket_values,
            "tuple_total": tuple_total,
        })

    return buckets, dp[best_count][group_count]


def compact_values(values, width=50):
    if len(values) == 1:
        text = repr(values[0])
    elif len(values) == 2:
        text = f"{values[0]!r}, {values[1]!r}"
    else:
        text = f"{values[0]!r}, ..., {values[-1]!r} ({len(values)} values)"
    return text if len(text) <= width else text[:width - 3] + "..."


def plot_like_slides(column, buckets, value_frequencies_for_plot, output_file):
    # Slide layout: frequency intervals are boxes resting on one baseline.
    fig, ax = plt.subplots(figsize=(13, 6))

    for index, bucket in enumerate(buckets, 1):
        low = bucket["min_frequency"]
        high = bucket["max_frequency"]

        # Frequencies are discrete. Add half a unit on each side so even a
        # [f, f] bucket is a visible box centred at f.
        left = low - 0.45
        width = (high - low) + 0.90

        # Height has no statistical meaning; it only leaves room for labels.
        shown = bucket["values"][:4]
        height = 0.75 + 0.32 * len(shown)

        rectangle = plt.Rectangle(
            (left, 0), width, height,
            facecolor="none", edgecolor=f"C{(index - 1) % 10}",
            linewidth=3, linestyle=":"
        )
        ax.add_patch(rectangle)

        if len(bucket["values"]) <= 4:
            value_text = "\n".join(repr(v) for v in shown)
        else:
            value_text = "\n".join(repr(v) for v in shown[:3])
            value_text += f"\n... ({len(bucket['values'])} values)"

        ax.text(left + width / 2, height / 2, value_text,
                ha="center", va="center", fontsize=8)
        ax.text(left + width / 2, height + 0.08, f"B{index}",
                ha="center", va="bottom", fontsize=9, fontweight="bold")

        ax.text(low, -0.10, str(low), ha="center", va="top", fontsize=9)
        if high != low:
            ax.text(high, -0.10, str(high), ha="center", va="top", fontsize=9)

    max_height = max(0.75 + 0.32 * min(4, len(b["values"])) for b in buckets)
    max_frequency = max(b["max_frequency"] for b in buckets)

    ax.axhline(0, color="black", linewidth=2)
    ax.set_xlim(0, max_frequency + 1)
    ax.set_ylim(-0.35, max_height + 0.55)
    ax.set_xlabel("Frequencies", fontsize=13)
    ax.set_ylabel("Value Set", fontsize=13)
    ax.set_title(f"Optimal serial histogram for {column}")
    ax.set_yticks([])
    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)

    fig.tight_layout()
    fig.savefig(output_file, dpi=200, bbox_inches="tight")
    plt.close(fig)


def write_boundaries(column, buckets):
    filename = f"serial_histogram_{column}_boundaries.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["bucket", "min_frequency", "max_frequency", "average_frequency",
                         "distinct_values", "sample_tuples", "values"])
        for i, bucket in enumerate(buckets, 1):
            writer.writerow([i, bucket["min_frequency"], bucket["max_frequency"],
                             f"{bucket['average_frequency']:.6f}", len(bucket["values"]),
                             bucket["tuple_total"], " | ".join(bucket["values"])])
    return filename


def main():
    parser = argparse.ArgumentParser(description="Build optimal serial histograms from a CSV sample.")
    parser.add_argument("sample_file", help="CSV containing id and title columns")
    args = parser.parse_args()

    with open(args.sample_file, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    for column in ("id", "title"):
        values = [row[column] for row in rows if row[column] != ""]

        start = time.perf_counter()
        buckets, objective = build_serial_histogram(values)
        elapsed = time.perf_counter() - start

        print(f"\n{column}: {len(buckets)} bucket(s), {elapsed:.6f} seconds, objective={objective:.6f}")
        for i, bucket in enumerate(buckets, 1):
            print(f"B{i}: frequency [{bucket['min_frequency']}, {bucket['max_frequency']}], "
                  f"average={bucket['average_frequency']:.3f}, "
                  f"distinct_values={len(bucket['values'])}")

        plot_like_slides(column, buckets, Counter(values), f"serial_histogram_{column}.png")
        write_boundaries(column, buckets)


if __name__ == "__main__":
    main()
