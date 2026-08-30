import argparse
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def prepare_data(input_path: Path, output_dir: Path) -> None:
    df = pd.read_csv(input_path)
    logger.info(f"Loaded {len(df)} persons")
    df = df[~df["alive"]]
    df = df[pd.notna(df["dplace_name"])]
    df = df[pd.notna(df["bplace_name"])]
    df = df[pd.notna(df["bplace_lat"])]
    df = df[pd.notna(df["dplace_lat"])]
    logger.info(f"{len(df)} persons remaining")

    output_path = output_dir / "persons.parquet"
    df.to_parquet(output_path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the Pantheondle dataset")

    parser.add_argument(
        "input", type=Path, help="Path to the CSV of the pantheon dataset"
    )
    parser.add_argument("output", type=Path, help="Path to the output directory")
    args = parser.parse_args()

    prepare_data(args.input, args.output)


if __name__ == "__main__":
    main()
