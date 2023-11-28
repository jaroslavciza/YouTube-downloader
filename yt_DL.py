from pytube import YouTube, Playlist
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import customtkinter
import re
import pathlib
from urllib import request

class Frame_YTinputURL(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.label  = customtkinter.CTkLabel(self, text="YouTube video/playlist URL:")
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.inputYT = customtkinter.CTkEntry(self, height=15, width=500)
        self.inputYT.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.addButton = customtkinter.CTkButton(self, text="Přidat", width=70)
        self.addButton.grid(row=0, column=2, padx=(0,30), pady=5, sticky="e")
        
class Frame_YTlist(customtkinter.CTkScrollableFrame ):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)  
        self.configure(label_text="Seznam videí ke stažení")
        
class Frame_Parameters(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)        
        self.audioOnly = customtkinter.CTkCheckBox(self, text="stáhnout pouze audio stopu")
        self.audioOnly.grid(row=0, column=0, padx=20, pady=20, sticky="w")           

class Frame_Paths(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)    
        self.label  = customtkinter.CTkLabel(self, text="Cílová cesta:")
        self.label.grid(row=0, column=0, padx=(20,0), pady=10, sticky="w")        
        self.path = customtkinter.CTkEntry(self, height=15, width=400)
        self.path.grid(row=0, column=1, padx=(0,20), pady=20, sticky="we")       
        self.path.insert(0, str(pathlib.Path().resolve()))
        self.path.configure(state="disabled")        

class Frame_Download (customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
        self.counter  = customtkinter.CTkLabel(self, text="")
        self.counter.grid(row=0, column=0, padx=(20,0), pady=10, sticky="w")        
        # self.progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal")
        # self.progressbar.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        self.deleteYTlistButton = customtkinter.CTkButton(self,text="Smazat seznam videí", width=150, state="disabled")
        self.deleteYTlistButton.grid(row=0, column=1, padx=(0,30), pady=20, sticky="e") #sticky to east and west             
        self.downloadButton = customtkinter.CTkButton(self,text="Stáhnout", width=150, state="disabled")
        self.downloadButton.grid(row=0, column=2, padx=(0,30), pady=20, sticky="e") #sticky to east and west        

class Frame_Messages(customtkinter.CTkFrame ):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #self.configure(label_text="Výpis logu")   
        self.grid_columnconfigure((0), weight=1)  
        self.messageBox = customtkinter.CTkTextbox(master=self, corner_radius=0)
        self.messageBox.grid(row=0, column=0, sticky="nsew")             

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube downloader - autor: Jaroslav C.")
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.YT_dict = {}
        self.deleteButton_dict = {}

        self.fr_YTinputURL = Frame_YTinputURL(master=self)
        self.fr_YTinputURL.grid(row=0, column=0, padx=20, pady=(20,5), sticky="ew", columnspan=2)

        self.fr_YTlist = Frame_YTlist(master=self)
        self.fr_YTlist.grid(row=1, column=0, padx=20, pady=5, sticky="ew", columnspan=2)

        self.fr_Paths = Frame_Paths(master=self)
        self.fr_Paths.grid(row=2, column=0, padx=(20,5), pady=5, sticky="ew")        

        self.fr_Parameters = Frame_Parameters(master=self)
        self.fr_Parameters.grid(row=2, column=1, padx=(5,20), pady=5, sticky="ew")
        
        self.fr_Download  = Frame_Download(master=self)
        self.fr_Download.grid(row=3, column=0, padx=20, pady=5, sticky="ew", columnspan=2)

        self.fr_Messages = Frame_Messages(master=self)
        self.fr_Messages.grid(row=4, column=0, padx=20, pady=(5,20), sticky="ew", columnspan=2)

        self.fr_Download.downloadButton.bind("<Button-1>", self.downloadButton_click)
        self.fr_Download.deleteYTlistButton.bind("<Button-1>", self.deleteYTlistButton_click)
        self.fr_YTinputURL.inputYT.bind("<Return>", self.decode_YT_URL)
        self.fr_YTinputURL.inputYT.bind("<Button-3>", self.insertClipboard)
        self.fr_YTinputURL.addButton.bind("<Button-1>", self.decode_YT_URL)
        self.fr_Paths.path.bind("<Button-1>", self.choosePath_click)

        #self.isInternetRuning()
 
    def add_YT_URL (self, URL):
        author = ""
        title = ""
        if self.isInternetRuning():
            try:
                yt = YouTube(URL)
                author = yt.author
                title = yt.title
            except:
                messagebox.showerror('Chyba', 'Chyba při importu videa!')  
            else:
                if URL not in self.YT_dict.keys():     
                    #print ("Adding URL: ", URL)      
                    self.insertMessage("Přidávám video \"" + author + " - " + title + "\" do seznamu ke stažení.")
                    label = customtkinter.CTkLabel(self.fr_YTlist, text=author+ " - " + title)
                    label.grid(row=len(self.YT_dict), column=0, padx=15, pady=5, sticky="w")
                    self.YT_dict[URL] = label

                    deleteButton = customtkinter.CTkButton(self.fr_YTlist, text="Smazat", command=lambda: self.delete_YT(URL), width=70)
                    deleteButton.grid(row=len(self.YT_dict)-1, column=1, padx=15, pady=5, sticky="e")
                    self.deleteButton_dict[URL] = deleteButton
                else:
                    messagebox.showerror('Chyba', 'Video je již v seznamu ke stažení!')  
            self.updateDLCounter()
            self.fr_YTinputURL.inputYT.delete('0', tk.END)         
        
    def decode_YT_URL(self, *args):
        URL = self.fr_YTinputURL.inputYT.get()  
        if self.isInternetRuning():
            if ("youtube.com/playlist?list=" in URL) or (".youtube.com/watch?v=" in URL and "&list=" in URL): #kvuli chybe v pytube musim otestovat alespon takhle, jinak callback error
                try:
                    playlist = Playlist(URL)
                except:
                    #print ("Not a playlist")
                    messagebox.showerror('Chyba', 'Odkaz neobsahuje plalist YouTube!')
                else:
                    for video in playlist.video_urls:
                        self.add_YT_URL(video)
                        self.update() #jinak se widgety updatenou s novymi daty az po dokonceni loopu
                self.insertMessage("******************************************* Přidávání videí do seznamu ke stažení dokončeno. *******************************************")

            #samotne video
            if ("youtube.com/watch?v=" in URL) and ("&list=" not in URL):
                try:
                    yt = YouTube(URL)
                except Exception as e:
                    #print ("Error")
                    messagebox.showerror('Chyba', 'Chybná adresa URL youtube videa!')
                else:       
                    self.add_YT_URL(URL)

    def delete_YT(self, *args):
        URL = args[0]
        if URL in self.YT_dict.keys():
            #print("Removing URL:", URL)
            self.insertMessage("Odebírám video " + URL + " ze seznamu ke stažení.")
            label = self.YT_dict.pop(URL)
            label.destroy()
            if URL in self.deleteButton_dict.keys():
                button = self.deleteButton_dict.pop(URL)
                button.destroy()
            self.updateDLCounter()

    def updateDLCounter(self, *args):
        if len(self.YT_dict) > 0:
            self.fr_Download.counter.configure(text="Celkem videí ke stažení: " + str(len(self.YT_dict)))
            self.fr_Download.downloadButton.configure(state="normal")
            self.fr_Download.deleteYTlistButton.configure(state="normal")
        else:
            self.fr_Download.counter.configure(text="")       
            self.fr_Download.downloadButton.configure(state="disabled")         
            self.fr_Download.deleteYTlistButton.configure(state="disabled")         

    def downloadButton_click(self, *args):
        if self.fr_Download.downloadButton.cget("state") == "normal":
            if self.isInternetRuning():
                self.fr_Download.downloadButton.configure(state = "disabled")
                self.update()
                for video in self.YT_dict:
                    try:
                        yt = YouTube(video)   
                        author = re.sub('[\\\\|/!?\'":;,.]+', '', yt.author)
                        title  = re.sub('[\\\\|/!?\'":;,.]+', '', yt.title)
                        if self.fr_Parameters.audioOnly.get() == 1:
                            yd = yt.streams.filter(only_audio=True).first()
                            yd.download(output_path = self.fr_Paths.path.get(), filename=f"{author} - {title}.mp3")
                            self.insertMessage("Stahování audiostopy \"" + author + " - " + title + "\" dokončeno.")
                        else:
                            yd = yt.streams.get_highest_resolution()  
                            yd.download(output_path = self.fr_Paths.path.get(), filename=f"{author} - {title}.mp4")
                            self.insertMessage("Stahování videa \"" + author + " - " + title + "\" dokončeno.")
                        self.update() #jinak se widgety updatenou s novymi daty az po dokonceni loopu
                    except Exception as e:
                        self.fr_Messages.messageBox.insert("0.0", "Chyba: " + str(e) + " \n")             
                self.insertMessage("************************************************** Stahování seznamu videí dokončeno. **************************************************")
                self.fr_Download.downloadButton.configure(state = "normal")

    def deleteYTlistButton_click (self,*args):
        if self.fr_Download.deleteYTlistButton.cget("state") == "normal":
            self.fr_Download.deleteYTlistButton.configure(state = "disabled")
            self.YT_dict = {}
            self.deleteButton_dict = {}
            for widget in self.fr_YTlist.winfo_children():
                widget.destroy()
            self.updateDLCounter()
            self.insertMessage("**************************************************** Seznam videí ke stažení vymazán. **************************************************")   

    def choosePath_click (self, *args):
        filePath = filedialog.askdirectory()
        if filePath != "":
            self.fr_Paths.path.configure(state="normal")
            self.fr_Paths.path.delete('0', tk.END)  
            self.fr_Paths.path.insert(0, filePath)
            self.fr_Paths.path.configure(state="normal")

    def insertClipboard(self, *args):
        self.fr_YTinputURL.inputYT.delete('0', tk.END)
        self.fr_YTinputURL.inputYT.insert('0', self.clipboard_get())
    
    def insertMessage(self, message):
         self.fr_Messages.messageBox.configure(state="normal")
         self.fr_Messages.messageBox.insert("0.0", str(message) + " \n") 
         self.fr_Messages.messageBox.configure(state="disabled")

    def isInternetRuning(self):
        try:
            request.urlopen('https://www.youtube.com/', timeout=1)
            return True
        except request.URLError as err: 
            self.insertMessage("!!! Nelze se připojit k YouTube.com. Zkontrolujte připojení k internetu. !!!")
            messagebox.showerror('Chyba', 'Nelze se připojit k YouTube.com!')  
            return False

app = App()
app.mainloop()

#pyinstaller --name NAZEV_APLIKACE --onefile --windowed  nazevSkiptu.py
#pyinstaller --name "YT downloader by JC" --onefile --windowed --icon=icon.ico "g:/Můj disk/Programování/Python/youtubeDL/yt_DL.py"       
#d:\_export> pyinstaller --onefile --name "Youtube DL by JC" --noconsole 'G:\Můj disk\Programování\Python\youtubeDL\yt_DL.py'

# max kvalita nefunguje?
