#!/usr/bin/env python3
"""
GPU Correlation Matrix Builder
==============================
Fetches 500-day history for NVDA, BTC-USD, DX-Y.NYB, NG=F from Yahoo Finance,
computes pairwise correlations, generates plots and saves results.

Outputs:
  - dashboard/plots/nvda_btc_correlation.html + .png
  - dashboard/plots/nvda_dxy_correlation.html + .png
  - dashboard/plots/correlation_heatmap.html + .png
  - dashboard/plots/nvda_500d_trend.html + .png
  - raw_data/correlation_matrix.json
"""

import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import yfinance as yf

# Import plotly and matplotlib — both may be available
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    print("WARNING: plotly not installed. HTML plots will not be generated.")
    PLOTLY_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MPL_AVAILABLE = True
except ImportError:
    print("WARNING: matplotlib not installed. PNG plots will not be generated.")
    MPL_AVAILABLE = False

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw_data")
PLOTS_DIR = os.path.join(BASE_DIR, "dashboard", "plots")
SCRIPT_DIR = os.path.join(BASE_DIR, "scripts")

os.makedirs(PLOTS_DIR, exist_ok=True)

# ── Helpers ──────────────────────────────────────────────────────────────────

def fetch_history(ticker: str, period: str = "500d") -> dict:
    """Fetch close-price history from yfinance, returning {date_str: price}."""
    print(f"  Fetching {ticker} ({period})...")
    try:
        t = yf.Ticker(ticker)
        df = t.history(period=period)
        if df.empty:
            print(f"  WARNING: {ticker} returned empty dataframe")
            return {}
        prices = {}
        for idx, row in df.iterrows():
            close = float(row["Close"])
            if np.isnan(close) or close <= 0:
                continue
            date_str = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx.date())
            prices[date_str] = close
        print(f"  Got {len(prices)} data points for {ticker}")
        return prices
    except Exception as e:
        print(f"  ERROR fetching {ticker}: {e}")
        return {}


def aligned_series(*dicts, labels: list[str]):
    """
    Given multiple {date: price} dicts, return a DataFrame with aligned dates
    (only dates present in ALL series).
    """
    # Find common dates
    date_sets = [set(d.keys()) for d in dicts]
    common_dates = sorted(set.intersection(*date_sets))
    if not common_dates:
        print("  WARNING: No common dates across all series!")
        return None

    import pandas as pd
    data = {}
    for label, d in zip(labels, dicts):
        data[label] = [d[dt] for dt in common_dates]
    df = pd.DataFrame(data, index=pd.to_datetime(common_dates))
    return df


def save_json(path: str, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved {path}")


# ── Plotting Functions ───────────────────────────────────────────────────────

def plot_nvda_btc(df, label: str):
    """NVDA vs BTC scatter + dual-axis overlay."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ── Matplotlib version ──
    if MPL_AVAILABLE:
        fig, ax1 = plt.subplots(figsize=(12, 6))

        color_nvda = "#76B900"  # NVIDIA green
        color_btc = "#F7931A"   # Bitcoin orange

        dates = df.index.to_pydatetime()
        ax1.plot(dates, df["NVDA"], color=color_nvda, linewidth=1.5, label="NVDA (USD)")
        ax1.set_ylabel("NVDA Price (USD)", color=color_nvda)
        ax1.tick_params(axis="y", labelcolor=color_nvda)
        ax1.legend(loc="upper left")

        ax2 = ax1.twinx()
        ax2.plot(dates, df["BTC-USD"], color=color_btc, linewidth=1.5, label="BTC (USD)")
        ax2.set_ylabel("Bitcoin Price (USD)", color=color_btc)
        ax2.tick_params(axis="y", labelcolor=color_btc)
        ax2.legend(loc="upper right")

        plt.title(f"NVDA vs Bitcoin — 500-Day Overlay ({label})")
        fig.autofmt_xdate()
        fig.tight_layout()
        png_path = os.path.join(PLOTS_DIR, "nvda_btc_overlay.png")
        fig.savefig(png_path, dpi=150)
        plt.close(fig)
        print(f"  Saved {png_path}")

        # Scatter
        corr = df["NVDA"].corr(df["BTC-USD"])
        fig2, ax = plt.subplots(figsize=(8, 8))
        ax.scatter(df["NVDA"], df["BTC-USD"], alpha=0.4, s=10, c="#76B900")
        ax.set_xlabel("NVDA Price (USD)")
        ax.set_ylabel("Bitcoin Price (USD)")
        ax.set_title(f"NVDA vs Bitcoin Scatter (500d) — r = {corr:.3f}")
        ax.grid(True, alpha=0.3)

        # Fit line
        m, b = np.polyfit(df["NVDA"], df["BTC-USD"], 1)
        x_line = np.linspace(df["NVDA"].min(), df["NVDA"].max(), 100)
        ax.plot(x_line, m * x_line + b, "r--", linewidth=1, alpha=0.7)
        png_path2 = os.path.join(PLOTS_DIR, "nvda_btc_correlation.png")
        fig2.savefig(png_path2, dpi=150)
        plt.close(fig2)
        print(f"  Saved {png_path2}")

    # ── Plotly version ──
    if PLOTLY_AVAILABLE:
        corr = df["NVDA"].corr(df["BTC-USD"])
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(
                f"NVDA vs Bitcoin — 500-Day Price Overlay (r = {corr:.3f})",
                f"NVDA vs Bitcoin — Scatter"
            ),
            vertical_spacing=0.15,
            row_heights=[0.5, 0.5],
        )

        # Overlay
        fig.add_trace(
            go.Scatter(x=df.index, y=df["NVDA"], name="NVDA",
                       line=dict(color="#76B900", width=2),
                       yaxis="y"),
            row=1, col=1,
        )
        fig.add_trace(
            go.Scatter(x=df.index, y=df["BTC-USD"], name="Bitcoin",
                       line=dict(color="#F7931A", width=2),
                       yaxis="y2"),
            row=1, col=1,
        )

        fig.update_layout(
            yaxis=dict(title="NVDA Price (USD)", side="left", color="#76B900"),
            yaxis2=dict(title="Bitcoin Price (USD)", side="right",
                        color="#F7931A", overlaying="y", anchor="x"),
            legend=dict(x=0.01, y=0.99),
        )

        # Scatter
        fig.add_trace(
            go.Scatter(
                x=df["NVDA"], y=df["BTC-USD"], mode="markers",
                marker=dict(color="#76B900", size=4, opacity=0.5),
                name="Daily Pairs",
                showlegend=False,
            ),
            row=2, col=1,
        )
        m, b = np.polyfit(df["NVDA"], df["BTC-USD"], 1)
        x_line = np.linspace(df["NVDA"].min(), df["NVDA"].max(), 100)
        fig.add_trace(
            go.Scatter(x=x_line, y=m * x_line + b, mode="lines",
                       line=dict(color="red", dash="dash", width=1),
                       name=f"Fit (r={corr:.3f})"),
            row=2, col=1,
        )
        fig.update_xaxes(title_text="NVDA Price (USD)", row=2, col=1)
        fig.update_yaxes(title_text="Bitcoin Price (USD)", row=2, col=1)

        fig.update_layout(
            title_text=f"NVDA vs Bitcoin — {label}",
            height=800,
            template="plotly_dark",
        )
        html_path = os.path.join(PLOTS_DIR, "nvda_btc_correlation.html")
        fig.write_html(html_path)
        print(f"  Saved {html_path}")


def plot_nvda_dxy(df, label: str):
    """NVDA vs DXY scatter + dual-axis overlay."""
    if MPL_AVAILABLE:
        fig, ax1 = plt.subplots(figsize=(12, 6))
        color_nvda = "#76B900"
        color_dxy = "#2E86C1"

        dates = df.index.to_pydatetime()
        ax1.plot(dates, df["NVDA"], color=color_nvda, linewidth=1.5, label="NVDA (USD)")
        ax1.set_ylabel("NVDA Price (USD)", color=color_nvda)
        ax1.tick_params(axis="y", labelcolor=color_nvda)
        ax1.legend(loc="upper left")

        ax2 = ax1.twinx()
        ax2.plot(dates, df["DX-Y.NYB"], color=color_dxy, linewidth=1.5, label="DXY")
        ax2.set_ylabel("US Dollar Index (DXY)", color=color_dxy)
        ax2.tick_params(axis="y", labelcolor=color_dxy)
        ax2.legend(loc="upper right")

        plt.title(f"NVDA vs US Dollar Index — 500-Day Overlay ({label})")
        fig.autofmt_xdate()
        fig.tight_layout()
        png_path = os.path.join(PLOTS_DIR, "nvda_dxy_overlay.png")
        fig.savefig(png_path, dpi=150)
        plt.close(fig)
        print(f"  Saved {png_path}")

        corr = df["NVDA"].corr(df["DX-Y.NYB"])
        fig2, ax = plt.subplots(figsize=(8, 8))
        ax.scatter(df["NVDA"], df["DX-Y.NYB"], alpha=0.4, s=10, c="#2E86C1")
        ax.set_xlabel("NVDA Price (USD)")
        ax.set_ylabel("US Dollar Index (DXY)")
        ax.set_title(f"NVDA vs DXY Scatter (500d) — r = {corr:.3f}")
        ax.grid(True, alpha=0.3)
        m, b = np.polyfit(df["NVDA"], df["DX-Y.NYB"], 1)
        x_line = np.linspace(df["NVDA"].min(), df["NVDA"].max(), 100)
        ax.plot(x_line, m * x_line + b, "r--", linewidth=1, alpha=0.7)
        png_path2 = os.path.join(PLOTS_DIR, "nvda_dxy_correlation.png")
        fig2.savefig(png_path2, dpi=150)
        plt.close(fig2)
        print(f"  Saved {png_path2}")

    if PLOTLY_AVAILABLE:
        corr = df["NVDA"].corr(df["DX-Y.NYB"])
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(
                f"NVDA vs US Dollar Index — 500-Day Overlay (r = {corr:.3f})",
                f"NVDA vs DXY — Scatter"
            ),
            vertical_spacing=0.15,
            row_heights=[0.5, 0.5],
        )
        fig.add_trace(
            go.Scatter(x=df.index, y=df["NVDA"], name="NVDA",
                       line=dict(color="#76B900", width=2)),
            row=1, col=1,
        )
        fig.add_trace(
            go.Scatter(x=df.index, y=df["DX-Y.NYB"], name="DXY",
                       line=dict(color="#2E86C1", width=2),
                       yaxis="y2"),
            row=1, col=1,
        )
        fig.update_layout(
            yaxis=dict(title="NVDA Price (USD)", side="left", color="#76B900"),
            yaxis2=dict(title="DXY", side="right", color="#2E86C1",
                        overlaying="y", anchor="x"),
            legend=dict(x=0.01, y=0.99),
        )
        fig.add_trace(
            go.Scatter(
                x=df["NVDA"], y=df["DX-Y.NYB"], mode="markers",
                marker=dict(color="#2E86C1", size=4, opacity=0.5),
                name="Daily Pairs",
                showlegend=False,
            ),
            row=2, col=1,
        )
        m, b = np.polyfit(df["NVDA"], df["DX-Y.NYB"], 1)
        x_line = np.linspace(df["NVDA"].min(), df["NVDA"].max(), 100)
        fig.add_trace(
            go.Scatter(x=x_line, y=m * x_line + b, mode="lines",
                       line=dict(color="red", dash="dash", width=1),
                       name=f"Fit (r={corr:.3f})"),
            row=2, col=1,
        )
        fig.update_xaxes(title_text="NVDA Price (USD)", row=2, col=1)
        fig.update_yaxes(title_text="DXY", row=2, col=1)
        fig.update_layout(
            title_text=f"NVDA vs DXY — {label}",
            height=800,
            template="plotly_dark",
        )
        html_path = os.path.join(PLOTS_DIR, "nvda_dxy_correlation.html")
        fig.write_html(html_path)
        print(f"  Saved {html_path}")


def plot_heatmap(corr_df, label: str):
    """Full correlation heatmap for all pairs."""
    if MPL_AVAILABLE:
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(corr_df.values, cmap="RdBu_r", vmin=-1, vmax=1,
                       aspect="auto")
        tick_labels = corr_df.columns
        ax.set_xticks(range(len(tick_labels)))
        ax.set_yticks(range(len(tick_labels)))
        ax.set_xticklabels(tick_labels, rotation=45, ha="right")
        ax.set_yticklabels(tick_labels)

        for i in range(len(tick_labels)):
            for j in range(len(tick_labels)):
                val = corr_df.values[i, j]
                color = "white" if abs(val) > 0.5 else "black"
                ax.text(j, i, f"{val:.3f}", ha="center", va="center",
                        fontsize=9, color=color)

        plt.colorbar(im, ax=ax, shrink=0.8)
        plt.title(f"Correlation Heatmap — {label}")
        fig.tight_layout()
        png_path = os.path.join(PLOTS_DIR, "correlation_heatmap.png")
        fig.savefig(png_path, dpi=150)
        plt.close(fig)
        print(f"  Saved {png_path}")

    if PLOTLY_AVAILABLE:
        fig = go.Figure(data=go.Heatmap(
            z=corr_df.values,
            x=list(corr_df.columns),
            y=list(corr_df.columns),
            colorscale="RdBu_r",
            zmin=-1, zmax=1,
            text=[[f"{v:.3f}" for v in row] for row in corr_df.values],
            texttemplate="%{text}",
            hovertemplate="%{x} vs %{y}: %{z:.3f}<extra></extra>",
        ))
        fig.update_layout(
            title=f"Correlation Matrix — {label}",
            xaxis_title="Asset",
            yaxis_title="Asset",
            template="plotly_dark",
            height=700,
        )
        html_path = os.path.join(PLOTS_DIR, "correlation_heatmap.html")
        fig.write_html(html_path)
        print(f"  Saved {html_path}")


def plot_nvda_trend(price_dict: dict, label: str):
    """NVDA 500-day time series."""
    dates = sorted(price_dict.keys())
    prices = [price_dict[d] for d in dates]

    if MPL_AVAILABLE:
        fig, ax = plt.subplots(figsize=(14, 6))
        parsed = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
        ax.plot(parsed, prices, color="#76B900", linewidth=1.5)

        # Annotations
        min_idx = np.argmin(prices)
        max_idx = np.argmax(prices)
        ax.annotate(f"Min: ${prices[min_idx]:.2f}",
                    xy=(parsed[min_idx], prices[min_idx]),
                    xytext=(10, -20), textcoords="offset points",
                    arrowprops=dict(arrowstyle="->", color="red"), color="red")
        ax.annotate(f"Max: ${prices[max_idx]:.2f}",
                    xy=(parsed[max_idx], prices[max_idx]),
                    xytext=(10, 10), textcoords="offset points",
                    arrowprops=dict(arrowstyle="->", color="green"), color="green")

        ax.set_ylabel("NVDA Close (USD)")
        ax.set_title(f"NVDA 500-Day Price Trend — {label}")
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        fig.autofmt_xdate()
        fig.tight_layout()
        png_path = os.path.join(PLOTS_DIR, "nvda_500d_trend.png")
        fig.savefig(png_path, dpi=150)
        plt.close(fig)
        print(f"  Saved {png_path}")

    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[datetime.strptime(d, "%Y-%m-%d") for d in dates],
            y=prices,
            mode="lines",
            name="NVDA",
            line=dict(color="#76B900", width=2),
            fill="tozeroy",
            fillcolor="rgba(118, 185, 0, 0.1)",
        ))
        # Min/max markers
        min_idx = np.argmin(prices)
        max_idx = np.argmax(prices)
        fig.add_trace(go.Scatter(
            x=[datetime.strptime(dates[min_idx], "%Y-%m-%d")],
            y=[prices[min_idx]],
            mode="markers+text",
            marker=dict(color="red", size=10, symbol="triangle-down"),
            text=[f"${prices[min_idx]:.2f}"],
            textposition="bottom center",
            name=f"Min ${prices[min_idx]:.2f}",
        ))
        fig.add_trace(go.Scatter(
            x=[datetime.strptime(dates[max_idx], "%Y-%m-%d")],
            y=[prices[max_idx]],
            mode="markers+text",
            marker=dict(color="green", size=10, symbol="triangle-up"),
            text=[f"${prices[max_idx]:.2f}"],
            textposition="top center",
            name=f"Max ${prices[max_idx]:.2f}",
        ))
        fig.update_layout(
            title=f"NVDA 500-Day Price Trend — {label}",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_dark",
            hovermode="x unified",
            height=600,
        )
        html_path = os.path.join(PLOTS_DIR, "nvda_500d_trend.html")
        fig.write_html(html_path)
        print(f"  Saved {html_path}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("GPU Correlation Matrix Builder")
    print("=" * 60)

    label = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 1-4: Fetch 500-day history
    print("\n[1-4] Fetching 500-day history from Yahoo Finance...")
    nvda = fetch_history("NVDA", "500d")
    btc = fetch_history("BTC-USD", "500d")
    dxy = fetch_history("DX-Y.NYB", "500d")
    ng = fetch_history("NG=F", "500d")

    # 5: Compute correlation matrix
    print("\n[5] Computing correlations...")
    all_data = [nvda, btc, dxy, ng]
    labels = ["NVDA", "BTC-USD", "DX-Y.NYB", "NG=F"]

    df = aligned_series(*all_data, labels=labels)
    if df is None:
        print("ERROR: Could not align data. Exiting.")
        sys.exit(1)

    print(f"  Aligned {len(df)} common trading days across all 4 assets")
    corr_df = df.corr(method="pearson")
    print("\n  Correlation Matrix:")
    print(corr_df.to_string())

    # 6: Generate plots
    print("\n[6] Generating plots...")
    plot_nvda_btc(df[["NVDA", "BTC-USD"]], label)
    plot_nvda_dxy(df[["NVDA", "DX-Y.NYB"]], label)
    plot_heatmap(corr_df, label)
    plot_nvda_trend(nvda, label)

    # 7: Save correlation data
    print("\n[7] Saving correlation matrix JSON...")
    corr_data = {
        "computed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "period_days": 500,
        "data_points": len(df),
        "correlations": {},
    }
    for i, row_label in enumerate(corr_df.columns):
        for j, col_label in enumerate(corr_df.columns):
            if i < j:
                key = f"{row_label}_vs_{col_label}"
                corr_data["correlations"][key] = round(float(corr_df.values[i, j]), 4)

    json_path = os.path.join(RAW_DIR, "correlation_matrix.json")
    save_json(json_path, corr_data)

    # Also save individual series for reuse
    nvda_series = {"symbol": "NVDA", "period": "500d", "computed_at": corr_data["computed_at"], "data_points": len(nvda)}
    save_json(os.path.join(RAW_DIR, "nvda_500d_prices.json"), nvda_series)

    print("\n" + "=" * 60)
    print("✅ Build complete!")
    print(f"   Aligned data points: {len(df)}")
    print(f"   Correlation matrix saved to: raw_data/correlation_matrix.json")
    print(f"   Plots saved to: dashboard/plots/")
    print("=" * 60)

    # Output summary for subagent reporting
    print("\n--- SUMMARY ---")
    print(json.dumps(corr_data, indent=2))
    print("--- END SUMMARY ---")


if __name__ == "__main__":
    main()
