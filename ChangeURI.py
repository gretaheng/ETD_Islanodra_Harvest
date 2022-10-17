import sys
import xml.etree.ElementTree as ET

def go(fp):
    tree = ET.parse(fp, outputp)
    for child in tree.getroot():
        f_id = child.find("./header/identifier").text.replace("oai:drupal-site.org:sdsu_", "")
        uri = "https://digitallibrary.sdsu.edu/islandora/object/sdsu%3A" + f_id
        urielement = child.findall("./metadata/mods/identifier[@type = 'uri']")
        if (len(urielement) > 0):
            urielement[0].text = uri
        else:
            mods = child.find("./metadata/mods")
            ue = ET.SubElement(mods, "identifier", type="uri")
            ue.text = uri
    tree.write('outputp')

if __name__ == "__main__":
    go(sys.argv[1], sys.argv[2])
