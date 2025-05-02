# sentra/core/engine/scanner_engine.py

import subprocess
import xml.etree.ElementTree as ET

class ScannerEngine:
    def __init__(self, target):
        self.target = target

    def run_scan(self):
        try:
            result = subprocess.run(
                ["nmap", "-sV", "-oX", "-", self.target],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"[ERROR] Nmap failed: {result.stderr}")
                return None

            return result.stdout

        except Exception as e:
            print(f"[ERROR] Exception occurred: {e}")
            return None

    def parse_nmap_xml(self, xml_output):
        try:
            root = ET.fromstring(xml_output)
            for host in root.findall('host'):
                addr = host.find('address').attrib.get('addr')
                print(f"[+] Host: {addr}")
                ports = host.find('ports')
                if ports is not None:
                    for port in ports.findall('port'):
                        portid = port.attrib.get('portid')
                        protocol = port.attrib.get('protocol')
                        service = port.find('service')
                        service_name = service.attrib.get('name') if service is not None else "unknown"
                        print(f"    - Port {portid}/{protocol}: {service_name}")
        except ET.ParseError as e:
            print(f"[ERROR] Failed to parse Nmap XML: {e}")
