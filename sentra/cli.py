# sentra/cli.py

import argparse
from core.engine.scanner_engine import ScannerEngine

def main():
    parser = argparse.ArgumentParser(description="Sentra - Network Recon Tool")
    parser.add_argument("--target", required=True, help="Target IP or hostname")

    args = parser.parse_args()

    print(f"[+] Target acquired: {args.target}")
    scanner = ScannerEngine(args.target)
    result = scanner.run_scan()

    if result:
        print("[+] Raw scan complete.")
        scanner.parse_nmap_xml(result)  # Call the XML parsing function
    else:
        print("[-] Scan failed or returned no output.")

if __name__ == "__main__":
    main()
