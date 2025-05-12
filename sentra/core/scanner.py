import subprocess
import re
import csv
from typing import Dict

def stealth_scan(target: str) -> Dict[str, str]:
    """
    Perform a stealth scan on the target IP address.

    - Uses ARP ping (`-PR -sn`) for private IPs (192.168.x.x, 10.x.x.x).
    - Uses SYN scan (`-PS -T2 --randomize-hosts`) for public IPs.
    - Returns a dictionary with keys `output` and `error`.

    Args:
        target (str): The target IP address to scan.

    Returns:
        dict: A dictionary containing the scan output and error messages.

    Raises:
        ValueError: If the target IP address is invalid.
    """
    # Validate the IP address
    private_ip_pattern = re.compile(r'^(192\.168\.|10\.)')
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

    if not ip_pattern.match(target):
        raise ValueError(f"Invalid IP address: {target}")

    # Determine scan type
    if private_ip_pattern.match(target):
        scan_type = "-A"
    else:
        scan_type = "-PS -T2 --randomize-hosts"

    # Execute the scan
    try:
        result = subprocess.run(
            ["nmap", scan_type, target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300,
            text=True,
        )
        return {
            "output": result.stdout,  # Return the full output
            "error": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"output": "", "error": "Scan timed out after 300 seconds."}
    except Exception as e:
        return {"output": "", "error": str(e)}

RISK_MAP = {
    "ssh": "Medium",
    "http": "Medium",
    "https": "Low",
    "telnet": "High",
    "ftp": "High",
    "rdp": "High",
}

def parse_nmap_to_csv(nmap_output: str, output_file: str):
    """
    Parse Nmap output and save results to a CSV file.

    Args:
        nmap_output (str): Raw Nmap output as a string.
        output_file (str): Path to the output CSV file.
    """
    results = []
    current_ip = None
    for line in nmap_output.splitlines():
        if line.startswith("Nmap scan report for"):
            current_ip = line.split()[-1]
        elif re.match(r"^\d+/tcp\s+open", line):
            parts = line.split()
            port_proto = parts[0]
            port, proto = port_proto.split('/')
            state = parts[1]
            service = parts[2] if len(parts) > 2 else "unknown"
            risk = RISK_MAP.get(service.lower(), "Unknown")
            note = f"{service.upper()} detected"
            results.append([current_ip, port, proto, state, service, risk, note])

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "Port", "Protocol", "State", "Service", "Risk", "Notes"])
        writer.writerows(results)

def save_scan_to_csv(target: str, output_file: str):
    """
    Perform a scan on the target and save the results to a CSV file.

    Args:
        target (str): The target IP address to scan.
        output_file (str): Path to the output CSV file.
    """
    scan_result = stealth_scan(target)
    if scan_result["error"]:
        print(f"Error during scan: {scan_result['error']}")
        return

    # Parse the scan output to CSV
    parse_nmap_to_csv(scan_result["output"], output_file)
