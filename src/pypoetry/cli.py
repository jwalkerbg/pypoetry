# src/pypoetry/cli.py

import argparse

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

if __name__ == "__main__":
    main()
