import cv2
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
username = 'jonasml'
password = 'jonasml0104'
endpoint = 'stream1'
ip = '192.168.0.186:554'

cap = None

def start_stream():
    global cap
    cap = cv2.VideoCapture(f'rtsp://{username}:{password}@{ip}/{endpoint}')

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=image)
            label2.imgtk = imgtk
            label2.configure(image = imgtk)
            label2.after(10, update_frame)
    update_frame()

def stop_stream():
    global cap
    if cap:
        cap.release()
        label2.config(image='')





root = Tk()
root.title("eksempel")
root.configure(background="red")
root.minsize(200, 200)
root.maxsize(1920, 1080)
root.geometry("300x300+50+50")


tabsystem = ttk.Notebook(root)
tab1 = Frame(tabsystem)
tabsystem.add(tab1, text="Foerste tab")
tabsystem.pack(expand=1, fill="both")

label = Label(tab1, text="hej med dig, din steg")
label.grid(column=1, row=1, padx=40, pady=40)


tab2 = Frame(tabsystem)
tabsystem.add(tab2, text="Anden tab")
tabsystem.pack(expand=1, fill="both")


label2 = ttk.Label(tab2)
label2.pack()

start_button = ttk.Button(tab2, text="Start Stream", command=start_stream)
start_button.pack()
stop_button = ttk.Button(tab2, text="Stop Stream", command=stop_stream)
stop_button.pack()



root.mainloop()
