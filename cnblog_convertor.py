from bs4 import BeautifulSoup
from collections import namedtuple
from datetime import datetime, timedelta
import requests
import re
import pathlib

DATE_FORMAT = "%a, %d %b %Y %X %Z"
BASE_DIR = "blog/"
BASE_IMAGE_DIR = "images/"

BlogInfo = namedtuple('BlogInfo',["title","text","date","name"])

def handleFileName(link : str):
    return link.split("/")[-1].replace(".html","").replace("_","-")

def handleImage(text:str):
    # extend this if pattern is more complicated
    r = re.findall("\!\[.*?\]\((.+?)\)", text)
    newText = text
    for image in r:
        # default to images file and change original image url to this
        newFilePath = BASE_IMAGE_DIR + image.split("/")[-1]
        resp = requests.get(image)
        print(f"{image}:{resp.status_code}")
        if resp.status_code == 200:
            with open(f"{newFilePath}", 'wb') as f:
                f.write(resp.content)
                # just replace
                newText = newText.replace(image, "/" + newFilePath)
    return newText

def handleItem(item):
    return BlogInfo(
        title=item.title.text,
        text=handleImage(item.description.text),
        # UTC+8 the easy way to do time convert...
        date=datetime.strptime(item.pubdate.text, DATE_FORMAT) + timedelta(hours=8),
        name=handleFileName(item.guid.text))

def writeToFile(blogInfos) :
    for blog in blogInfos:
        with open(BASE_DIR + blog.name + ".md", "w", encoding="utf-8") as fout:
            fout.write(
f"""---
title: "{blog.title}"
date: {datetime.strftime(blog.date, "%Y/%m/%d %H:%M:%S")}
---
{blog.text}
""")


pathlib.Path(BASE_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(BASE_IMAGE_DIR).mkdir(parents=True, exist_ok=True)
blogInfos = None
with open("CNBlogs_BlogBackup_1_201709_201905.xml", encoding="utf-8") as file:
    xml = BeautifulSoup(file, "html.parser")
    blogInfos = [handleItem(item) for item in xml.find_all("item")]

writeToFile(blogInfos)
