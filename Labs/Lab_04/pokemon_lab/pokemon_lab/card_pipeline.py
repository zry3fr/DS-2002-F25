import os
import sys
import json
import pandas as pd

def _load_lookup_data(lookup_dir):
    """Load all card lookup data from JSON files into a DataFrame."""
    all_data = []
    for file in os.listdir(lookup_dir):
        if file.endswith(".json"):
            file_path = os.path.join(lookup_dir, file)
            with open(file_path, "r") as f:
                data = json.load(f).get("data", [])
                for card in data:
                    card_id = card.get("id")
                    card_name = card.get("name")
                    card_number = card.get("number")
                    set_info = card.get("set", {})
                    set_id = set_info.get("id", "")
                    set_name = set_info.get("name", "")
                    prices = card.get("tcgplayer", {}).get("prices", {})
                    market_value = None
                    if "holofoil" in prices:
                        market_value = prices["holofoil"].get("market")
                    elif "normal" in prices:
                        market_value = prices["normal"].get("market")
                    all_data.append({
                        "card_id": card_id,
                        "card_name": card_name,
                        "card_number": card_number,
                        "set_id": set_id,
                        "set_name": set_name,
                        "card_market_value": market_value
                    })
    df = pd.DataFrame(all_data)
    print("Loaded lookup columns:", list(df.columns))
    return df

def _load_inventory_data(inventory_dir):
    """Load all inventory CSV files into a DataFrame."""
    csv_files = [f for f in os.listdir(inventory_dir) if f.endswith(".csv")]
    if not csv_files:
        print(f"No inventory files found in {inventory_dir}.")
        return pd.DataFrame()

    dfs = []
    for file in csv_files:
        df = pd.read_csv(os.path.join(inventory_dir, file))
        dfs.append(df)
    inventory_df = pd.concat(dfs, ignore_index=True)
    inventory_df["card_id"] = inventory_df["set_id"] + "-" + inventory_df["card_number"].astype(str)
    print("Loaded inventory columns:", list(inventory_df.columns))
    return inventory_df

def update_portfolio(inventory_dir, lookup_dir, output_file):
    """Main ETL/Loading logic."""
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    if inventory_df.empty:
        print("Error: Inventory data is empty.", file=sys.stderr)
        empty_cols = [
            "index","card_id","card_name","card_number","set_id",
            "set_name","binder_name","page_number","slot_number","card_market_value"
        ]
        pd.DataFrame(columns=empty_cols).to_csv(output_file, index=False)
        return

    print("Merging inventory_df and lookup_df...")
    portfolio_df = pd.merge(inventory_df, lookup_df, on="card_id", how="left", suffixes=("_inv", "_look"))
    print("Resulting portfolio_df columns:", list(portfolio_df.columns))

    portfolio_df["card_name"] = portfolio_df["card_name_look"].combine_first(portfolio_df["card_name_inv"])
    portfolio_df["card_number"] = portfolio_df["card_number_look"].combine_first(portfolio_df["card_number_inv"])
    portfolio_df["set_id"] = portfolio_df["set_id_look"].combine_first(portfolio_df["set_id_inv"])
    portfolio_df["set_name"] = portfolio_df["set_name"].fillna("NOT_FOUND")
    portfolio_df["card_market_value"] = portfolio_df["card_market_value"].fillna(0.0)

    portfolio_df["index"] = (
        portfolio_df["binder_name"].astype(str)
        + "_"
        + portfolio_df["page_number"].astype(str)
        + "_"
        + portfolio_df["slot_number"].astype(str)
    )

    final_cols = [
        "index","card_id","card_name","card_number","set_id",
        "set_name","binder_name","page_number","slot_number","card_market_value"
    ]
    portfolio_df[final_cols].to_csv(output_file, index=False)
    print(f"Portfolio successfully written to {output_file}")

def main():
    """
    Runs the full production pipeline.
    Uses real inventory and lookup directories.
    """
    print("Running production portfolio update...")
    update_portfolio(
        inventory_dir="./card_inventory",
        lookup_dir="./card_set_lookup",
        output_file="card_portfolio.csv"
    )

def test():
    """
    Runs the test version of the pipeline.
    Uses test inventory and lookup directories.
    """
    print("Running test portfolio update...")
    update_portfolio(
        inventory_dir="./card_inventory_test",
        lookup_dir="./card_set_lookup_test",
        output_file="test_card_portfolio.csv"
    )

if __name__ == "__main__":
    # test()
    main()

import sys

if __name__ == "__main__":
    print("Starting Pokémon Card Pipeline in Test Mode...", file=sys.stderr)

    test()


    

