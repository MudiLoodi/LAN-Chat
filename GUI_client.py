import socket
from threading import Thread
import tkinter
from tkinter.constants import DISABLED, END, INSERT, NORMAL


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            # Allows to add new text
            text.config(state=NORMAL)
            text.tag_config("msg", background="lightsteelblue",
                            foreground="black", wrap='word')
            text.insert(END, f"{msg}\n", "msg")
            text.config(state=DISABLED)  # Makes it read-only
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
root.geometry("400x340")
#root.resizable(False, False)

messages_frame = tkinter.Frame(root)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")  # Add later .rjust(50)


# To navigate through past messages.
scrollbar = tkinter.Scrollbar(messages_frame)
text = tkinter.Text(messages_frame)
text.pack()
# Following will contain the messages.
# msg_list = tkinter.Listbox(messages_frame, height=15,
#                           width=50, yscrollcommand=scrollbar.set, activestyle="none", selectbackground="white", highlightcolor="white")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

# msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(root, textvariable=my_msg, width=100)
entry_field.bind("<Return>", send)
entry_field.bind("<FocusIn>", handle_focus)
entry_field.pack()
# entry_field.place(y=200)
send_button = tkinter.Button(root, text="Send", command=send)
# send_button.place(y=240)
send_button.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 2004))

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
