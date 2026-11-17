'''Copyright 2026 Seleah O'Connor

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://apache.org

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''

import argparse
from pathlib import Path
import csv

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process a CSV file path from the command line."
    )
    parser.add_argument(
        "csv_path",
        help="Path to the input CSV file",
        type=Path,
    )

    args = parser.parse_args()

    if not args.csv_path.exists():
        parser.error(f"input file not found: {args.csv_path}")
    if not args.csv_path.is_file():
        parser.error(f"not a file: {args.csv_path}")

    return args

def main() -> None:
    args = parse_args()
    with args.csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        print(reader.fieldnames)
    print(f"Received CSV path: {args.csv_path}")

if __name__ == "__main__":
    main()