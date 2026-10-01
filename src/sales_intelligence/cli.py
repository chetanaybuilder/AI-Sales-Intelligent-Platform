"""Command Line Interface for the Sales Intelligence Platform."""

import argparse
import logging
import sys
from typing import Optional

from .ai_advisor import AIAdvisor
from .analytics import compute_kpis
from .config import Config
from .data_loader import load_sales_data
from .report import print_dashboard

logger = logging.getLogger(__name__)


def main(args: Optional[list] = None) -> None:
    """Main entry point for CLI."""
    Config.setup_logging()

    parser = argparse.ArgumentParser(
        description="AI Sales Intelligence Platform - Enterprise E-Commerce Analytics"
    )
    parser.add_argument(
        "--file",
        type=str,
        default="data/sample_sales.csv",
        help="Path to the sales CSV file.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Analyze command
    subparsers.add_parser("analyze", help="Load data and just ensure it is valid")

    # Dashboard command
    subparsers.add_parser("dashboard", help="Print the business KPIs dashboard")

    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask the AI a business question")
    ask_parser.add_argument(
        "question", nargs="?", default="", help="Your question for the AI"
    )

    # Interactive chat command
    subparsers.add_parser("chat", help="Start an interactive chat session with the AI")

    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        sys.exit(0)

    try:
        df = load_sales_data(parsed_args.file)
        kpis = compute_kpis(df)
    except Exception as e:
        logger.error("Failed to process data: %s", e)
        sys.exit(1)

    if parsed_args.command == "analyze":
        print(f"Successfully loaded and analyzed {len(df)} records.")

    elif parsed_args.command == "dashboard":
        print_dashboard(kpis)

    elif parsed_args.command == "ask":
        if not parsed_args.question:
            print(
                'Please provide a question. Example: sales-ai ask "How can I increase revenue?"'
            )
            sys.exit(1)

        advisor = AIAdvisor()
        print("\nThinking...\n")
        response = advisor.ask(kpis, parsed_args.question)
        print("AI ADVISOR RESPONSE:")
        print("-" * 50)
        print(response)
        print("-" * 50)

    elif parsed_args.command == "chat":
        print_dashboard(kpis)
        advisor = AIAdvisor()
        print("\nWelcome to SalesMind AI Interactive Chat!")
        print("Type 'exit' or 'quit' to end the session.\n")

        while True:
            try:
                question = input("Ask me something about sales! > ")
                if question.strip().lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break
                if not question.strip():
                    continue

                response = advisor.ask(kpis, question)
                print(f"\n{response}\n")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break


if __name__ == "__main__":
    main()
