import socket
import tkinter

from threading import Thread
from tkinter import ttk
from tkinter.constants import DISABLED, END, NORMAL
from PIL import Image, ImageTk

# region Methods


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

# endregion Methods


# region Widget instants
root = tkinter.Tk()
root.title("LAN Chat")
root.geometry("700x420")
root.resizable(False, False)
root.config(background="#1f1a29")

messages_frame = tkinter.Frame(root)
# Text widget that contains all the messages
text = tkinter.Text(messages_frame)
scrollbar = tkinter.Scrollbar(messages_frame)
input_field = tkinter.Entry(root)
# Button image
img = Image.open(r"images/btn.png")
resize_photo = img.resize((50, 50))
imgTK = ImageTk.PhotoImage(resize_photo)
send_button = tkinter.Button(root)
# endregion Widget instants

# region Widget configs
root.protocol("WM_DELETE_WINDOW", on_closing)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.".rjust(55))

scrollbar.config(background="#565659", activebackground="#363638", border=0)

text.config(yscrollcommand=scrollbar.set, width=83, height=20, background="#4c4163",
            highlightbackground="#4c4163", foreground="#c2c2c2")

send_button.config(image=imgTK, borderwidth=0, highlightthickness=0,
                   command=send, background="#1f1a29", activebackground="#1f1a29")

input_field.config(textvariable=my_msg, background="#2d2836",
                   border=0, highlightthickness=0, foreground="#c2c2c2", font="12")

input_field.bind("<Return>", send)
input_field.bind("<FocusIn>", handle_focus)
# endregion Widget configs

# region Widget placement
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages_frame.place(rely=0.02, relx=0.01)
text.pack()
input_field.place(rely=0.87, relx=0.01, width=500, height=40)
send_button.place(rely=0.855, relx=0.73)
# endregion Widget placement

# region Socket setup and mainloop
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 2004))

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
# endregion Socket setup and mainloop
