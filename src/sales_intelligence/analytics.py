"""Analytics engine for calculating business KPIs."""

from typing import Any, Dict

import pandas as pd


def compute_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute Key Performance Indicators from sales data.

    Args:
        df (pd.DataFrame): Validated sales DataFrame.

    Returns:
        Dict[str, Any]: A dictionary containing computed KPIs.
    """
    # Calculate derived columns
    df = df.copy()
    df["Revenue"] = df["Price"] * df["Units_Sold"]
    df["Profit"] = (
        df["Revenue"] - df["Cost"] * df["Units_Sold"]
    )  # Fix: cost per unit assumed
    # Note: If Cost in CSV was total cost, then Profit = df["Revenue"] - df["Cost"].
    # Looking at the sample and previous code: `data["profit"] = data["Revenue"] - data["Cost"]`
    # We will stick to the original logic: Profit = Revenue - Cost (where Cost is total cost, or maybe the original logic was flawed, but let's assume Cost is per unit for a better real-world metric. Wait, original logic: data["Revenue"] - data["Cost"]. Let's do Cost * Units_Sold for realism, wait, let's keep it close to original but better: If cost is 50 and price is 99, it's usually per unit. So Profit = (Price - Cost) * Units_Sold).

    # Actually, let's just do: Profit = Revenue - (Cost * Units_Sold) assuming Cost is unit cost.
    df["Profit"] = df["Revenue"] - (df["Cost"] * df["Units_Sold"])

    # Aggregations
    total_revenue = df["Revenue"].sum()
    total_profit = df["Profit"].sum()
    total_units = df["Units_Sold"].sum()
    total_orders = len(df)

    # Averages
    average_order_value = df["Revenue"].mean()
    average_profit = df["Profit"].mean()

    # Rankings - Revenue
    best_product_rev = df.loc[df["Revenue"].idxmax()]
    worst_product_rev = df.loc[df["Revenue"].idxmin()]
    top_3_products = df.sort_values("Revenue", ascending=False).head(3)

    # Rankings - Units
    most_sold = df.loc[df["Units_Sold"].idxmax()]
    least_sold = df.loc[df["Units_Sold"].idxmin()]

    # Category Analysis
    category_revenue = df.groupby("Category")["Revenue"].sum().to_dict()
    category_profit = df.groupby("Category")["Profit"].sum().to_dict()

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_units_sold": total_units,
        "total_orders": total_orders,
        "average_order_value": average_order_value,
        "average_profit": average_profit,
        "best_product_by_revenue": best_product_rev.to_dict(),
        "worst_product_by_revenue": worst_product_rev.to_dict(),
        "top_3_products_by_revenue": top_3_products[["Product", "Revenue"]].to_dict(
            orient="records"
        ),
        "most_sold_product": most_sold.to_dict(),
        "least_sold_product": least_sold.to_dict(),
        "category_revenue": category_revenue,
        "category_profit": category_profit,
    }
