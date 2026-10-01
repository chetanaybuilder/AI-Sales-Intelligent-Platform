"""Tests for the analytics module."""

import pandas as pd

from sales_intelligence.analytics import compute_kpis


def test_compute_kpis():
    """Test KPI computation with mock data."""
    data = {
        "Product": ["Prod A", "Prod B"],
        "Category": ["Cat 1", "Cat 2"],
        "Price": [10.0, 20.0],
        "Units_Sold": [5, 2],
        "Cost": [5.0, 10.0],
    }
    df = pd.DataFrame(data)

    kpis = compute_kpis(df)

    # Revenue: A=50, B=40 -> Total=90
    assert kpis["total_revenue"] == 90.0

    # Cost: A=25, B=20 -> Profit A=25, B=20 -> Total Profit=45
    assert kpis["total_profit"] == 45.0

    assert kpis["total_units_sold"] == 7
    assert kpis["total_orders"] == 2
    assert kpis["average_order_value"] == 45.0  # (50+40)/2
    assert kpis["average_profit"] == 22.5  # (25+20)/2

    assert kpis["best_product_by_revenue"]["Product"] == "Prod A"
    assert kpis["worst_product_by_revenue"]["Product"] == "Prod B"
    assert kpis["most_sold_product"]["Product"] == "Prod A"
    assert kpis["least_sold_product"]["Product"] == "Prod B"

    assert kpis["category_revenue"]["Cat 1"] == 50.0
    assert kpis["category_revenue"]["Cat 2"] == 40.0
