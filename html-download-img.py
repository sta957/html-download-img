#!/usr/bin/env python
# coding: utf-8

# ## html-download-img (download images from html-site)
# simple and small programm to download images from a single html-site


from bs4 import BeautifulSoup
import urllib
import urllib.request
import requests
import sys
import os



url_to_scrape = 'http://' + sys.argv[2] # combine 'http://' with the given argument of cli
dir_path = sys.argv[1]                  # the directory is named by it's site
headers = {                             # set the useragent to appear as real user
    'User-Agent':'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
page = requests.get(url_to_scrape, headers = headers) #, headers = headers)      # set a get-request to the webpage
page_content = page.content             # get the html-content of the get-request
soup = BeautifulSoup(page_content, 'lxml')      # store the html-content into the soup variable
img_num = 0
x = 0
y = 0
img_elements = soup.find_all('img')

# create a local folder to store the images from html-site
# folders with the same name have to be deleted first to avoid an error
try:
    os.mkdir(str(dir_path))
except:
    print("Directory " + str(dir_path) + " can't be created!")
else:
    print("Directory " + str(dir_path) + " successfully created!")


# for all images on html-site
for i in img_elements:
    raw_url = i.get('src')

    # skip img with data: tag
    if raw_url[:5] == "data:":
        continue

    # check if it's the full url-path or just a subpath
    if raw_url[:4] == "http":
        image_url = raw_url
    elif raw_url[:3] == "www":
        image_url = raw_url
    elif raw_url[:1] == "/":
        image_url = url_to_scrape + raw_url
    else:
        image_url = url_to_scrape + '/' + raw_url

    # get the title of the requested image
    img_header = i.get('alt')

    # check if title of image is a NoneType -> set header
    if img_header is None:
        print('NoneType detected: ' + str(image_url))
        img_header = 'NT_' + str(y)
        y = y+1

    if img_header != '' and '<' not in img_header and '>' not in img_header:
        filename = img_header
    else:
        filename = str(x)
        x = x+1

    # increase image counter and get the image
    img_num = img_num+1
    req_img_url = requests.get(image_url)

    # store the image files in the right format
    if image_url[-4:] == '.png':
        with open(str(dir_path) + '/' + str(filename) + '.png', 'wb') as f:
            f.write(req_img_url.content)
    elif image_url[-4:] == '.gif':
        with open(str(dir_path) + '/' + str(filename) + '.gif', 'wb') as f:
            f.write(req_img_url.content)
    elif image_url[-4:] == '.svg':
            with open(str(dir_path) + '/' + str(filename) + '.svg', 'wb') as f:
                f.write(req_img_url.content)
    else:
        with open(str(dir_path) + '/' + str(filename) + '.jpeg', 'wb') as f:
            f.write(req_img_url.content)

    print(image_url) # output for debugging purposes



print("Code was completed! Downloaded " + str(img_num) + " images into folder: " + str(dir_path))
