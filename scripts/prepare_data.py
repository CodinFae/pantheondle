import argparse
import pyarrow
from ast import arg

import pandas as pd
from pathlib import Path


def prepare_data(input_path: Path, output_dir: Path):
    print(f"Reading {input_path} and saving to {output_dir}/persons.parquet")
    df = pd.read_csv(input_path)

    print(f"Loaded {len(df)} persons")
    df = df[~df["alive"]]
    df = df[pd.notna(df["dplace_name"])]
    df = df[pd.notna(df["bplace_name"])]
    df = df[pd.notna(df["bplace_lat"])]
    df = df[pd.notna(df["dplace_lat"])]

    print(f"Kept {len(df)}")

    output_path = output_dir / "persons.parquet"
    df.to_parquet(output_path, index=False)
    print(f"Saved file to {output_path}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the Pantheondle dataset")

    parser.add_argument("input", type=Path, help="Path to the CSV of the pantheon dataset")
    parser.add_argument("output", type=Path, help="Path to the output directory")
    args = parser.parse_args()

    prepare_data(args.input, args.output)

if __name__ == "__main__":
    main()
