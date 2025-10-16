import os
import json
import pandas as pd

def _load_lookup_data(lookup_dir):
    """Load and flatten all JSON lookup data, keeping the highest market value per card."""

    all_lookup_df = []

    for file in os.listdir(lookup_dir):
        if file.endswith(".json"):
            file_path = os.path.join(lookup_dir, file)

            with open(file_path, "r") as f:
                data = json.load(f)

            df = pd.json_normalize(data["data"])

            df = df.rename(columns={
                "id": "card_id",
                "name": "card_name",
                "number": "card_number",
                "set.id": "set_id",
                "set.name": "set_name"
            })

            df["card_market_value"] = (
                df.get("tcgplayer.prices.holofoil.market", pd.Series([0]*len(df)))
                .fillna(df.get("tcgplayer.prices.normal.market", 0))
                .fillna(0.0)
            )

            required_cols = [
                "card_id", "card_name", "card_number",
                "set_id", "set_name", "card_market_value"
            ]

            df = df[[col for col in required_cols if col in df.columns]]

            all_lookup_df.append(df.copy())

    if not all_lookup_df:
        print(f"No lookup files found in {lookup_dir}.")
        return pd.DataFrame(columns=[
            "card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"
        ])

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    lookup_df = (
        lookup_df.sort_values("card_market_value", ascending=False)
        .drop_duplicates(subset=["card_id"], keep="first")
    )

    print("Loaded lookup columns:", lookup_df.columns.tolist()) 

    return lookup_df


import os
import pandas as pd

def _load_inventory_data(inventory_dir):
    """Load all binder CSVs and create unified card_id key."""

    inventory_data = []

    for file in os.listdir(inventory_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(inventory_dir, file)
            df = pd.read_csv(file_path)
            inventory_data.append(df)

    if not inventory_data:
        print(f"No inventory files found in {inventory_dir}.")
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_data, ignore_index=True)

    inventory_df["card_id"] = (
        inventory_df["set_id"].astype(str) + "-" + inventory_df["card_number"].astype(str)
    )

    print("Loaded inventory columns:", inventory_df.columns.tolist())  # DEBUG

    return inventory_df

import sys
import pandas as pd

def update_portfolio(inventory_dir, lookup_dir, output_file):
    """Main ETL controller — merges lookup and inventory data into final portfolio CSV."""

    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    print("Loaded lookup columns:", lookup_df.columns.tolist())
    print("Loaded inventory columns:", inventory_df.columns.tolist())

    if inventory_df.empty:
        print("No inventory data found.", file=sys.stderr)
        empty_cols = [
            "index", "card_id", "card_name", "card_number",
            "set_id", "set_name", "binder_name",
            "page_number", "slot_number", "card_market_value"
        ]
        pd.DataFrame(columns=empty_cols).to_csv(output_file, index=False)
        return

    required_cols = [
        "card_id", "card_name", "card_number",
        "set_id", "set_name", "card_market_value"
    ]
    for col in required_cols:
        if col not in lookup_df.columns:
            lookup_df[col] = None  

    print("Merging inventory_df and lookup_df...")
    portfolio_df = pd.merge(
        inventory_df,
        lookup_df[required_cols],
        on="card_id",
        how="left",
        suffixes=("_inv", "_look")
    )

    print("Resulting portfolio_df columns:", portfolio_df.columns.tolist())

    portfolio_df["card_market_value"] = portfolio_df["card_market_value"].fillna(0.0)
    portfolio_df["set_name"] = portfolio_df["set_name"].fillna("NOT_FOUND")

    portfolio_df["card_name"] = portfolio_df["card_name_look"].combine_first(portfolio_df["card_name_inv"])
    portfolio_df["card_number"] = portfolio_df["card_number_look"].combine_first(portfolio_df["card_number_inv"])
    portfolio_df["set_id"] = portfolio_df["set_id_look"].combine_first(portfolio_df["set_id_inv"])

    portfolio_df["index"] = (
        portfolio_df["binder_name"].astype(str) + "_" +
        portfolio_df["page_number"].astype(str) + "_" +
        portfolio_df["slot_number"].astype(str)
    )

    final_cols = [
        "index", "card_id", "card_name", "card_number",
        "set_id", "set_name", "binder_name",
        "page_number", "slot_number", "card_market_value"
    ]

    portfolio_df[final_cols].to_csv(output_file, index=False)

    print(f"Portfolio successfully written to {output_file}")

def main():
    """
    Runs the production version of the pipeline.
    Uses production inventory and lookup directories.
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
    print("Starting Pokémon Update Script in Test Mode...")
    test()


