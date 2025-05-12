#!/usr/bin/env python3

import argparse
from sentra.core.scanner import stealth_scan
from termcolor import colored

def main():
    parser = argparse.ArgumentParser(description="Sentra CLI for network scanning.")
    parser.add_argument("--target", required=True, help="Target IP or CIDR to scan.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    target = args.target

    try:
        result = stealth_scan(target)
        if result["error"]:
            print(colored(f"Error: {result['error']}", "red"))
        else:
            if args.verbose:
                print(colored(f"Full Scan Output:\n{result['output']}", "green"))
            else:
                print(colored(f"Scan Summary:\n{result['output'][:100]}...", "green"))
    except ValueError as e:
        print(colored(f"Invalid Input: {e}", "red"))
    except Exception as e:
        print(colored(f"Unexpected Error: {e}", "red"))

if __name__ == "__main__":
    main()