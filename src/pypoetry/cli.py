# src/pypoetry/cli.py

import argparse
from .cyth.hello_world import hello

def main():
    parser = argparse.ArgumentParser(description="A simple CLI for pypoetry.")

    # Define arguments
    parser.add_argument(
        "--name",
        default="World",
        help="Name to greet (default: 'World')"
    )

    # Parse arguments
    args = parser.parse_args()

    # Print greeting
    print(f"Hello, {args.name}!")

    print(f"{hello()}")

if __name__ == "__main__":
    main()
