#!/usr/bin/env python3
"""
generate_summary.py
--------------------
Reads a completed Pokémon card portfolio CSV and prints summary statistics:
- Total market value
- Most valuable card (name, ID, and value)
"""

import os
import sys
import pandas as pd


def generate_summary(portfolio_file):
    """Reads a portfolio CSV and prints key summary statistics."""

    if not os.path.exists(portfolio_file):
        print(f"Error: File '{portfolio_file}' not found.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print("The portfolio file is empty — nothing to summarize.")
        return

    total_portfolio_value = df["card_market_value"].sum()

    max_index = df["card_market_value"].idxmax()
    most_valuable_card = df.loc[max_index]

    print("\n=== Pokémon Card Portfolio Summary ===")
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print("\nMost Valuable Card:")
    print(f"  Name: {most_valuable_card['card_name']}")
    print(f"  ID: {most_valuable_card['card_id']}")
    print(f"  Market Value: ${most_valuable_card['card_market_value']:,.2f}")
    print("======================================\n")


def main():
    """Runs the summary using the production portfolio file."""
    print("Running summary for production portfolio...")
    generate_summary("card_portfolio.csv")


def test():
    """Runs the summary using the test portfolio file."""
    print("Running summary for test portfolio...")
    generate_summary("test_card_portfolio.csv")


if __name__ == "__main__":
    print("Starting Pokémon Portfolio Summary in Test Mode...", file=sys.stderr)
    test()
