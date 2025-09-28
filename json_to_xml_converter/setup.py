from setuptools import setup, find_packages

setup(
    name="json_to_xml_converter",
    version="1.0",
    py_modules=["convert", "json_to_xml"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "json2xml=convert:main",
        ],
    },
)
