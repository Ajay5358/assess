import xml.etree.ElementTree as ET
from json_to_xml import convert_json_to_xml

def xml_to_str(elem):
    return ET.tostring(elem, encoding="unicode").replace("<null />", "<null/>")

def test_string_conversion():
    data = {"greeting": "hello"}
    xml = convert_json_to_xml(data)
    out = xml_to_str(xml)
    assert "<string name=\"greeting\">hello</string>" in out

def test_number_conversion():
    data = {"age": 25}
    xml = convert_json_to_xml(data)
    out = xml_to_str(xml)
    assert "<number name=\"age\">25</number>" in out

def test_boolean_conversion():
    data = {"flag": True}
    xml = convert_json_to_xml(data)
    out = xml_to_str(xml)
    assert "<boolean name=\"flag\">true</boolean>" in out

def test_null_conversion():
    data = {"missing": None}
    xml = convert_json_to_xml(data)
    out = xml_to_str(xml)
    assert "<null name=\"missing\"/>" in out

def test_array_conversion():
    data = {"values": [1, "abc", False, None]}
    xml = convert_json_to_xml(data)
    out = xml_to_str(xml)
    assert "<array name=\"values\">" in out
    assert "<number>1</number>" in out
    assert "<string>abc</string>" in out
    assert "<boolean>false</boolean>" in out
    assert "<null/>" in out

def test_nested_object():
    data = {"person": {"name": "Ajay", "age": 22}}
    xml = convert_json_to_xml(data)
    out = xml_to_str(xml)
    assert "<object name=\"person\">" in out
    assert "<string name=\"name\">Ajay</string>" in out
    assert "<number name=\"age\">22</number>" in out
