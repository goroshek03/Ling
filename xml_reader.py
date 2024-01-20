import xml.etree.ElementTree as ET

tree = ET.parse('xml/output.xml')

root = tree.getroot()


for child in root.iter('Person'):
    print(child.text)
