from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
import dateutil.parser as parser
from datetime import datetime
import csv
import pandas as pd

# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('token.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = build('gmail', 'v1', http=creds.authorize(Http()))

# Call the Gmail API
user_id = 'me'
label_id_one = 'INBOX'
label_id_two = 'UNREAD'

# Getting all the unread messages from Inbox
# labelIds can be changed accordingly
unread_msgs = GMAIL.users().messages().list(userId='me', labelIds=[label_id_one,label_id_two]).execute()

# We get a dictonary. Now reading values for the key 'messages'
mssg_list = unread_msgs['messages']

print("Total unread messages in inbox: ", str(len(mssg_list)))

final_list = []
final_msg = []
for mssg in mssg_list[:10]:
    temp_dict = {}
    m_id = mssg['id']  # get id of individual message
    message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()  # fetch the message using API
    payld = message['payload']  # get payload of the message
    headr = payld['headers']  # get header of the payload

    for one in headr:  # getting the Subject
        if one['name'] == 'Subject':
            msg_subject = one['value']
            temp_dict['Subject'] = msg_subject
        else:
            pass

    for two in headr:  # getting the date
        if two['name'] == 'Date':
            msg_date = two['value']
            date_parse = (parser.parse(msg_date))
            m_date = (date_parse.date())
            temp_dict['Date'] = str(m_date)
        else:
            pass

    for three in headr:  # getting the Sender
        if three['name'] == 'From':
            msg_from = three['value']
            temp_dict['Sender'] = msg_from
        else:
            pass

    temp_dict['Snippet'] = message['snippet']  # fetching message snippet

    try:

        pyld = message['payload']
        body = pyld['body']
        part_data = body['data']  # fetching data from the body
        clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
        soup = BeautifulSoup(clean_two, "lxml")
        mssg_body = soup.get_text()
        msg = mssg_body.split(" ")
        nmsg = []
        for i in msg:
            if i.isalnum():
                nmsg.append(i)

        msg = ' '.join(nmsg)

    except:
        pass


    print(temp_dict)
    try:
        final_list.append(temp_dict['Sender']+" "+temp_dict['Subject']+" "+temp_dict['Snippet'])  # This will create a dictonary item in the final list
        final_msg.append(msg)
    except:
        pass



print("Total messaged retrived: ", str(len(final_list)))



df = pd.DataFrame({'Snippets':final_list,'Message':final_msg})
df.to_csv('sample.csv')



data = pd.DataFrame.from_csv('sample.csv')
data['class'] = "NaN"

for i in range(len(data)):
    print(data['Snippets'][i])
    data.at[i,'class'] = input("Enter I or NI\n")

print(data)
data.to_csv('sample.csv')
