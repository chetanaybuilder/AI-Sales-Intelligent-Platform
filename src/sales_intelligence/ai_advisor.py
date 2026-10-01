"""AI Advisor integration using Google Gemini."""

import logging
from typing import Any, Dict

from google import genai
from google.genai.errors import APIError

from .config import Config

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are SalesMind AI, an elite E-commerce Sales Intelligence Consultant.

Your job is to analyze sales data and help business owners increase revenue, profit, and business growth.

Rules:
• Always answer professionally.
• Give practical business advice, not generic AI responses.
• Base every recommendation on the provided sales data summary.
• Explain WHY a product performs well or poorly.
• Suggest ways to increase revenue and profit.
• Identify best-selling and worst-selling products based on the data.
• Recommend marketing, pricing, inventory, bundling, discounts, and upselling strategies.
• If data is insufficient, clearly say what additional data is needed.
• Never invent numbers that are not present in the dataset.
• Keep answers concise, actionable, and business-focused.
• Use bullet points whenever possible.
• Think like a senior business analyst working for a million-dollar e-commerce company.

Your goal is to help businesses make smarter decisions using data.
"""


class AIAdvisor:
    """Client for interacting with the AI advisor."""

    def __init__(self) -> None:
        """Initialize the AI Advisor with the Gemini client."""
        if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == "your_api_key_here":
            logger.warning(
                "GEMINI_API_KEY is missing or invalid. AI features will fail."
            )
            self.client = None
        else:
            self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def _build_context(self, kpis: Dict[str, Any]) -> str:
        """Build the context string from KPIs."""
        return f"""
        DATA SUMMARY:
        - Total Revenue: ${kpis["total_revenue"]:.2f}
        - Total Profit: ${kpis["total_profit"]:.2f}
        - Average Order Value: ${kpis["average_order_value"]:.2f}
        - Total Orders: {kpis["total_orders"]}
        - Total Units Sold: {kpis["total_units_sold"]}
        
        PRODUCT INSIGHTS:
        - Best by Revenue: {kpis["best_product_by_revenue"]["Product"]} (${kpis["best_product_by_revenue"]["Revenue"]:.2f})
        - Worst by Revenue: {kpis["worst_product_by_revenue"]["Product"]} (${kpis["worst_product_by_revenue"]["Revenue"]:.2f})
        - Most Sold: {kpis["most_sold_product"]["Product"]} ({kpis["most_sold_product"]["Units_Sold"]} units)
        - Least Sold: {kpis["least_sold_product"]["Product"]} ({kpis["least_sold_product"]["Units_Sold"]} units)
        
        CATEGORY REVENUE: {kpis["category_revenue"]}
        CATEGORY PROFIT: {kpis["category_profit"]}
        """

    def ask(self, kpis: Dict[str, Any], question: str) -> str:
        """
        Ask the AI advisor a business question based on the KPIs.

        Args:
            kpis (Dict[str, Any]): The computed business KPIs.
            question (str): The user's question.

        Returns:
            str: The AI's response.
        """
        if not self.client:
            return "Error: GEMINI_API_KEY is not configured properly."

        context = self._build_context(kpis)
        prompt = f"{SYSTEM_PROMPT}\n{context}\n\nUSER QUESTION: {question}"

        try:
            logger.info("Sending request to Gemini AI (%s)", Config.MODEL_NAME)
            response = self.client.models.generate_content(
                model=Config.MODEL_NAME, contents=prompt
            )
            return response.text
        except APIError as e:
            logger.error("Gemini API Error: %s", e)
            return f"API Error: Failed to communicate with AI. ({e})"
        except Exception as e:
            logger.error("Unexpected error during AI generation: %s", e)
            return f"An unexpected error occurred: {e}"
