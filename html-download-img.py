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
import multiprocessing



url_to_scrape = 'http://' + sys.argv[2]                 # combine 'http://' with the given argument of cli
dir_path = sys.argv[1]                                  # the directory is named by it's site
headers = {                                             # set the useragent to appear as real user
    'User-Agent':'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
page = requests.get(url_to_scrape, headers = headers)   # set a get-request to the webpage
page_content = page.content                             # get the html-content of the get-request
soup = BeautifulSoup(page_content, 'lxml')              # store the html-content into the soup variable
img_num = 0
x = 0
y = 0
img_elements = soup.find_all('img')                     # find all images in soup variable

# define func that verifies input for y/N
def folder_wr():
    write_req = input('Do you want to write into existing folder ' + str(dir_path) + ' (y/N)? [y]: ')
    if write_req == '':
        write_req = 'y'
    elif write_req != 'y' and write_req != 'N':
        print('Please enter a valid argument...')
        folder_wr()
    return write_req

# if not exits create a local folder to store the images from html-site
# else ask to put images into the existing folder
def folder_check():
    if os.path.isdir(dir_path) == False:
        try:
            os.mkdir(str(dir_path))
        except:
            print("Directory " + str(dir_path) + " can't be created!")
        else:
            print("Directory " + str(dir_path) + " successfully created!")
    else:
        if folder_wr() == 'N':
            exit()

# for all images on html-site
def get_img(img_elements_f):
    img_num = 0
    for i in img_elements_f:
        if i.get('data-src') is not None:
            raw_url = i.get('data-src')
        else:
            raw_url = i.get('src')

        # skip img with data: tag
        if raw_url[:5] == "data:":
            continue

        # check if it's the full url-path or just a subpath
        if raw_url[:4] == "http":
            image_url = raw_url
        elif raw_url[:3] == "www":
            image_url = raw_url
        elif raw_url[:2] == "//":
            image_url = 'http:' + raw_url
        elif raw_url[:1] == "/":
            image_url = url_to_scrape + raw_url
        else:
            image_url = url_to_scrape + '/' + raw_url

        # set the url as image-name
        filename_complete_url = image_url.split('/')
        filename_url = str(filename_complete_url[-1]).split('.')
        filename = str(filename_url[0])
        img_type = str(filename_url[1]).split('?')

        # increase image counter and get the image
        img_num = img_num+1
        req_img_url = requests.get(image_url)

        # store the image files
        with open(str(dir_path) + '/' + str(filename) + '.' + str(img_type[0]), 'wb') as f:
            f.write(req_img_url.content)

        print(image_url)

def testf(num):
    return num+10

# worker thread function
def worker(num, num_work, c_elem):
    # check for usecase of thread
    e_inspect = 0
    to_inspect = []

    if c_elem >= num_work:
        e_inspect = round(c_elem / num_work)                   # number of elements to inspect by simple worker
        e_range_start = num * e_inspect                 # first element to be scanned
        e_range_end = (e_range_start + e_inspect) - 1   # last element to be scanned
    elif c_elem >= num + 1:
        e_inspect = 1
        e_range_start = num
        e_range_end = num
    else:
        exit()

    # check for the last thread to scan the lasting images
    if num + 1 == num_work:
        e_range_start = c_elem - e_inspect
        e_range_end = c_elem - 1

    for x in range(e_range_start, e_range_end + 1):
        to_inspect.append(img_elements[x])

    get_img(to_inspect) ## fix ths bugs

    # print ('Worker:' + str(num) + ' --> '+ str(to_inspect)) # for debugging purposes

# multiprocessing the download
def multiproc():
    if __name__ == '__main__':
        jobs = []
        range_start = 0
        count_elements = len(img_elements)
        num_workers = 15
        for i in range(num_workers):
            p = multiprocessing.Process(target=worker, args=(i, num_workers, count_elements))
            jobs.append(p)
            p.start()

multiproc()
