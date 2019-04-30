import requests
import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()


url = "https://b.thumbs.redditmedia.com/P8WJSc0UT53zWMRshZbi7dbyn4dX7xlh4CbR8g-ziQM.jpg"
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


catsvdogs = []
if 'Cat' in labels:
    
    if 'Dog' in labels:
        catsvdogs.append('Cat and Dog')
    else:
        catsvdogs.append("Cat")
elif 'Dog' in labels:
    catsvdogs.append('Dog')

return catsvdogs