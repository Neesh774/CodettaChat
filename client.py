import tkinter as tk
from tkinter import Canvas, ttk
from tkinter.scrolledtext import ScrolledText
import re
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys

import long_responses as long

window = tk.Tk()
window.resizable(False, False)
window.title("GenCyber Agent ChatBot")
window.geometry("680x500")

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)

# messages
messageHeight = 20
clientMessages = [] 

messages_frame = tk.Frame(window,width=500)
my_msg = tk.StringVar()  # For the messages to be sent.
msg_list = ttk.Frame(messages_frame, height=450, width=650)

msg_list.pack(side=tk.LEFT)
canvas = Canvas(msg_list, height=1000000, width=650, scrollregion=(0,0,450,messageHeight))

scrollbar = tk.Scrollbar(msg_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)
canvas.pack()

messages_frame.pack()

#===================CHATBOT=====================
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response("That's great!", ["i'm", "well", "doing", "ok", "good", "not"], required_words=[])
    response('I am an avid enjoyer of cheese.', ['i', 'love', 'cheese'], required_words=['cheese'])
    response('I\'m a bot, but I\'m still learning.', ['i', 'am', 'a', 'bot'], required_words=['a', 'bot'])
    response('Never gonna give you up, never gonna let you down...', ['rickroll', 'rick', 'astley'], required_words=['never'])
    response("🎵WHAT IS LOVE? BABY DON'T HURT ME....DON'T HURT ME....NO MORE...🎵", ['love', 'what'], required_words=[])
    response("I loveeee puppies!", ['dog','animal','puppy', 'pet', 'puppies', "love", "like"], required_words=[])
    response("Kitties are the best!", ['kitty', 'kitties', 'cat', 'kitten', 'pet', 'animal', "I", "love", "like", "kittens"], required_words=[])
    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])
    response(long.R_CREATOR, ['creator', 'author', 'chatbot', 'who'], required_words=[])
    response(long.R_DISCORD_BOT, ['bot', 'discord', 'javascript'], required_words=['discord'])
    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

def chatbot_message(clientText):
    global messageHeight
    text = get_response(clientText)
    my_msg.set("")
    message = canvas.create_text(0, 0, text=text, width=100, justify='left')
    bounds = canvas.bbox(message)
    canvas.delete(message)
    botMessageTextHeight = bounds[3] - bounds[1]
    botMessageTextWidth = bounds[2] - bounds[0]
    botMessageHeight = botMessageTextHeight + 20
    botMessageWidth = botMessageTextWidth + 20
    canvas.create_rectangle(0, messageHeight, botMessageWidth, messageHeight + botMessageHeight,fill = "#E9EAEC", outline="#E9EAEC")
    canvas.create_text(botMessageWidth/2, messageHeight + (botMessageHeight/2), text=text, width=100, justify='left')
    messageHeight += (botMessageHeight + 20)
    canvas.config(scrollregion=(0, 0, 450, messageHeight+40))
    canvas.update()
    canvas.yview_moveto(1)
#================================================

# sending a message to the chatbot and the window
def sendClientMessage(event=None):
    global messageHeight
    if(len(my_msg.get()) != 0):
        client_socket.send(bytes(my_msg.get(), "utf8"))
        if my_msg.get() == "{quit}":
            client_socket.close()
            return sys.exit()
        text = my_msg.get()
        if(len(text) > 10 and len(clientMessages) == 0):
            text = text[:9]
        my_msg.set("")
        message = canvas.create_text(0, 0, text=text, width=100, justify='left')
        bounds = canvas.bbox(message)
        canvas.delete(message)
        clientMessageTextHeight = bounds[3] - bounds[1]
        clientMessageTextWidth = bounds[2] - bounds[0]
        clientMessageHeight = clientMessageTextHeight + 20
        clientMessageWidth = clientMessageTextWidth + 20
        if(len(clientMessages)== 0):
            messageHeight += 10
        canvas.create_rectangle(650-clientMessageWidth, messageHeight, 650, messageHeight + clientMessageHeight,fill = "#FAD02C", outline="#FAD02C")
        message = canvas.create_text(650 - (clientMessageWidth/2), messageHeight + (clientMessageHeight/2), text=text, width=100, justify='left')
        messageHeight += (clientMessageHeight + 20)
        canvas.config(scrollregion=(0, 0, 450, messageHeight+40))
        canvas.update()
        canvas.yview_moveto(1)
        if(len(clientMessages) > 3):
            chatbot_message(text)
        clientMessages.append(text)
#-------------------------------------Sending System Message
def sendSystemMessage(text):
    global messageHeight
    sysMessage = canvas.create_text(325, messageHeight, text=text, justify="center")
    height = canvas.bbox(sysMessage)[3] - canvas.bbox(sysMessage)[1]
    messageHeight+=(height + 10)
    canvas.config(scrollregion=(0, 0, 450, messageHeight+40))
    canvas.update()
    canvas.yview_moveto(1)
def sendWelcomeMessage(text):
    global messageHeight
    sysMessage = canvas.create_text(325, messageHeight, text=text, justify="center")
    height = canvas.bbox(sysMessage)[3] - canvas.bbox(sysMessage)[1]
    messageHeight+=(height + 30)
    canvas.config(scrollregion=(0, 0, 450, messageHeight+40))
    canvas.update()
    canvas.yview_moveto(1)
#------------------------------------Send User Message
def sendUserMessage(text):
    global messageHeight
    my_msg.set("")
    message = canvas.create_text(0, 0, text=text, width=100, justify='left')
    bounds = canvas.bbox(message)
    canvas.delete(message)
    botMessageTextHeight = bounds[3] - bounds[1]
    botMessageTextWidth = bounds[2] - bounds[0]
    botMessageHeight = botMessageTextHeight + 20
    botMessageWidth = botMessageTextWidth + 20
    canvas.create_rectangle(0, messageHeight, botMessageWidth, messageHeight + botMessageHeight,fill = "#90ADC6", outline="#90ADC6")
    canvas.create_text(botMessageWidth/2, messageHeight + (botMessageHeight/2), text=text, width=100, justify='left')
    messageHeight += (botMessageHeight + 20)
    canvas.config(scrollregion=(0, 0, 450, messageHeight+40))
    canvas.update()
    canvas.yview_moveto(1)
# message input
entry_field = tk.Entry(window, textvariable=my_msg)
entry_field.place(x=10, y=460, width=610, height=30)
entry_field.bind("<Return>", sendClientMessage)
def character_limit(entry_text):
    if len(my_msg.get()) > 100:
        my_msg.set(my_msg.get()[0:100])

my_msg.trace("w", lambda *args: character_limit(my_msg))  
send_button = tk.Button(window, text="↑", command=sendClientMessage)
send_button.place(x=625, y=460, width=30, height=30)

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if(msg.startswith("SERVER:")): 
                sendSystemMessage(msg[7:])
            elif(msg.startswith("WELCOME:")):
                sendWelcomeMessage(msg[8:])
            else:
                sendUserMessage(msg)
        except OSError:  # Possibly client has left the chat.
            break

def on_closing(event=None):
    my_msg.set("{quit}")
    sendSystemMessage("A user has left the chat")

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000  # Default value.
else:
    PORT = int(PORT)
BUFSIZ = 1024

ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
window.mainloop()  # Starts GUI execution.