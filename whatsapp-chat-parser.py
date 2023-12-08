"""
Original code: https://github.com/karthikchiru12/ChatToCSV
Adapted by Andrea Riboni
"""

import os
import numpy as np
import pandas as pd
import regex as re
import sys


class WhatsAppChatToCSV:

    def __init__(self, input_filename, output_filename="output", path=os.getcwd(), return_df = False):
        """
        input:
            input_filename  : Whatsapp exported chat
            output_filename : name for csv file to be saved
            path            : Path in which the files are located
        """

        self.input_filename = input_filename
        self.output_filename = output_filename
        self.path = path
        self.return_df = return_df
        self.messages = []
        self.users = []
        self.dates = []
        self.times = []

    def addPointerToEachLine(self):
        # Improved regex pattern to match dates more accurately
        dates_pattern = r"\b[0-9]{1,2}[-/_][0-9]{1,2}[-/_][0-9]{2,4}\b"
        self.data = re.sub(dates_pattern, lambda x: '<*+*>' + x.group(), self.data)
        self.data = self.data.split('<*+*>')

    def seperatelyExtractContent(self):
        messages = []
        dates = []
        times = []
        users = []
        for i in range(len(self.data)):
            if len(self.data[i]) != 0 and self.data[i]:
                # Extract date, time, user, and message using regex pattern
                pattern = r"(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{1,2}) - ([^:]+): (.+)"
                match = re.match(pattern, self.data[i])
                if match:
                    # Verify if the extracted date and time match the expected format
                    try:
                        date = pd.to_datetime(match.group(1), format='%d/%m/%y').strftime('%Y-%m-%d')
                        time = pd.to_datetime(match.group(2), format='%H:%M').strftime('%H:%M:%S')
                        dates.append(date)
                        times.append(time)
                        users.append(match.group(3))
                        messages.append(match.group(4))
                    except ValueError:
                        # The extracted date or time does not match the expected format, skip this line
                        continue

        self.messages = messages
        self.users = users
        self.dates = dates
        self.times = times

        return None

    def removeUnwantedRows(self):

        """
        Removes rows with media omitted or deleted messages
        """

        rows_to_remove = []
        for i in range(len(self.dataframe)):
            if self.dataframe.values[i][2].strip('\n') == self.dataframe.values[i][3].strip('\n') or '<Media omitted>' in self.dataframe.values[i][3] or 'This message was deleted' in self.dataframe.values[i][3]:
                rows_to_remove.append(i)
        self.dataframe = self.dataframe.drop(
            rows_to_remove, axis=0).reset_index(drop=True)

        return None

    def buildCSV(self):

        """
        Builds the final csv
        """

        with open(self.path+'/'+self.input_filename, encoding='utf-8') as file:
            self.data = file.read()

        self.addPointerToEachLine()
        self.seperatelyExtractContent()
        finalOutput = {'Date': self.dates, 'Time': self.times,
                       'User': self.users, 'Message': self.messages}
        self.dataframe = pd.DataFrame(finalOutput)
        self.removeUnwantedRows()
        #self.dataframe.to_csv(self.output_filename+".csv",index=False)

        if self.return_df:
            return self.dataframe

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR: incorrect number of arguments!")
        print("How to use it:")
        print("    python3 whatsapp-chat-parser.py <chat_history_txt> <output_file_csv>")
        print("Example:")
        print("    python3 telegram-chat-parser.py movies_group.json output.csv")
        sys.exit()

    w = WhatsAppChatToCSV(sys.argv[1],sys.argv[2],return_df = True)
    chat = w.buildCSV()
    chat['Date'] = pd.to_datetime(chat['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
    chat = chat.rename(columns={'Date': 'day'})
    chat['msg_id'] = range(1, len(chat) + 1)
    chat = chat.rename(columns={'Time': 'time', 'User': 'sender', 'Message': 'msg_content'})
    chat.to_csv(sys.argv[2])