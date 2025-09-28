import sys, json
import xml.etree.ElementTree as ET
from json_to_xml import convert_json_to_xml, write_xml

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert.py input.json output.xml")
        sys.exit(1)

    input_file, output_file = sys.argv[1], sys.argv[2]

    with open(input_file, "r") as f:
        json_data = json.load(f)

    xml_root = convert_json_to_xml(json_data)
    tree = ET.ElementTree(xml_root)
    write_xml(tree, output_file)

if __name__ == "__main__":
    main()
