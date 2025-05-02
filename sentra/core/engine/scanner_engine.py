# sentra/core/engine/scanner_engine.py

import subprocess
import xml.etree.ElementTree as ET

class ScannerEngine:
    def __init__(self, target):
        self.target = target

    def run_scan(self):
        try:
            result = subprocess.run(
                ["nmap", "-A", "--osscan-guess", "-oX", "-", self.target],
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
            discovered_ports = []
            for host in root.findall('host'):
                addr = host.find('address').attrib.get('addr')
                print(f"[+] Host: {addr}")
                ports = host.find('ports')
                if ports is not None:
                    for port in ports.findall('port'):
                        portid = int(port.attrib.get('portid'))
                        protocol = port.attrib.get('protocol')
                        service = port.find('service')
                        service_name = service.attrib.get('name') if service is not None else "unknown"
                        print(f"    - Port {portid}/{protocol}: {service_name}")
                        discovered_ports.append(portid)

            # Categorize the discovered ports
            categorized_ports = self.categorize_ports(discovered_ports)
            print("\n[+] Categorized Ports:")
            for category, ports in categorized_ports.items():
                print(f"  {category}: {ports}")

        except ET.ParseError as e:
            print(f"[ERROR] Failed to parse Nmap XML: {e}")

    def categorize_ports(self, ports):
        categories = {
            'Web Services': [80, 443, 8080],
            'Database Services': [3306, 5432, 27017],
            'Email Services': [25, 587, 465],
            'File Transfer Services': [21, 22],
            'Remote Access': [22, 3389],
        }

        categorized = {
            'Web Services': [],
            'Database Services': [],
            'Email Services': [],
            'File Transfer Services': [],
            'Remote Access': [],
        }

        for port in ports:
            for category, port_list in categories.items():
                if port in port_list:
                    categorized[category].append(port)
                    break

        return categorized
