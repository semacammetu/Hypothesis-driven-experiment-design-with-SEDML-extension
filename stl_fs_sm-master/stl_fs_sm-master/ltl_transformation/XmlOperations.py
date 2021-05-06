import xml.etree.ElementTree as ET

from numpy import float64


def d2x(data):
    d = []
    for i, row in data.iterrows():
        xml = ['<item>']
        for field in row.index:
            xml.append('<field name="{0}">{1}</field>'.format(field, row[field]))
        xml.append('</item>'.join('\n'))
        d.append('\n'.join(xml))
    return d


def writeDatasetsToXml(xml):
    root = ET.Element("data")
    for data in xml:
        doc = ET.SubElement(root, "set")
        for i, row in data.iterrows():
            item = ET.SubElement(doc, "field")
            for field in row.index:
                ET.SubElement(item, "item", name=field).text = str(float64(row[field]))
    tree = ET.ElementTree(root)
    indent(root)
    # writing xml
    tree.write("data.xml", encoding="utf-8", xml_declaration=True)


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
