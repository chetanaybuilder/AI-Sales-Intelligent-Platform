"""Reporting and terminal dashboard rendering."""

from typing import Any, Dict


def print_dashboard(kpis: Dict[str, Any]) -> None:
    """
    Print a formatted dashboard of the business KPIs to the terminal.

    Args:
        kpis (Dict[str, Any]): Dictionary of computed KPIs.
    """
    print("=" * 60)
    print(" AI SALES INTELLIGENCE DASHBOARD")
    print("=" * 60)

    print("\nFINANCIAL OVERVIEW")
    print("-" * 30)
    print(f"Total Revenue:      ${kpis['total_revenue']:,.2f}")
    print(f"Total Profit:       ${kpis['total_profit']:,.2f}")
    print(f"Average Order:      ${kpis['average_order_value']:,.2f}")
    print(f"Average Profit:     ${kpis['average_profit']:,.2f}")

    print("\nVOLUME METRICS")
    print("-" * 30)
    print(f"Total Orders:       {kpis['total_orders']}")
    print(f"Total Units Sold:   {kpis['total_units_sold']}")

    print("\nPRODUCT RANKINGS")
    print("-" * 30)
    best_rev = kpis["best_product_by_revenue"]
    worst_rev = kpis["worst_product_by_revenue"]
    most_sold = kpis["most_sold_product"]
    least_sold = kpis["least_sold_product"]

    print(f"Best by Revenue:    {best_rev['Product']} (${best_rev['Revenue']:,.2f})")
    print(f"Worst by Revenue:   {worst_rev['Product']} (${worst_rev['Revenue']:,.2f})")
    print(
        f"Most Sold:          {most_sold['Product']} ({most_sold['Units_Sold']} units)"
    )
    print(
        f"Least Sold:         {least_sold['Product']} ({least_sold['Units_Sold']} units)"
    )

    print("\nTOP 3 PRODUCTS BY REVENUE")
    print("-" * 30)
    for idx, prod in enumerate(kpis["top_3_products_by_revenue"], 1):
        print(f"{idx}. {prod['Product']:<20} - ${prod['Revenue']:,.2f}")

    print("\nCATEGORY BREAKDOWN")
    print("-" * 30)
    for cat, rev in kpis["category_revenue"].items():
        prof = kpis["category_profit"].get(cat, 0)
        print(f"{cat:<15} Rev: ${rev:<10,.2f} Prof: ${prof:,.2f}")

    print("=" * 60)
