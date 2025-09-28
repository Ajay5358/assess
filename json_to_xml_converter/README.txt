JSON to XML Converter
=====================

This project converts arbitrary JSON data into XML format
according to the assignment specification.

-----------------
Usage
-----------------
    python convert.py input.json output.xml

If incorrect arguments are provided:
    python convert.py
    -> Prints usage message

-----------------
Requirements
-----------------
- Python 3.x
(No external libraries required)

-----------------
Build
-----------------
Install package:
    python setup.py install

Run directly with CLI entry point:
    json2xml input.json output.xml

-----------------
Tests
-----------------
Run all tests with:
    pytest tests/

-----------------
Example
-----------------
Input (input.json):
{
    "name": "Ajay",
    "age": 22,
    "is_student": true,
    "skills": ["python", null, 5]
}

Run:
    python convert.py input.json output.xml

Output (output.xml):
<?xml version="1.0" encoding="utf-8"?>
<object>
  <string name="name">Ajay</string>
  <number name="age">22</number>
  <boolean name="is_student">true</boolean>
  <array name="skills">
    <string>python</string>
    <null/>
    <number>5</number>
  </array>
</object>
