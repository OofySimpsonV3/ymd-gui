# YMD BETA 0.6
# Github: OofySimpsonV3

import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import filedialog
import os
from yt_dlp import YoutubeDL
import ffmpeg
from threading import Thread
from time import sleep

class App:
    def __init__(self, root):
        # setting title
        root.title("YMD-G Alpha 0.5 (UNIX Edition)")
        # setting window size
        width = 462
        height = 155
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        global btnDownload
        btnDownload = tk.Button(root)
        btnDownload["bg"] = "#e9e9ed"
        ft = tkFont.Font(family="Times", size=10)
        btnDownload["font"] = ft
        btnDownload["fg"] = "#000000"
        btnDownload["justify"] = "center"
        btnDownload["text"] = "Download"
        btnDownload.place(x=10, y=50, width=441, height=37)
        btnDownload["command"] = self.btnDownload_command

        global boxPlaylist
        boxPlaylist = tk.Checkbutton(root)
        ft = tkFont.Font(family="Times", size=10)
        boxPlaylist["font"] = ft
        boxPlaylist["fg"] = "#333333"
        boxPlaylist["justify"] = "center"
        boxPlaylist["anchor"] = "w"
        boxPlaylist["text"] = "Playlist"
        boxPlaylist.place(x=5, y=90, width=118, height=20)
        boxPlaylist["offvalue"] = "0"
        boxPlaylist["onvalue"] = "1"
        boxPlaylist["command"] = self.boxPlaylist_command
        boxPlaylist["variable"] = varBox

        global boxSearch
        boxSearch = tk.Checkbutton(root)
        ft = tkFont.Font(family="Times", size=10)
        boxSearch["font"] = ft
        boxSearch["fg"] = "#333333"
        boxSearch["justify"] = "left"
        boxSearch["anchor"] = "w"
        boxSearch["text"] = "Search"
        boxSearch.place(x=5, y=110, width=80, height=20)
        boxSearch["offvalue"] = "0"
        boxSearch["onvalue"] = "1"
        boxSearch["command"] = self.boxSearch_command
        boxSearch["variable"] = varSearch

        global boxThumbnail
        boxThumbnail = tk.Checkbutton(root)
        ft = tkFont.Font(family="Times", size=10)
        boxThumbnail["font"] = ft
        boxThumbnail["fg"] = "#333333"
        boxThumbnail["justify"] = "left"
        boxThumbnail["anchor"] = "w"
        boxThumbnail["text"] = "Add thumbnail to metadata"
        boxThumbnail.place(x=5, y=130, width=200, height=20)
        boxThumbnail["offvalue"] = "0"
        boxThumbnail["onvalue"] = "1"
        boxThumbnail["command"] = self.boxThumbnail_command
        boxThumbnail["variable"] = varThumbnail

        global txtUrls
        txtUrls = tk.Entry(root)
        txtUrls["borderwidth"] = "1px"
        ft = tkFont.Font(family="Times", size=10)
        txtUrls["font"] = ft
        txtUrls["fg"] = "#333333"
        txtUrls["justify"] = "left"
        txtUrls["text"] = "URLs (Seperate multiple URLs with spaces!)"
        txtUrls.place(x=10, y=10, width=441, height=33)

        global radioVideo
        radioVideo = tk.Radiobutton(root)
        ft = tkFont.Font(family="Times", size=10)
        radioVideo["font"] = ft
        radioVideo["fg"] = "#333333"
        radioVideo["justify"] = "center"
        radioVideo["text"] = "Video"
        radioVideo.place(x=370, y=95, width=86, height=30)
        radioVideo["value"] = 1
        radioVideo["command"] = self.radioVideo_command
        radioVideo["variable"] = varRadio
        
        global radioAudio
        radioAudio = tk.Radiobutton(root)
        ft = tkFont.Font(family="Times", size=10)
        radioAudio["font"] = ft
        radioAudio["fg"] = "#333333"
        radioAudio["justify"] = "center"
        radioAudio["text"] = "Audio (mp3 + metadata)"
        radioAudio.place(x=190, y=95, width=177, height=31)
        radioAudio["value"] = 0
        radioAudio["command"] = self.radioAudio_command
        radioAudio["variable"] = varRadio

    # DOWNLOAD AUDIO STANDARD FUNCTION
    def downloadAudio(self):
        outputDir = filedialog.askdirectory(
            parent=root, initialdir=os.getcwd(), title="Please select a folder:"
        )
        print(outputDir)
        # IF SEARCH OPTION IS SELECTED
        if varSearch.get() == 1:
            urls = "ytsearch: " + txtUrls.get()
        else:
            urls = txtUrls.get().split(" ")

        # IF THUMBNAIL OPTION IS SELECTED
        if varThumbnail.get() == 1:
            opts = {
                "outtmpl": outputDir + "/%(title)s-%(id)s.%(ext)s",
                "embed-thumbnail": True,
                "format": "bestaudio/best",
                "writethumbnail": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    },
                    {"key": "FFmpegMetadata"},
                    {
                        "key": "EmbedThumbnail",
                        "already_have_thumbnail": False,
                    },
                ],
                "addmetadata": True,
                "add-metadata": True,
            }
        else:
            opts = {
                "outtmpl": outputDir + "/%(title)s-%(id)s.%(ext)s",
                "embed-thumbnail": True,
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    },
                    {"key": "FFmpegMetadata"},
                ],
                "addmetadata": True,
                "add-metadata": True,
            }

        try:
            with YoutubeDL(opts) as ydl:
                ydl.download(urls)
                messagebox.showinfo("Success!", "Successfully downloaded media!")
        except:
            messagebox.showerror(
                "ERROR",
                "Failed to download media! Make sure all URL(s) are valid and make sure you are connected to internet.",
            )

        btnDownload["state"] = "normal"
        btnDownload["text"] = "Download"

    # DOWNLOAD AUDIO PLAYLIST FUNCTION
    def downloadAudioPlaylist(self):
        outputDir = filedialog.askdirectory(
            parent=root, initialdir=os.getcwd(), title="Please select a folder:"
        )
        print(outputDir)

        print("[LOG] DOWNLOADING PLAYLIST")
        messagebox.askquestion(
            title="YMD",
            message=f"Downloading {txtUrls.get()} as a PLAYLIST! Is this correct?",
        )
        urls = txtUrls.get().split(" ")
        opts = {
            "ignoreerrors": True,
            "abort_on_unavailable_fragments": True,
            "format": "bestaudio/best",
            "writethumbnail": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
                {"key": "FFmpegMetadata"},
                {
                    "key": "EmbedThumbnail",
                    "already_have_thumbnail": False,
                },
            ],
            "addmetadata": True,
            "add-metadata": True,
            "outtmpl": outputDir + "/%(playlist_index)s-%(title)s.%(ext)s",
        }
        try:
            with YoutubeDL(opts) as ydl:
                ydl.download(urls)
                messagebox.showinfo("Success!", "Successfully downloaded media!")
        except:
            messagebox.showerror(
                "ERROR",
                "Failed to download media! Make sure all URL(s) are valid and make sure you are connected to internet.",
            )

        btnDownload["state"] = "normal"
        btnDownload["text"] = "Download"

    # DOWNLOAD VIDEO STANDARD FUNCTION
    def downloadVideo(self):
        outputDir = filedialog.askdirectory(
            parent=root, initialdir=os.getcwd(), title="Please select a folder:"
        )
        print(outputDir)

        print("[LOG] DOWNLOADING CONTENT FROM URLS")

        if varSearch.get() == 1:
            urls = "ytsearch: " + txtUrls.get()
        else:
            urls = txtUrls.get().split(" ")

        opts = {
            "outtmpl": outputDir + "/%(title)s-%(id)s.%(ext)s",
        }

        try:
            with YoutubeDL(opts) as ydl:
                ydl.download(urls)
                messagebox.showinfo("Success!", "Successfully downloaded media!")
        except:
            messagebox.showerror(
                "ERROR",
                "Failed to download media! Make sure all URL(s) are valid and make sure you are connected to internet.",
            )

        btnDownload["state"] = "normal"
        btnDownload["text"] = "Download"

    # DOWNLOAD VIDEO PLAYLIST FUNCTION
    def downloadVideoPlaylist(self):
        outputDir = filedialog.askdirectory(
            parent=root, initialdir=os.getcwd(), title="Please select a folder:"
        )
        print(outputDir)

        print("[LOG] DOWNLOADING PLAYLIST")
        messagebox.askquestion(
            title="YMD",
            message=f"Downloading {txtUrls.get()} as a PLAYLIST! Is this correct?",
        )
        urls = txtUrls.get().split(" ")
        opts = {
            "ignoreerrors": True,
            "abort_on_unavailable_fragments": True,
            "outtmpl": outputDir + "/%(playlist_index)s-%(title)s.%(ext)s",
        }
        try:
            with YoutubeDL(opts) as ydl:
                ydl.download(urls)
                messagebox.showinfo("Success!", "Successfully downloaded media!")
        except:
            messagebox.showerror(
                "ERROR",
                "Failed to download media! Make sure all URL(s) are valid and make sure you are connected to internet.",
            )

        btnDownload["state"] = "normal"
        btnDownload["text"] = "Download"

    def btnDownload_command(self):
        btnDownload["state"] = "disabled"
        btnDownload["text"] = "Downloading..."
        try:
            if varBox.get() == 0:  # IF PLAYLIST CHECKBOX IS NOT CHECKED
                if varRadio.get() == 1:  # IF AUDIO SELECTED
                    audioThread = Thread(target=self.downloadAudio)
                    audioThread.start()
                else:
                    videoThread = Thread(target=self.downloadVideo)
                    videoThread.start()
            else:
                if varRadio.get() == 1:  # IF AUDIO IS SELECTED
                    audioPlaylistThread = Thread(target=self.downloadAudioPlaylist)
                    audioPlaylistThread.start()
                else:
                    videoPlaylistThread = Thread(target=self.downloadVideoPlaylist)
                    videoPlaylistThread.start()
        except:
            btnDownload["state"] = "normal"
            btnDownload["text"] = "Download"

    def boxPlaylist_command(self):
        if varBox.get() == 1:
            print("[LOG] Playlist = True")
        else:
            print("[LOG] Playlist = False")

    def radioAudio_command(self):
        print("[LOG] Radio Button (Audio) Selected")

    def radioVideo_command(self):
        print("[LOG] Radio Button (Video) Selected")

    def boxSearch_command(self):
        if varSearch.get() == 1:
            varBox.set(0)
            boxPlaylist["state"] = "disable"
            print("[LOG] Search = True")
        else:
            boxPlaylist["state"] = "normal"
            print("[LOG] Search = False")

    def boxThumbnail_command(self):
        if varThumbnail.get() == 1:
            print("[LOG] Thumbnail = True")
        else:
            print("[LOG] Thumbnail = False")


if __name__ == "__main__":
    print("[LOG] Log has started!")
    print(
        "[LOG] You are using YMD-GUI BETA 0.6 (UNIX Edition)! Report any errors to OofySimpsonV3 on github."
    )

    root = tk.Tk()
    varBox = tk.IntVar()
    varRadio = tk.IntVar()
    varSearch = tk.IntVar()
    varThumbnail = tk.IntVar(value=1)
    app = App(root)
    root.mainloop()
