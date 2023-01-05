from bs4 import BeautifulSoup
import requests
import pandas as pd
import collections
collections.Callable = collections.abc.Callable
import Lib.urllib.request
import rdflib
from itertools import islice
import requests
import glob, os
import sys

from rdflib import Graph

def harvest_selected_id(idfile):
    my_file = open(idfile, "r")
    data = my_file.read()
    all_id = data.split("\n")
    data.split("\n")
    return all_id

def download_xml_single(all_id, full_path):
    new_id = all_id
    bf_files = glob.glob(full_path + '/single_xml/*')
    if len(bf_files) > 0:
        for f in bf_files:
            os.remove(f)
    num = 0
    for hid in new_id:
        weburl = "https://digitallibrary.sdsu.edu/oai2?verb=GetRecord&metadataPrefix=mods&identifier=oai:drupal-site.org:sdsu_" + hid
        page = requests.get(weburl)
        soup = BeautifulSoup(page.content, 'xml')
        fname = full_path + '/single_xml/' + str(hid) + ".xml"
        f = open(fname, "w", encoding="utf-8")
        f.write(soup.prettify())
        f.close()
        # if num // 100:
        #     time.sleep(5)
        print(num, ', id is: ', hid)
        num += 1
    return

def merge_xml(date, full_path):
    allf = []
    for filename in os.listdir(full_path + '/single_xml'):
        if not filename.endswith('.xml'):
            continue
        else:
            allf.append(full_path + '/single_xml/' + filename)
    allr = """<?xml version="1.0" encoding="utf-8"?><collection>"""
    for i in allf:
        with open(i, 'r', encoding="utf8") as f:
            s = f.read()
            r1 = s.index('<record>')
            r2 = s.index('</record>') + len("</record>")
            record = s[r1:r2]
            record = record.replace("> ", ">").replace(" <", "<")
            allr += record
    allr += """</collection>"""
    fn_new = full_path +"/merged_pre_upload/output" + str(date) + ".xml"
    with open(fn_new, "w", encoding="utf8") as fout:
        fout.write(allr)
    return

def go(idfile, full_path, date):
    all_id = harvest_selected_id(idfile)
    download_xml_single(all_id, full_path)
    merge_xml(date, full_path)
    print("edit in Oxygen")
    print("replace '> ' with '>'")
    print("replace' </' with '</'")
    print("""replace '<mods    xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-5.xsd">' with '<mods>'""")

if __name__ == "__main__":
    go(sys.argv[1], sys.argv[2], sys.argv[3])