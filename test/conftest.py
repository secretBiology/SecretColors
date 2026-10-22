import os

# Plot tests must not initialize a desktop GUI on macOS or headless CI.
os.environ["MPLBACKEND"] = "Agg"
