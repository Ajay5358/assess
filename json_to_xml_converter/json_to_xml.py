import xml.etree.ElementTree as ET

def json_to_xml_element(key, value):
    """Convert a JSON value into an XML element according to the spec."""

    if isinstance(value, dict):  # Object
        elem = ET.Element("object")
        for k, v in value.items():
            child = json_to_xml_element(k, v)
            child.set("name", k)
            elem.append(child)
        return elem

    elif isinstance(value, list):  # Array
        elem = ET.Element("array")
        for item in value:
            child = json_to_xml_element(None, item)
            elem.append(child)
        return elem

    elif isinstance(value, str):  # String
        elem = ET.Element("string")
        elem.text = value
        return elem

    elif isinstance(value, bool):  # Boolean
        elem = ET.Element("boolean")
        elem.text = "true" if value else "false"
        return elem

    elif isinstance(value, (int, float)):  # Number
        elem = ET.Element("number")
        elem.text = str(value)
        return elem

    elif value is None:  # Null → enforce <null/>
        elem = ET.Element("null")
        elem.text = None
        return elem

    else:
        raise TypeError(f"Unsupported JSON type: {type(value)}")


def convert_json_to_xml(json_data):
    """Convert full JSON (must be object or array at top level)."""
    if not isinstance(json_data, (dict, list)):
        raise ValueError("Top-level JSON must be an object or array.")
    return json_to_xml_element(None, json_data)


# ---------------- Pretty Printing ----------------
def indent(elem, level=0):
    """Helper function to add indentation for pretty printing."""
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def write_xml(tree, output_file):
    """Write XML with pretty formatting and <null/> enforcement."""
    root = tree.getroot()
    indent(root)  # apply indentation
    xml_str = ET.tostring(root, encoding="unicode")
    xml_str = xml_str.replace("<null />", "<null/>")  # enforce <null/>
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(xml_str)
