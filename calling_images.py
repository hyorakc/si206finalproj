import requests
import io
import os
import sqlite3

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

conn = sqlite3.connect('reddit_r_awww.sqlite')
cur = conn.cursor()
cur.execute('SELECT thumburl FROM Reddit')
post_list = cur.fetchall()

for _ in post_list:

    url = _
    response = requests.get(url)
    if response.status_code == 200:
        # with open("/Users/apple/Desktop/sample.jpg", 'wb') as f:
        #     f.write(response.content)
        content = response.content


    # Loads the image into memory
    # with io.open(file_name, 'rb') as image_file:
    #     content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # print('Labels:')
    # for label in labels:
    #     print(label.description)

    labels2 = [x.description for x in labels]


    catsvdogs = []
    if 'Cat' in labels2:
    
        if 'Dog' in labels2:
            catsvdogs.append('Cat and Dog')
        else:
            catsvdogs.append("Cat")
    elif 'Dog' in labels2:
        catsvdogs.append('Dog')

    return catsvdogs
    # print(catsvdogs)