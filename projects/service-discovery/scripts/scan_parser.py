import sys
import xml.etree.ElementTree as ET

if len(sys.argv) < 2:
	print("Usage: python3 scan_parser.py <scan.xml>")
	sys.exit()

try:
	tree = ET.parse(sys.argv[1])

except FileNotFoundError:
	print("Error: File does not exist.")
	sys.exit()
except ET.ParseError:
	print("Error: File is not valid XML.")
	sys.exit()

root = tree.getroot()

ports = root.findall(".//port")

for port in ports:
	protocol = port.get("protocol")
	port_id = port.get("portid")
	state_element = port.find("state")
	state = state_element.get("state")

	service_element = port.find("service")
	if service_element is not None:
		service = service_element.get("name")
		product = service_element.get("product", "Unknown")
		version = service_element.get("version", "Unknown")
	else:
		service = "Unknown"
		product = "Unknown"
		version = "Unknown"

	print(f"{protocol}/{port_id} - {state} - {service} - {product} - {version}")
