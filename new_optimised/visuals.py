# visuals.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

COLORS = {
    "navy":      "#0B1F3A",
    "gold":      "#C99A4E",
    "cool_gray": "#A5A5A5",
    "ivory":     "#FEFDF9",
    "graphite":  "#2C2C2C",
}

def apply_theme():
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor":   COLORS["ivory"],
        "axes.edgecolor":   COLORS["graphite"],
        "grid.color":       COLORS["cool_gray"],
        "grid.alpha":       0.3,
        "grid.linestyle":   "--",
        "font.family":      "Open Sans",
        "font.size":        12,
        "axes.titlesize":   14,
        "axes.titleweight": "bold",
        "axes.labelsize":   12,
        "xtick.color":      COLORS["graphite"],
        "ytick.color":      COLORS["graphite"],
        "lines.linewidth":  2,
        "legend.frameon":   False,
        "legend.fontsize":  11,
        "savefig.dpi":      300,
    })
    sns.set_style("whitegrid", {
        "axes.facecolor": COLORS["ivory"],
        "grid.color":     COLORS["cool_gray"],
    })

def style_metrics_table(df):
    """
    Take a DataFrame of raw numeric metrics and return a styled
    Styler with Navy/Gray/Gold columns, Open Sans 9pt cells.
    """
    palette = {
        "Portfolio":  COLORS["navy"],
        "Benchmark":  COLORS["cool_gray"],
        "Difference": COLORS["gold"],
    }

    def _color(col):
        c = palette.get(col.name, "white")
        return [f"background-color: {c}; color: white; font-weight: 600;"
                for _ in col]

    return (
        df.style
          .apply(_color, axis=0)
          .set_properties(**{
              "font-family": "Open Sans",
              "font-size":   "9pt",
              "text-align":  "center",
          })
          .set_caption("Performance Metrics")
    )