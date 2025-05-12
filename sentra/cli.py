#!/usr/bin/env python3
# sentra/cli.py

import argparse
import ipaddress
import json
import logging
import netifaces
import os
import random
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{os.path.expanduser('~')}/sentra.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("sentra")

# Constants
MAX_WORKERS = 10  # Thread pool size
SCAN_TIMEOUT = 300  # Seconds

def get_local_cidr() -> Tuple[Optional[str], Optional[str]]:
    """Detect the IP and CIDR of the default interface."""
    try:
        default_gateway = netifaces.gateways().get('default', {}).get(netifaces.AF_INET)
        if not default_gateway:
            logger.warning("No default IPv4 gateway found")
            return None, None

        iface_name = default_gateway[1]
        iface_data = netifaces.ifaddresses(iface_name)[netifaces.AF_INET][0]
        network = ipaddress.IPv4Network(
            f"{iface_data['addr']}/{iface_data['netmask']}", 
            strict=False
        )
        return iface_data['addr'], str(network)
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"CIDR detection failed: {e}", exc_info=True)
        return None, None

def discover_live_hosts(cidr_block: str) -> List[str]:
    """Perform hybrid host discovery (ARP for local, SYN for remote)."""
    network = ipaddress.IPv4Network(cidr_block)
    scan_type = "-PR" if network.is_private else "-PS"  # ARP for LAN, SYN for WAN
    
    try:
        cmd = [
            "nmap",
            scan_type,
            "-sn",  # Ping scan
            "-n",  # No DNS resolution
            "--disable-arp-ping",  # Force specified scan type
            cidr_block
        ]
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=SCAN_TIMEOUT
        )
        return re.findall(r"\d+\.\d+\.\d+\.\d+", result.stdout)
    except subprocess.TimeoutExpired:
        logger.error("Host discovery timed out (network defenses may be active)")
        return []
    except Exception as e:
        logger.error(f"Host discovery failed: {e}", exc_info=True)
        return []

def scan_hosts(hosts: List[str]) -> Dict[str, dict]:
    """Conduct parallel scans on discovered hosts."""
    from core.engine.scanner_engine import ScannerEngine  # Lazy import
    
    results = {}
    random.shuffle(hosts)  # Avoid predictable patterns
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(ScannerEngine(host).run_scan): host 
            for host in hosts
        }
        
        for future in as_completed(futures):
            host = futures[future]
            try:
                results[host] = future.result()
            except Exception as e:
                logger.error(f"Scan failed for {host}: {e}")
    
    return results

def save_results(results: dict, output_format: str = "json") -> str:
    """Save scan results to file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sentra_scan_{timestamp}.{output_format}"
    
    try:
        if output_format == "json":
            with open(filename, "w") as f:
                json.dump(results, f, indent=2)
        elif output_format == "csv":
            # Implement CSV conversion here
            raise NotImplementedError("CSV export coming soon")
        else:
            raise ValueError(f"Unsupported format: {output_format}")
        
        logger.info(f"Results saved to {filename}")
        return filename
    except Exception as e:
        logger.error(f"Failed to save results: {e}", exc_info=True)
        raise

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Sentra Network Auditor")
    parser.add_argument(
        "--output-format",
        choices=["json", "csv"],
        default="json",
        help="Output file format (default: json)"
    )
    parser.add_argument(
        "--stealth",
        action="store_true",
        help="Enable MAC randomization and slow timing"
    )
    return parser.parse_args()

def main():
    """Main execution flow."""
    args = parse_args()
    logger.info("Starting Sentra network audit")
    
    # Network detection
    local_ip, cidr = get_local_cidr()
    if not cidr:
        logger.critical("Failed to detect network configuration. Exiting.")
        return
    
    logger.info(f"Local IP: {local_ip}")
    logger.info(f"Network CIDR: {cidr}")
    
    # Host discovery
    live_hosts = discover_live_hosts(cidr)
    if not live_hosts:
        logger.warning("No live hosts detected")
        return
    
    logger.info(f"Discovered {len(live_hosts)} hosts: {', '.join(live_hosts)}")
    
    # Scanning
    logger.info("Beginning host scans...")
    scan_results = scan_hosts(live_hosts)
    
    # Output
    try:
        save_results(scan_results, args.output_format)
    except Exception:
        logger.critical("Failed to save results")

if __name__ == "__main__":
    main()
