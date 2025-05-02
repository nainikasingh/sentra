# sentra/cli.py

import argparse
import netifaces
import ipaddress
import subprocess
import re
from core.engine.scanner_engine import ScannerEngine

def get_local_cidr():
    """
    Detect the IP and netmask of the default interface, and return CIDR format.
    Excludes loopback interfaces.
    """
    # Get the default gateway and its associated interface
    default_gateway = netifaces.gateways().get('default', {})
    default_iface = default_gateway.get(netifaces.AF_INET)

    if not default_iface:
        print("[!] Could not determine the default network interface.")
        return None, None

    iface_name = default_iface[1]  # Get the interface name
    try:
        iface_data = netifaces.ifaddresses(iface_name)[netifaces.AF_INET][0]
        ip = iface_data['addr']
        netmask = iface_data['netmask']
        cidr = convert_to_cidr(ip, netmask)
        return ip, cidr
    except (KeyError, IndexError):
        print(f"[!] Could not retrieve IP or netmask for interface: {iface_name}")
        return None, None

def convert_to_cidr(ip, netmask):
    """
    Convert an IP address and netmask to a CIDR subnet.
    """
    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
    return str(network)

def discover_live_hosts(cidr_block):
    """
    Perform host discovery using nmap -sn and return a list of live IPs.
    """
    print(f"[+] Discovering live hosts in {cidr_block} ...")
    try:
        result = subprocess.run(['nmap', '-sn', cidr_block], capture_output=True, text=True)
        live_hosts = []
        for line in result.stdout.splitlines():
            if "Nmap scan report for" in line:
                ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                if ip_match:
                    live_hosts.append(ip_match.group())
        print(f"[+] Live hosts found: {live_hosts}")
        return live_hosts
    except Exception as e:
        print(f"[!] Error during host discovery: {e}")
        return []

def main():
    """
    Main entry point for the script.
    Automatically detects the local CIDR, discovers live hosts, and scans them.
    """
    ip, cidr = get_local_cidr()
    if not ip or not cidr:
        print("[!] Could not determine local CIDR.")
        return

    print(f"[+] Local IP: {ip}")
    print(f"[+] Network CIDR: {cidr}")

    live_hosts = discover_live_hosts(cidr)
    if not live_hosts:
        print("[!] No live hosts found.")
        return

    print(f"[+] {len(live_hosts)} host(s) are up.")
    print("[+] Preparing to scan live hosts...")

    # Scan each live host
    for host in live_hosts:
        print(f"[+] Scanning host: {host}")
        scanner = ScannerEngine(host)
        result = scanner.run_scan()

        if result:
            print("[+] Raw scan complete.")
            scanner.parse_nmap_xml(result)
        else:
            print(f"[-] Scan failed or returned no output for host: {host}")

if __name__ == "__main__":
    main()
