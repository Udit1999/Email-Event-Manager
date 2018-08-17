import Gmail
import Classifier
from  Classifier import predictions
import pandas as pd
import tkinter as tk

Inbox = pd.DataFrame.from_csv('Inbox.csv')
root = tk.Tk()

logo = tk.PhotoImage(file="tenor.gif")
root.title("New Message Arrived")

msg = tk.Message(root,text = Inbox['Snippets'][0])
msg.config(bg = 'black',fg = 'white',font = ('times',16))
msg.pack()

tk.mainloop()


