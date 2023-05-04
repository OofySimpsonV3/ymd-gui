# YMD ALPHA 0.3

import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import filedialog
import os
from yt_dlp import YoutubeDL
import ffmpeg
from pytube import YouTube

class App:
    def __init__(self, root):
        #setting title
        root.title("YMD for Unix (GUI)")
        #setting window size
        width=462
        height=124
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        global btnDownload
        btnDownload=tk.Button(root)
        btnDownload["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        btnDownload["font"] = ft
        btnDownload["fg"] = "#000000"
        btnDownload["justify"] = "center"
        btnDownload["text"] = "Download"
        btnDownload.place(x=10,y=50,width=444,height=37)
        btnDownload["command"] = self.btnDownload_command

        global boxPlaylist
        boxPlaylist=tk.Checkbutton(root)
        ft = tkFont.Font(family='Times',size=10)
        boxPlaylist["font"] = ft
        boxPlaylist["fg"] = "#333333"
        boxPlaylist["justify"] = "center"
        boxPlaylist["text"] = "Playlist (BETA)"
        boxPlaylist.place(x=0,y=90,width=118,height=30)
        boxPlaylist["offvalue"] = "0"
        boxPlaylist["onvalue"] = "1"
        boxPlaylist["command"] = self.boxPlaylist_command
        boxPlaylist["variable"] = varBox

        global txtUrls
        txtUrls=tk.Entry(root)
        txtUrls["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        txtUrls["font"] = ft
        txtUrls["fg"] = "#333333"
        txtUrls["justify"] = "left"
        txtUrls["text"] = "URLs (Seperate multiple URLs with spaces!)"
        txtUrls.place(x=10,y=10,width=441,height=33)

        global radioAudio
        radioAudio=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        radioAudio["font"] = ft
        radioAudio["fg"] = "#333333"
        radioAudio["justify"] = "center"
        radioAudio["text"] = "Audio (mp3 + metadata)"
        radioAudio.place(x=190,y=90,width=177,height=31)
        radioAudio["value"] = 1
        radioAudio["command"] = self.radioAudio_command
        radioAudio["variable"] = varRadio

        global radioVideo
        radioVideo=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        radioVideo["font"] = ft
        radioVideo["fg"] = "#333333"
        radioVideo["justify"] = "center"
        radioVideo["text"] = "Video"
        radioVideo.place(x=370,y=90,width=86,height=30)
        radioVideo["value"] = 0
        radioVideo["command"] = self.radioVideo_command
        radioVideo["variable"] = varRadio

    def btnDownload_command(self):
        print("[LOG] BUTTON PRESS")
        if varRadio.get() == 1:
            print("[LOG] DOWNLOADING AUDIO")
            # DOWNLOADING AUDIO!!!
            if txtUrls.get() == "":
                print("[ERROR] Blank input! Please add atleast 1 valid URL...")
                messagebox.showerror(title="ERROR", message="Blank input! Please add atleast 1 valid URL...")
            else:
                outputDir = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title="Please select a folder:")
                print(outputDir)
                
                if varBox.get() == 0:    # IF CHECKBOX IS NOT CHECKED
                    # DOWNLOAD URLS NORMALLY
                    print("[LOG] DOWNLOADING CONTENT FROM URLS")
                    urls = txtUrls.get()

                    opts = {
                        'outtmpl': outputDir + '/%(title)s-%(id)s.%(ext)s',
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        },
                        {
                            'key': 'FFmpegMetadata'
                        }],
                        'addmetadata': True,
                        'add-metadata': True,
                    }
                    try:
                        with YoutubeDL(opts) as ydl:
                            ydl.download(urls)
                            messagebox.showinfo("Success!", "Successfully downloaded media!")
                    except:
                        messagebox.showerror("ERROR", "Failed to download media! Make sure all URL(s) are valid and make sure you are connected to internet.")
                else:
                    # DOWNLOAD PLAYLIST
                    print("[LOG] DOWNLOADING PLAYLIST")
                    messagebox.askquestion(title="YMD", message=f"Downloading {txtUrls.get()} as a PLAYLIST! Is this correct?")
                    urls = txtUrls.get()
                    opts = {
                        'ignoreerrors': True,
                        'abort_on_unavailable_fragments': True,
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        },
                        {
                            'key': 'FFmpegMetadata'
                        }],
                        'addmetadata': True,
                        'add-metadata': True,
                        'outtmpl': outputDir + '/%(playlist_uploader)s ## %(playlist)s\%(title)s ## %(uploader)s ## %(id)s.%(ext)s',
                    }
                    try:
                        with YoutubeDL(opts) as ydl:
                            ydl.download(urls)
                            messagebox.showinfo("Success!", "Successfully downloaded media!")
                    except:
                        messagebox.showerror("ERROR", "Failed to download media! Make sure all URL(s) are valid and make sure you are connected to internet.")
        else:
            # DOWNLOAD VIDEO!!!!

            outputDir = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title="Please select a folder:")
            print(outputDir)

            if varBox.get() == 0:    # IF CHECKBOX IS NOT CHECKED
                # DOWNLOAD URLS NORMALLY
                print("[LOG] DOWNLOADING CONTENT FROM URLS")
                urls = txtUrls.get()

                opts = {
                    'outtmpl': outputDir + '/%(title)s-%(id)s.%(ext)s',
                    'format': 'bestvideo/best'
                }
                try:
                    with YoutubeDL(opts) as ydl:
                        ydl.download(urls)
                        messagebox.showinfo("Success!", "Successfully downloaded media!")
                except:
                    messagebox.showerror("ERROR", "Failed to download media! Make sure all URL(s) are valid and make sure you are connected to internet.")

            else:
                # DOWNLOAD PLAYLIST
                print("[LOG] DOWNLOADING PLAYLIST")
                messagebox.askquestion(title="YMD", message=f"Downloading {txtUrls.get()} as a PLAYLIST! Is this correct?")
                urls = txtUrls.get()
                opts = {
                    'ignoreerrors': True,
                    'abort_on_unavailable_fragments': True,
                    'format': 'bestvideo/best',
                    'outtmpl': outputDir + '/%(playlist_uploader)s ## %(playlist)s\%(title)s ## %(uploader)s ## %(id)s.%(ext)s',
                }
                try:
                    with YoutubeDL(opts) as ydl:
                        ydl.download(urls)
                        messagebox.showinfo("Success!", "Successfully downloaded media!")
                except:
                    messagebox.showerror("ERROR", "Failed to download media! Make sure all URL(s) are valid and make sure you are connected to internet.")



    def boxPlaylist_command(self):
        print("command")


    def radioAudio_command(self):
        print("command")


    def radioVideo_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    varBox = tk.IntVar()
    varRadio = tk.IntVar()
    app = App(root)
    root.mainloop()
