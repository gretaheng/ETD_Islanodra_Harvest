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

def harvest_id(pagenum):
    pagenum = int(pagenum)
    all_id = []
    num = 0
    webbase = "https://fake?page="
    while num < pagenum:
        weburl = webbase + str(num)
        page = requests.get(weburl)
        soup = BeautifulSoup(page.content, 'html.parser')
        box = soup.find_all("dt", class_="islandora-object-thumb")
        if len(box) == 12 or num == pagenum-1:
            for b in box:
                alink = b.find_all("a", href=True)
                newid = alink[0]["href"].replace("/islandora/object/sdsu%3A","")
                if newid not in all_id:
                    all_id.append(newid)
                else:
                    print(all_id, " dup handleid")
        else:
            print(weburl," manual check")
        num+=1
        print("processing page ", num)
    return all_id

def get_new_id(full_path, date, all_id):
    all_idbf = []
    f = full_path + "/idfiles/id_bf.txt"
    file = open(f, 'r')
    for line in file:
        all_idbf.append(line.strip())
    file.close()
    new_id_fn = full_path + "/idfiles/id_new_" + str(date) + ".txt"
    textfile = open(new_id_fn, "w")
    for element in all_id:
        if element not in all_idbf:
            textfile.write(element + "\n")
    textfile.close()
    f2 = full_path + "/idfiles/id_bf.txt"
    file2 = open(f2, "w")
    for line in all_id:
        file2.write(line + "\n")
    file2.close()
    return new_id_fn

def download_xml_single(new_id_fn , full_path):
    new_id = []
    file = open(new_id_fn , 'r')
    for line in file:
        new_id.append(line.strip())
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

def go(pagenum, full_path, date):
    all_id = harvest_id(pagenum)
    new_id_fn  = get_new_id(full_path, date, all_id)
    download_xml_single(new_id_fn , full_path)
    merge_xml(date, full_path)
    print("edit in Oxygen")
    print("replace '> ' with '>'")
    print("replace' </' with '</'")
    print("""replace '<mods    xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-5.xsd">' with '<mods>'""")

if __name__ == "__main__":
    go(sys.argv[1], sys.argv[2], sys.argv[3])
