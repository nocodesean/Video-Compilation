import upload as upload
import pickle
#auth = str(upload.get_authenticated_service())
#print(auth)

'''auth = open("V0.txt",  # List of Streamers that are Banned
              "rb"  # Open a File in Binary Format to Read
              )  # Open Saved Banned List

token = pickle.load(auth)  # Unpickling BanList

print(token)'''

'''
def uploadVideo(title,keywords, description,category,privacyStatus,file):
    options = {"title": title,
        "keywords": keywords,
        "description": description,
        "category": category,
        "privacyStatus": privacyStatus,
        "file": file
    }
    upload.initialize_upload(token, options)

uploadVideo("Test","Tests,Tests2","wee","20","private","V0.mp4")'''


'''from PIL import Image, ImageOps

# open image
img = Image.open("thumbnails/2 - Doublelift.jpg")

# border color
color = "green"

# top, right, bottom, left
border = (10, 10, 10, 10)

new_img = ImageOps.expand(img, border=border, fill=color)

# save new image
new_img.save("test_image_result.jpg")

# show new bordered image in preview
new_img.show()'''
'''from PIL import Image, ImageOps

import random
random_number = random.randint(0,16777215)
hex_number = str(hex(random_number))
hex_number ='#'+ hex_number[2:]
print('A  Random Hex Color Code is :',hex_number)

import os

#os.mkdir('videos/V0')

from moviepy.editor import *

clip = VideoFileClip('V0.mp4')
clip.save_frame('V0.jpg', t=5.00)

# open image
img = Image.open("V0.jpg")

# border color
color = hex_number

# top, right, bottom, left
border = (10, 10, 10, 10)

new_img = ImageOps.crop(img, border=border)
new_img = ImageOps.expand(new_img, border=border, fill=color)

# save new image
new_img.save("test_image_result.jpg")

# show new bordered image in preview
new_img.show()'''


pL = open("videos/V10/V10.setting",  # List of Streamers that are Approved
                  "rb"  # Open a File in Binary Format to Read
                  )  # Open Saved Approved List

pendingList = pickle.load(pL)  # Unpickling BanList

print(pendingList["title"])

print(pendingList["description"])

print(pendingList["names"])


'''pL = open("video.settings",  # List of Streamers that are Approved
                  "rb"  # Open a File in Binary Format to Read
                  )  # Open Saved Approved List

pendingList = pickle.load(pL)  # Unpickling BanList

print(pendingList)'''
