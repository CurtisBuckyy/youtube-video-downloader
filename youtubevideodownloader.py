#YouTube Video Downloader program created by Curtis Buckingham (https://github.com/CurtisBuckyy)

#-----Software Information-----#

#This software requires use of tkinter, customTkinter, pytube, os, sys, pathlib, pillow and re modules which need to be installed seperately.
#The software allows the highest quality download of .mp3 and .mp4 files of the requested YouTube video via an inputted link.
#Downloaded files will automatically save in a generated folder called 'YouTube Downloads' within the windows downloads directory.
#The generated folder will be created through either two events, clicking on the 'open downloads folder' button or downloading a valid youtube video file.

import customtkinter
from tkinter import *
from pytube import YouTube
import os, sys
import os.path
import pathlib
from pathlib import Path
from PIL import Image, ImageTk
import re

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

path = resource_path("youtubevideodownloaderlogo1.png")
path2 = resource_path("youtubevideodownloaderlogo.ico")
path3 = resource_path("download_icon.png")
path4 = resource_path("folder_icon.png")

root = customtkinter.CTk()  # create CTk window like you do with the Tk window
root.title("YouTube Video Downloader") 
root.configure(background="white")
root.geometry("750x850+585+115") #Sizing of application window and positioning to center of screen, assuming resolution is 1920x1080
root.resizable(False, False) #Making program un-resizable
root.iconbitmap(path2) #Assigning icon to application window

#Variables set to Global so they can be used anywhere within the program code
global downloadDirectory 
global windowsUserName
global youtubeTitleMessage

windowsUserName = os.getlogin() #Grabbing Windows user name
downloadDirectory = "/Users/{name}/downloads".format(name = windowsUserName) #Adding windows user name to downloads directory
createdDirectory = downloadDirectory + "/YouTube Downloads"
mp3Directory = createdDirectory + "/Mp3 Downloads"
mp4Directory = createdDirectory + "/Mp4 Downloads"

def checkFolderExists():
     
     if os.path.isdir(createdDirectory) == False: #Checking if directory doesn't exist, if not then it creates directory

         #Creating the relevant directories for files to saved in.
          os.mkdir(createdDirectory) 
          os.mkdir(mp3Directory)
          os.mkdir(mp4Directory)

def downloadMp4():

     errorMessage.config(text="") #Resetting error message to default state.

     youtubeUrl = videoUrlInput.get()

     youtubeUrlLength = len(youtubeUrl)

     videoUrlInput.delete(0, youtubeUrlLength)

     try:
        yt = YouTube(youtubeUrl) #Creating youtube object
        yd = yt.streams.get_highest_resolution()#Grabbing highest resolution

        youtubeTitleMessage = "Download complete: " + yt.title + ".mp4"

        ytTitle = re.sub(r'[\\/*?:"<>|]+-%#|',"",yt.title) #Removing illegal characters for file names.

        ytTitle = ytTitle.replace("'", '') #Removing single quotes from string.

        checkPath = "C:/Users/cbuck/Downloads/YouTube Downloads/Mp4 Downloads/{title}.mp4".format(title = ytTitle)

        if os.path.isfile(checkPath):
            errorMessage.config(text="Failed to download: File already exists") #Configuring error message to provide error message
            downloadMessage.config(text="")

        else:
            yd.download(mp4Directory) #Downloading video to the directory stored in downloadDirectory
            downloadMessage.config(text=youtubeTitleMessage) #Outputting that the download was a success
     except:
        print("Exception error caught")
        errorMessage.config(text="Please input a valid YouTube URL") #Configuring error message to provide error message

def downloadMp3():

     errorMessage.config(text="") #Resetting error message to default state.
     
     youtubeUrl = videoUrlInput.get()

     youtubeUrlLength = len(youtubeUrl)

     videoUrlInput.delete(0, youtubeUrlLength)

     try:
        yt = YouTube(youtubeUrl) #Creating youtube object
        yd = yt.streams.filter(only_audio=True).first() #Extracting audio from YouTube file
        
        youtubeTitleMessage = "Download complete: " + yt.title + ".mp3"

        ytTitle = re.sub(r'[\\/*?:"<>|]+-%#|',"",yt.title) #Removing illegal characters for file names.

        ytTitle = ytTitle.replace("'", '') #Removing single quotes from string.

        checkPath = "C:/Users/cbuck/Downloads/YouTube Downloads/Mp3 Downloads/{title}.mp3".format(title = ytTitle)

        if os.path.isfile(checkPath):
            errorMessage.config(text="Failed to download: File already exists") #Configuring error message to provide error message
            downloadMessage.config(text="")
        else:
            downloadFile = yd.download(mp3Directory) #Downloading video to the directory stored in downloadDirectory
            base, ext = os.path.splitext(downloadFile)
            converted_file = base + '.mp3'
            os.rename(downloadFile, converted_file) #Converting file extension from .mp4 to .mp3
            downloadMessage.config(text=youtubeTitleMessage) #Outputting that the download was a success
        
     except:
        print("Exception error caught")
        errorMessage.config(text="Please input a valid YouTube URL") #Configuring error message to provide error message

def openDownloadsFolder():

    checkFolderExists() #Excecutes checkFolderExists function
    os_drive = pathlib.Path.home().drive

    #Launches downloads folder within file explorer based on users drive location i.e (C: Drive)
    os.startfile("{drive}/users/{name}/downloads/Youtube Downloads".format(name = windowsUserName, drive = os_drive))


download_image = ImageTk.PhotoImage(Image.open(path3).resize((35,35), Image.ANTIALIAS))
download_folder_image = ImageTk.PhotoImage(Image.open(path4).resize((50,50), Image.ANTIALIAS))

programLogo = PhotoImage(file = "youtubevideodownloaderlogo.png")
programLogoLabel = Label(root, image=programLogo, borderwidth=0)
programLogoLabel.pack(pady=25)

informationLbl = customtkinter.CTkLabel(master=root, text="Insert YouTube URL here:", text_font=("Arial", -14), text_color="black")
informationLbl.pack(pady=10)

videoUrlInput = customtkinter.CTkEntry(master=root, width=400, placeholder_text_color="black", bg_color="white", fg_color="white", text_color="black")
videoUrlInput.pack(pady=25)

downloadmp4Button = customtkinter.CTkButton(master=root, image = download_image, text="Download .mp4", width=250, height=60, command=downloadMp4, text_font=("Arial", -16), compound = RIGHT)
downloadmp4Button.pack(pady=20)

downloadmp3Button = customtkinter.CTkButton(master=root, image = download_image, text="Download .mp3", width=250, height=60, command=downloadMp3, text_font=("Arial", -16), compound = RIGHT)
downloadmp3Button.pack(pady=20)

openDownloadsButton = customtkinter.CTkButton(master=root, image = download_folder_image , text="Open Downloads Folder", width=250, height=60, fg_color = "red", hover_color="#8a0808", command=openDownloadsFolder, text_font=("Arial", -16), compound = RIGHT)
openDownloadsButton.pack(pady=20)

downloadMessage = Label(text = "", font = ("Arial", 10), bg="white", fg="black")
downloadMessage.pack(pady=20)

errorMessage = Label(text = "", font = ("Arial", 10), bg="white", fg="red")
errorMessage.pack()

root.mainloop()
