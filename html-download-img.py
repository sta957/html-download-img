#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import urllib
import urllib.request
import requests
import sys
import os


url_to_scrape = 'http://' + sys.argv[1] # combine 'http://' with the given argument of cli
dir_path = sys.argv[1]                  # the directory is named by it's site
page = requests.get(url_to_scrape)      # set a get-request to the webpage
page_content = page.content             # get the html-content of the get-request
soup = BeautifulSoup(page_content)      # store the html-content into the soup variable
img_num = 0
x = 0


# create a local directory to store th images from website
try:
    os.mkdir(str(dir_path))
except:
    print("Directory " + str(dir_path) + " can't be created!")
else:
    print("Directory " + str(dir_path) + " successfully created!")

for i in soup.find_all('img'):
    imagelist = i.get('src')
    img_num = img_num+1
    
    # check if it's the full url-path or just a subpath
    if imagelist[:1]=="/" or imagelist[:1]==".":
        image = url_to_scrape + '/' + imagelist
    else:
        image = imagelist
        
    # get the title of the requested image
    img_header = i.get('alt')
    
    # check if title of image is empty or contains sourcecode
    if img_header != '' and '<' not in img_header and img_header is not None:
        filename = img_header
    else:
        filename = str(x)
        x = x+1
        
    # get the image format to store it right : (jpg, png, gif) are supported by default            
    if image[-4:] == '.png':
        file_image = open(str(dir_path) + '/' + str(filename) + '.png', 'wb')
    elif image[-4:] == '.gif':
        file_image = open(str(dir_path) + '/' + str(filename) + '.gif', 'wb')
    else:
        file_image = open(str(dir_path) + '/' + str(filename) + '.jpeg', 'wb')
    
    # store the imagefiles in the local directory and close the file-connection
    file_image.write(urllib.request.urlopen(image).read())
    file_image.close()

    
print("Code was completed! Downloaded " + str(img_num) + " images into " + str(dir_path))

