from twitchAPI.twitch import Twitch
from datetime import timedelta
import datetime
import urllib.request
import pickle
import shutil
from moviepy.editor import *
import upload as test
import math
import os
from os import startfile
from PIL import Image, ImageOps
import random


def convert(seconds):  # Convert Time in Seconds to Time in Minutes and Seconds in 00:00 format

    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%02d:%02d" % (minutes, seconds)


def removeFiles(path):  # Deletes All Files in a Directory

    try:

        files = os.listdir(path)

        for file in files:
            os.remove(path + file)

    except:

        pass


def play_movie(path):  # Open Video

    startfile(path)  # Start Video


def getToken():  # Retrieves Token from File if saved or API Call

    try:

        auth = open("youtubeToken.pickle",  # Pickled Youtube Token
                    "rb"  # Open a File in Binary Format to Read
                    )  # Open Saved Youtube Token

        token = pickle.load(auth)  # Unpickling Youtube Token

    except:

        token = test.get_authenticated_service()  # Call Google API for Youtube Token

        with open("youtubeToken.pickle", "wb") as auth:  # Save Youtube Token

            pickle.dump(token, auth)  # Pickle Youtube Token

    return token


def changeBanList():
    pass


def reviewPending():
    try:

        aL = open("approvedList.txt",  # List of Streamers that are Approved
                  "rb"  # Open a File in Binary Format to Read
                  )  # Open Saved Approved List

        approvedList = pickle.load(aL)  # Unpickling BanList

    except:

        approvedList = []

    try:

        bl = open("banList.txt",  # List of Streamers that are Banned
                  "rb"  # Open a File in Binary Format to Read
                  )  # Open Saved Banned List

        banList = pickle.load(bl)  # Unpickling BanList

    except:

        banList = []

    try:

        pL = open("pendingList.txt",  # List of Streamers that are Pending
                  "rb"  # Open a File in Binary Format to Read
                  )  # Open Saved Pending List

        pendingList = pickle.load(pL)  # Unpickling Pending

    except:

        pendingList = []

    loop = "y"

    while loop == "y":

        print("Current Number of Streamers Pending: " + str(len(pendingList)))

        streamerName = input("Enter Name: ")
        streamerName = str(streamerName)

        if streamerName in pendingList:
            approval = ""
            while approval != "a" or approval != "b":
                approval = input(streamerName + " Approve(a) or Ban(b)")

            if approval == "a":

                approvedList.append(streamerName)

            elif approval == "b":

                banList.append(streamerName)

            else:

                pass

            pendingList.remove(streamerName)

        loop = input("Process Another Streamer (y/n): ")

    try:

        with open("approved.txt",  # List of Streamers that are Approved
                  "wb") as aLTemp:  # Open a File in Binary Format to Write

            pickle.dump(approvedList, aLTemp)  # Pickling

    except:

        pass

    try:

        with open("banList.txt",  # List of Streamers that are Banned
                  "wb") as bLTemp:  # Open a File in Binary Format to Write

            pickle.dump(banList, bLTemp)  # Pickling

    except:

        pass

    try:

        with open("pendingList.txt",  # List of Streamers that are Pending
                  "wb") as pLTemp:  # Open a File in Binary Format to Write

            pickle.dump(pendingList, pLTemp)  # Pickling

    except:

        pass


def checkApproval(streamers):

    approval = True

    try:

        aL = open("approvedList.txt",  # List of Streamers that are Approved
                  "rb"  # Open a File in Binary Format to Read
                  )  # Open Saved Approved List

        approvedList = pickle.load(aL)  # Unpickling BanList

    except:

        approvedList = []

    try:

        pL = open("pendingList.txt",  # List of Streamers that are Approved
                  "rb"  # Open a File in Binary Format to Read
                  )  # Open Saved Approved List

        pendingList = pickle.load(pL)  # Unpickling BanList

    except:

        pendingList = []

    for streamer in streamers:

        try:

            if streamer not in approvedList and streamer not in pendingList:
                input("https://www.twitch.tv/" + streamer)

                pendingList = pendingList.append(streamer)
                approval = False

        except:

            pass

    try:

        with open("pendingList.txt",  # List of Streamers that are Banned
                  "wb") as bLTemp:  # Open a File in Binary Format to Write

            pickle.dump(pendingList, bLTemp)  # Pickling

    except:

        pass

    return approval


def createDescription(file, filePath):  # Take Data from Video File and Create a Description

    description = 'Follow me for more daily videos: \n\nTwitter: https://twitter.com/readysetleague \nInstagram: https://www.instagram.com/readysetleague/ \nFacebook: https://www.facebook.com/gaming/readysetleague\n\nCredits-\n\n'

    file = filePath + file

    try:

        clipTimes = open(file.replace('.mp4', '.txt'),  # Pickled Time of Clips
                         "rb"  # Open a File in Binary Format to Read
                         )  # Open Time of Clips

        cT = pickle.load(clipTimes)  # Unpickling Time of Clips

    except:

        cT = []

    streamers = []
    tN = ""  # Time and Names
    nL = ""  # Names and Link
    names = ""

    for t in cT:

        tN = str(tN) + str(t) + '\n'  # Format String List (00:00 <Name of Streamer>)

        if t.split(' ')[0] != "00:00":  # Exclude First Clip / Intro Clip from Stream Links

            if t.split(' ')[1] not in streamers:

                nL = str(nL) + t.split(' ')[1] + ": https://www.twitch.tv/" + t.split(' ')[
                    1] + "\n"  # Format String List (<Name of Streamer>: <Link to Twitch Stream>)

                streamers.append(t.split(' ')[1])
            else:
                pass

            if names == "":  # If First

                names = t.split(' ')[1]  # Get Only Name of Streamer

            else:

                names = str(names) + "," + t.split(' ')[
                    1]  # Get Only Name of Streamer and Add to Current List of Streamers

    description = description + nL + '\n' + tN  # Combine Two Lists to Rest of Description

    return description, names, streamers


def createThumbnail(file, filePath):
    fileName = file.replace('.mp4', '.jpg')

    clip = VideoFileClip(filePath + file)
    clip.save_frame(filePath + fileName, t=5.00)

    img = Image.open(filePath + fileName)  # open image

    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_number = '#' + hex_number[2:]
    while len(hex_number) < 7:
        hex_number = hex_number + '0'

    color = hex_number  # border color

    border = (30, 30, 30, 30)  # top, right, bottom, left

    new_img = ImageOps.crop(img, border=border)
    new_img = ImageOps.expand(new_img, border=border, fill=color)

    new_img.save(filePath + fileName)  # save new image

    new_img.show()  # show new bordered image in preview


def createVideoTitle(path):

    play_movie(os.path.realpath(path))  # Play the Video with Windows Video Player
    title = str(input("Video Title: "))  # Assign Judgement of the Clip ("" = Approve Clip, "." = Skip Clip, 0 = Skip Clip and Ban Broadcaster of the Clip)
    os.system("TASKKILL /F /IM Video.UI.exe")  # End the Windows Video Player Process to Close the Window

    return title


def uploadVideo(category, privacyStatus, file, token):  # Upload Video

    vS = open("videos/"+file+"/"+file+".setting",  # Pickled Time of Clips
              "rb"  # Open a File in Binary Format to Read
              )  # Open Time of Clips

    videoSettings = pickle.load(vS)  # Unpickling Time of Clips

    options = {"title": videoSettings["title"],
               "keywords": videoSettings["names"],
               "description": videoSettings["description"],
               "category": category,
               "privacyStatus": privacyStatus,
               "thumbnail": videoSettings["path"].replace('.mp4', '.jpg'),
               "file": videoSettings["path"]
               }

    test.initialize_upload(token, options)  # Call Upload.py to Upload to Youtube


def createVideo(clips, videoName, clipTimes, token, socialMedia):  # Take Clips and Compose Video

    if socialMedia is False:

        videoPath = 'videos/' + videoName.replace('.mp4', '/')

        try:

            os.mkdir(videoPath)

        except:

            pass

        video = concatenate_videoclips(clips, method="compose")  # Take Clips and Compose Video


        with open(videoPath + videoName.replace('.mp4', '.txt'), "wb") as videoCT:  # Create Text File Associated with Video

            pickle.dump(clipTimes, videoCT)  # Save Time of Clips to Text File

        video.write_videofile(videoPath + videoName)  # Write Video

        description, names, streamers = createDescription(videoName, videoPath)  # Get Description and Names/Keywords for Video
        createThumbnail(videoName, videoPath)
        names = names + "League,League of Legends,LOL,Twitch"  # Add Extra Keywords
        title = createVideoTitle(videoPath + videoName)

        videoInformation = {"title": title, "names": names, "description": description, "path": videoPath + videoName}

        with open(videoPath + videoName.replace('.mp4', '.setting'),
                  "wb") as videoSettings:  # Create Text File Associated with Video

            pickle.dump(videoInformation, videoSettings)  # Save Time of Clips to Text File

        #uploadVideo("20", "private", videoName, token)  # Upload Video to Youtube

    else:

        videoPath = 'videosSM/'

        video = concatenate_videoclips(clips, method="compose")  # Take Clips and Compose Video

        video.write_videofile(videoPath + videoName)  # Write Video

    '''    approval = checkApproval(streamers)

    if approval is True:

        

    else:

        try:

            pVL = open("pendingVideoList.txt",  # List of Streamers that are Approved
                       "rb"  # Open a File in Binary Format to Read
                       )  # Open Saved Approved List

            pendingVideoList = pickle.load(pVL)  # Unpickling BanList

        except:

            pendingVideoList = []

        pendingVideoList.append(videoPath + videoName)

        with open("pendingVideoList.txt",
                  "wb") as pLV:  # Create Text File Associated with Video

            pickle.dump(pendingVideoList, pLV)  # Save Time of Clips to Text File'''


def assignClips(reviewedClips=None):

    token = getToken()  # Retrieve Token for Youtube

    clips = [VideoFileClip('media/ready.mp4')]  # Create List of Clips and Add Intro Video to the Beginning
    clipTimes = ['00:00 Intro']  # Create List of Clip Times and Add Intro Video Time to the Beginning
    currentClipTime = 3  # Create Current Clip Time and Adjust for Intro Video
    currentVideoDuration = 3  # Create Current Video Duration and Adjust for Intro Video
    pce = 0  # Create Past Clip End for Intro Video

    try:

        vN = open("video.settings",  # Pickled Time of Clips
                         "rb"  # Open a File in Binary Format to Read
                         )  # Open Time of Clips

        videoName = pickle.load(vN)  # Unpickling Time of Clips

    except:

        videoName = 0  # Create Current Video Name

    if reviewedClips is None:
        reviewedClips = os.listdir('reviewedClips/')

    for filename in reviewedClips:  # Retrieve Each File Name for Every File in 'reviewedClips/' Folder

        if filename.endswith(".mp4"):  # If the File is '.mp4'

            clip = VideoFileClip('reviewedClips/' + filename)  # Assign File to clip

            if clip.w == 1920 and clip.h == 1080:  # If clip has a Width of 1920 PX and a Height of 1080 PX

                try:

                    clip.set_start(pce - 1).crossfadein(1)  # Create a Crossfade for One Second on clip

                except:

                    pass

                clips.append(clip)  # Add clip to List of Clips

                currentClipTime = currentClipTime + pce  # Adjust CurrentClipTime
                clipTimes.append(str(convert(math.floor(currentClipTime))) + ' ' + filename.split(' - ')[1].replace('.mp4', ''))  # Add Start of clip to Clip Times

                pce = clip.end  # Assign the Time at the End of the Current Clip to pce

                currentVideoDuration = currentVideoDuration + pce  # Adjust Current Video Duration

        if currentVideoDuration >= 572:  # If the Current Clips are at least Ten Minutes

            clips.append(VideoFileClip('media/EndCard.mp4'))

            createVideo(clips, "V" + str(videoName) + ".mp4", clipTimes, token, False)  # Call Create Video

            clips = [VideoFileClip('media/ready.mp4')]  # Reset Clips
            clipTimes = [0]  # Reset Clip Times
            currentClipTime = 3  # Reset Current Clip Time
            currentVideoDuration = 3  # Reset Current Video Duration
            videoName = int(videoName) + 1  # Increase Video Name Iterator
            pce = 0  # Reset Previous Clip End

            try:

                with open("video.settings",
                          "wb") as videoNameTemp:

                    pickle.dump(videoName, videoNameTemp)  # Pickling

            except:

                videoName = 0  # Create Current Video Name

        else:

            pass

    if currentVideoDuration >= 154 and currentVideoDuration < 572:
        createVideo(clips, "V" + str(videoName) + ".mp4", clipTimes, token, True)  # Call Create Video


def getLists():  # Load Lists

    banList = []  # Create List of Banned Streamers
    approvedList = []  # Create List of Approved Streamers
    pendingList = []  # Create List of Pending Streamers

    try:

        bl = open("banList.txt",  # List of Streamers that are Banned
                  "rb"  # Open a File in Binary Format to Read
                  )  # Open Saved Banned List

        banList = pickle.load(bl)  # Unpickling BanList

    except:

        pass

    return banList, approvedList, pendingList


def twitchLogin():
    twitch = Twitch('4mvus9unwmq1zk0jasp3jjv4wifi0e',  # Client ID from Twitch API
                    '8jyh9qfi1g80rgsugotxw512cyuedm'  # Secret ID from Twitch API
                    )  # Create Instance of Twitch API

    twitch.authenticate_app([])  # Twitch API Authentication Call

    return twitch


def reviewClips(LOC, banList):  # Review Clips in 'clips/' Folder

    reviewedClips = []  # Create Reviewed Clips List

    input("Start Video Review: ")

    for x in range(0, len(LOC)):  # x is the Iterator for the List of Clips

        if LOC[x]["broadcaster_name"] not in banList:  # If the Name of the Broadcaster of the Clip is not in the Ban List

            video_name = str(x) + " - " + LOC[x]["broadcaster_name"]  # Create a Video Name Made from x and the Name of the Broadcaster of the Clip
            review = ""  # Create Review Input Variable Default

            try:

                play_movie(os.path.realpath('clips/' + video_name + '.mp4'))  # Play the Video with Windows Video Player
                review = str(input())  # Assign Judgement of the Clip ("" = Approve Clip, "." = Skip Clip, 0 = Skip Clip and Ban Broadcaster of the Clip)
                os.system("TASKKILL /F /IM Video.UI.exe")  # End the Windows Video Player Process to Close the Window

            except:

                review = "."  # Assign Clip to be Skipped

            if review == "":

                reviewedClips.append(video_name + '.mp4')  # Approve Clip

                try:

                    shutil.move(os.path.realpath('clips/' + video_name + '.mp4'),  # Move Clip from 'clips' Folder
                                os.path.realpath('reviewedClips/' + video_name + '.mp4'))  # Move Clip to 'reviewedClips' Folder

                except:

                    pass

            elif review == "0":  # Ban Streamer

                try:

                    banList.append(LOC[x]["broadcaster_name"])  # Add Name of Broadcaster to Ban List

                    with open("banList.txt",  # List of Streamers that are Banned
                              "wb") as bLTemp:  # Open a File in Binary Format to Write

                        pickle.dump(banList, bLTemp)  # Pickling

                except:

                    pass

    input("End of Review")

    assignClips()


def getClips():  # Retrieve Clips from Twitch According to Settings

    twitch = twitchLogin()  # Call Twitch Login
    banList, approvedList, pendingList = getLists()
    removeFiles("clips/")
    removeFiles("reviewedClips/")
    input("Start Getting Clips")

    LOC = []  # List of Clips

    clips = twitch.get_clips(game_id='21779',  # Game ID for League of Legends
                             first=100,  # Get the First 100 Clips
                             started_at=datetime.datetime.now() - timedelta(hours=24)  # In the last 24 Hours
                             )
    print(datetime.datetime.now() - timedelta(hours=24))

    for x in clips["data"]:  # x is the Current Clip

        if x["language"] == "en" and x["broadcaster_name"] not in banList:  # If the Language is English and the Broadcaster Name of the Clip is not on the Ban List

            if len(LOC) < 1:  # If List of Clips is Empty

                LOC.append(x)  # Add the Current Clip

            else:

                if x["view_count"] > LOC[0]["view_count"]:  # If the Clips View Count is Greater than the Highest View Count of Clips in the List of Clips

                    LOC.insert(0, x)  # Add the Current Clip to the Top of the List of Clips
                else:

                    LOC.append(x)  # Add the Current Clip to the Bottom of the List of Clips

    while 1 == 1:

        #print(clips['pagination'])

        try:

            clips = twitch.get_clips(game_id='21779',  # Game ID for League of Legends
                                     first=100,  # Get the First 100 Clips
                                     started_at=datetime.datetime.now() - timedelta(hours=24),  # In the last 24 Hours
                                     after=clips["pagination"]["cursor"]  # From the Next Page of Clips
                                     )

        except:

            break

        for x in clips["data"]:  # x is the Current Clip

            if x["language"] == "en" and x["broadcaster_name"] not in banList:  # If the Language is English and the Name of the Broadcaster of the Clip is not on the Ban List

                #clip = VideoFileClip('reviewedClips/' + filename)  # Assign File to clip


                #if clip.w == 1920 and clip.h == 1080:

                if len(LOC) < 1:  # If List of Clips is Empty

                    LOC.append(x)  # Add the Current Clip

                else:

                    if x["view_count"] > LOC[0]["view_count"]:  # If the Clips View Count is Greater than the Highest View Count of Clips in the List of Clips

                        LOC.insert(0, x)  # Add the Current Clip to the Top of the List of Clips

                    else:

                        LOC.append(x)  # Add the Current Clip to the Bottom of the List of Clips

    for x in range(0, len(LOC)):  # x is the Iterator for the List of Clips

        try:

            video_name = str(x) + " - " + LOC[x][
                "broadcaster_name"]  # Create a Video Name Made from x and the Name of the Broadcaster of the Clip

            print(video_name + " - " + LOC[x]["created_at"] + " - " + LOC[x]["url"])

            video_url = LOC[x]["thumbnail_url"].split(
                "https://clips-media-assets2.twitch.tv/")  # Isolate the Url ID of the Clip
            video_url = video_url[1].split("-preview")  # Isolate the Url ID of the Clip
            video_url = video_url[0]  # Assign the URL ID of the Clip

            urllib.request.urlretrieve("https://production.assets.clips.twitchcdn.net/" + video_url + ".mp4",
                                       # Download the Current Clip
                                       "clips/" + video_name + '.mp4'  # Save the Current Clip into the 'clips' folder
                                       )

            clip = VideoFileClip('clips/' + video_name + '.mp4')  # Assign File to clip

            if clip.w != 1920 or clip.h != 1080:

                os.remove('clips/' + video_name + '.mp4')

            else:
                pass


        except:

            pass

    input("End of Getting Clips")
    reviewClips(LOC, banList)


getClips()
#assignClips()
#uploadVideo("20", "private", 'V4', getToken())  # Upload Video to Youtube
# print(createThumbnail("V0.mp4","videos/V0/"))
#reviewPending()
