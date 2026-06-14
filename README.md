# Assignment 4 — Heaps and Priority Queues

This repository contains an educational implementation and analysis of
heap data structures, Heapsort, and a binary-heap-based priority queue.

Repository layout
- `src/heapsort.py` — in-place Heapsort (max-heap) with detailed docstrings
- `src/priority_queue.py` — `Task` dataclass and `BinaryMaxHeap` implementation
- `src/scheduler.py` — small scheduler simulation using the priority queue
- `benchmarks/compare_sorts.py` — simple benchmark runner (prints timings)
- `benchmarks/run_and_plot.py` — repeated benchmarking and plotting script
- `benchmarks/bench_results.csv` — benchmark numeric results
- `benchmarks/plots.png` — saved plot of benchmark results
- `benchmarks/run_bench_output.txt` — raw textual output from a run
- `report.md` — analysis, complexity discussion, and experimental summary

Quick start (recommended)

1. Create and activate the virtual environment (optional but recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install required packages (for plotting):

```bash
pip install --user -r requirements.txt || pip install matplotlib
```

3. Run small demos:

```bash
python3 src/heapsort.py     # quick self-check for heapsort
python3 src/scheduler.py    # scheduler demo (random tasks)
```

4. Run the simple benchmark (prints timings):

```bash
python3 benchmarks/compare_sorts.py
```

5. Run the repeated benchmark and generate plots (requires matplotlib):

```bash
python3 benchmarks/run_and_plot.py
```

Report and results

- View the analysis and embedded benchmark summary in `report.md`.
- The generated plot is at `benchmarks/plots.png` and CSV results are in
	`benchmarks/bench_results.csv`.

Notes and suggestions
- The provided sorting implementations are intentionally simple and
	educational; prefer Python's built-in `sorted()` for production use.
- If you'd like, I can add a `requirements.txt`, CI to re-run benchmarks,
	or convert the report to PDF/HTML with embedded figures.