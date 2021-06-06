from os import replace
import socket
import tkinter
from threading import Thread
from tkinter.constants import BOTTOM, DISABLED, END, INSERT, NORMAL
from tkinter import ttk

from PIL import Image, ImageTk


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            # Allows to add new text
            text.config(state=NORMAL)
            text.insert(END, f"{msg}\n", "msg")
            text.config(state=DISABLED)  # Makes text window read-only
            text.see(END)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # Set as an event to bind to <Return>
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(str.encode(msg, "utf8"))
    if msg == "-quit":
        client_socket.close()
        root.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("-quit")
    send()


def handle_focus(event):
    my_msg.set("")


root = tkinter.Tk()
root.title("LAN Chat")
root.geometry("700x420")
#root.resizable(False, False)
root.config(background="#1f1a29")

messages_frame = tkinter.Frame(root)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.".rjust(55))


# To navigate through past messages.
scrollbar = tkinter.Scrollbar(
    messages_frame, background="#565659", activebackground="#363638", border=0)
# Following will contain the messages.
text = tkinter.Text(
    messages_frame, yscrollcommand=scrollbar.set, width=83, height=20, background="#4c4163", highlightbackground="#4c4163", border=0, foreground="#c2c2c2")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages_frame.place(rely=0.02, relx=0.01)
text.pack()

entry_field = tkinter.Entry(
    root, textvariable=my_msg, background="#2d2836", border=0, highlightthickness=0, foreground="#c2c2c2", font="12")
entry_field.bind("<Return>", send)
entry_field.bind("<FocusIn>", handle_focus)
entry_field.place(rely=0.87, relx=0.01, width=500, height=40)

img = Image.open(r"images/btn.png")
resize_photo = img.resize((50, 50))
imgTK = ImageTk.PhotoImage(resize_photo)

send_button = tkinter.Button(
    root, image=imgTK, borderwidth=0, highlightthickness=0, command=send, background="#1f1a29", activebackground="#1f1a29")

send_button.place(rely=0.855, relx=0.73)
root.protocol("WM_DELETE_WINDOW", on_closing)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 2004))

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
