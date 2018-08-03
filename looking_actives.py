# Date: 07/24/2018
# @author : dewan <dewshrs@gmail.com>
#
# This program is tested on python 2.7
#
# This program downloads  all the active ligands for the particular target protein in sdf format.
# It takes the protein id (uniprot id) as an input.
#
#The command will look like: python extract_ligands.py -i P46663
#
#This may require installation of packages BeautifulSoup, urlib2 and requests if not installed
#

import requests
from bs4 import BeautifulSoup
import urllib2
import argparse

# function to extract the ligands for particular ligand
def extract_ligands(id):
    l_count =0
    output = open(id+'.sdf', 'w')
    # link of the protein
    link = 'https://pharos.nih.gov/idg/targets/'+ id

    # extracting all the content in the link above
    r= requests.get(link)
    c = r.content
    content = BeautifulSoup(c,'html.parser')

    # getting only the elements with h3 tag and class = panel-title
    all = content.find_all("h3",{"class":"panel-title"})

    # extracting unique id required to get the ligands associated with the protein
    for n in range(0,len(all)):
        try:
            a = all[n].find("a",{"class":"pull-right"})
            #print(a)
            if a >0:
                _id = str(a).split('targets/')[1].split('/')[0]
                break
        except:
            continue

    drugs = "https://pharos.nih.gov/idg/targets/"+ _id + "/ligands?group=drugs"
    chembl = "https://pharos.nih.gov/idg/targets/"+_id+"/ligands?group=chembl"

    try:
        print('looking for active ligands on section drugs')
        response = urllib2.urlopen(drugs)
        data = response.read()
        output.write(data)
        l_count = int(data.count('$$$$'))
    except:
        print('no ligands on section drugs')

    try:
        print('looking for active ligands on section chembl')
        response = urllib2.urlopen(chembl)
        data = response.read()
        output.write(data)
        l_count = l_count + int(data.count('$$$$'))
    except:
        print('no ligands on section chembl')

    output.close()
    print('Ligand search completed for ' + str(id) + ', '+ str(l_count)+ ' number of ligands found.\n')

if  __name__== "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i",required=True,help='uniprot id of the protein')
    args = vars(ap.parse_args())

    id = args["i"]
    print('\n-------------------------- Searching on Pharos website ------------------------------\n')
    extract_ligands(id)


