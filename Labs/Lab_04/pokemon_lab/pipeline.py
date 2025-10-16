import sys
from update_portfolio import main as update_portfolio_main
from generate_summary import main as generate_summary_main


def run_production_pipeline():
    """
    Runs the full production data pipeline.
    """
    print("=== Starting Full Pokemon Portfolio Pipeline ===", file=sys.stderr)

    # --- ETL Step ---
    print("[1/2] Running update_portfolio (ETL)...", file=sys.stderr)
    update_portfolio_main()

    # --- Reporting Step ---
    print("[2/2] Running generate_summary (Reporting)...", file=sys.stderr)
    generate_summary_main()

    print("=== Pokemon Portfolio Pipeline Completed Successfully ===", file=sys.stderr)


if __name__ == "__main__":
    run_production_pipeline()

