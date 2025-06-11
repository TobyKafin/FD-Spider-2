
from urllib.parse import urlsplit
import requests
from bs4 import BeautifulSoup
import webbrowser
import os, sys
import pathlib
import time
from datetime import datetime

#defining a function to download the most current sitemap as a .xml.gz file in the sitemap_indices folder
def get_sitemap_index():
    #set paths
    sitemap_ogname = 'sitemap.xml.gz'
    sitemap_dname = 'sitemap_'+datetime.now().strftime('%Y-%m-%d')+'.xml.gz'
    download_path = 'C://Users//Tobias//Downloads//'+sitemap_ogname
    destination_path = 'C://Users//Tobias//Documents//Python//FD-Spider-2//sitemap_indices//'+sitemap_dname

    time.sleep(3) #giving time for download
    #check if sitemap_dname already exists
    print('Checking if '+download_path+' exists...')
    print()
    if os.path.exists(download_path):
        print(download_path+' already exists')
        print('Deleting '+download_path)
        os.remove(download_path)
        print()

    print('Downloading latest copy of the sitemap...')
    webbrowser.open('https://www.freshdirect.com/sitemap/sitemap.xml.gz')
    time.sleep(3)
    print()
    if os.path.exists(destination_path):
        print(destination_path+' already exists.')
        print('Replacing '+destination_path+ ' with the latest sitemap...')
        os.remove(destination_path)
        os.rename(download_path, destination_path)
        print()
    else:
        print('Editing path and name from '+download_path+' to '+destination_path)
        os.rename(download_path, destination_path)
        print()
    
    #sanity check
    if os.path.exists(destination_path):
        print(destination_path+' exists')
    else:
        print('Something went wrong.')
        print(destination_path+' does not exist')

