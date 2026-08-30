# Histogram Analysis

Implementation and results for Assignment 1 on PostgreSQL histograms using the Join Order Benchmark (2013 snapshot).

The repository contains:

- PostgreSQL histogram visualisations for `id` and `title` from the `title` table.
- Optimal serial histograms built from random samples of 1,000, 3,000, and 5,000 rows.
- Bucket-boundary CSV files and generated plots.
- Linear-regression extrapolation for full-table histogram construction time.
- Sample-size versus maximum-selectivity-error analysis.

## Environment

The work was run on macOS 15.6.1 with Python 3 and PostgreSQL 18.3 installed through Homebrew. Commands may vary slightly on another operating system. Equivalent commands for other operating systems are not included here.

The JOB database was loaded into a PostgreSQL database named `job`. The `title` table contained 2,528,312 rows.

## Setup

From the repository root, create and activate a virtual environment, then install the Python dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Q1.6: PostgreSQL histogram plots

Run from the `Q1.6` directory:

```bash
python3 id_title_plotter.py
```

The generated plots are:

- `id_histogram.png` (Correct)
- `title_native_collation_histogram.png` (Correct)
- `title_ordinal_histogram.png` (Incorrect)
- `title_scalar_histogram.png` (Incorrect)
I have stored the incorrect files to document the exploration process.

## Q2: Random samples

The samples were created separately and stored as CSV files so that all later results are reproducible. Sampling time is therefore excluded from the reported histogram-construction times.

Run from the `Q2` directory:

```bash
psql -d job -c "\copy (
  SELECT id, title
  FROM title TABLESAMPLE BERNOULLI (1)
  ORDER BY random()
  LIMIT 1000
) TO 'title_sample_1000.csv' WITH (FORMAT CSV, HEADER)"
```

```bash
psql -d job -c "\copy (
  SELECT id, title
  FROM title TABLESAMPLE BERNOULLI (1)
  ORDER BY random()
  LIMIT 3000
) TO 'title_sample_3000.csv' WITH (FORMAT CSV, HEADER)"
```

```bash
psql -d job -c "\copy (
  SELECT id, title
  FROM title TABLESAMPLE BERNOULLI (1)
  ORDER BY random()
  LIMIT 5000
) TO 'title_sample_5000.csv' WITH (FORMAT CSV, HEADER)"
```

`BERNOULLI` performs row-level sampling. ORDER BY random() followed by LIMIT selects the requested number of rows from the sampled candidates, provided TABLESAMPLE BERNOULLI (1) returns at least that many rows.

## Q2.1-Q2.5: Optimal serial histograms

`serial_histogram.py` reads a sample CSV supplied on the command line and builds histograms for both `id` and `title`. It uses at most 10 non-redundant buckets and minimises the serial-histogram objective.

Run from the `Q2` directory:

```bash
python3 serial_histogram.py title_sample_1000.csv
python3 serial_histogram.py title_sample_3000.csv
python3 serial_histogram.py title_sample_5000.csv
```

Each run prints:

- Histogram construction time for `id` and `title`.
- Actual number of buckets.
- Frequency boundaries, average frequency, and distinct-value count for every bucket.
- Objective value.

Each run also creates histogram plots and bucket-boundary CSV files. The final outputs have been organised under:

- `Q2/1000 samples/`
- `Q2/3000 samples/`
- `Q2/5000 samples/`

## Q2.6-Q2.7: Timing regression

From the `Q2` directory, run:

```bash
python3 regression_analysis.py
```

The script uses the recorded build times for 1,000, 3,000, and 5,000 samples. It prints the linear-regression equations and extrapolated build times for the complete `title` table, and generates:

```text
sample_size_vs_time.png
```

## Q2.8: Selectivity-error plot

From the `Q2` directory, run:

```bash
python3 selectivity_error.py
```

The script prints the maximum histogram selectivity errors used in the report and generates:

```text
sample_size_vs_max_selectivity_error.png
```

The reported errors consider a single-value equality query and histogram approximation error only, not sampling error.

## Repository structure

```text
Q1.6/                         PostgreSQL histogram plotting code and plots
Q2/                           Serial-histogram code, samples, results, and analysis
Q2/1000 samples/              Results for the 1,000-row sample
Q2/3000 samples/              Results for the 3,000-row sample
Q2/5000 samples/              Results for the 5,000-row sample
Reference/                    Reference documents
requirements.txt              Python dependencies
README.md                     Execution instructions
```
