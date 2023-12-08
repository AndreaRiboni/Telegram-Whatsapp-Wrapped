# Chat-Wrapped: a chat mining application
A python tool to analyze your telegram or whatsapp chats. This script works for both private and group chats. The employed analysis are
- Number of messages per day
- Number of messages per day per person
- General statistics about the number of messages per day
- Dates with the highest or lowest message count
- Dates with the highest or lowest message count per person
- Average sender distribution
- Number of messages per month
- Number of messages per day of week
- Number of messages per hour of day
- Number of messages per minute of hour
- Common words
- Common words per person
- Message length in number of words and number of characters
- Message length in number of words and number of characters per sender
- Response time
- Response time per sender
- Topic modelling using LDA
- Sentiment analysis
- Sentiment analysis per month
- Emotion analysis
- Emotion analysis per month
- Reply graph
- Reply heatmap
- Top repliers graph

The script has been developed for Telegram chats. Whatsapp chats are supported, but since they are not standardized during the exportation (mostly the date format), it might be necessary to perform minor tweaking.

## How to use
### Export the chat
Export the telegram chat from the desktop application in JSON format
- Select the telegram chat you want to export
- Click the "more options" icon and click "Export chat history"
- Unselect all types of media (no photos, no videos, no stickers...)
- Change the "Format" from HTML to JSON
- Click "Export"

### Convert to CSV
Then move the output file "result.json" to the project root folder and run the python parser. This will convert your JSON file to a better-manageable CSV file.

To run it, open the terminal and enter the following command
> python .\telegram-chat-parser.py result.json

The script will ask you for the output file path and name. You can type what you want, let's say
> chat_dataset.csv

### Install the requirements
Finally, it is possible to run the Jupyter Notebook. Install the needed requirements:
> pip install -r requirements.txt

### Run the analysis
And run the notebook. Remember to change the file path in the first cell!
> chat_path = 'YOUR_FILE_PATH.csv'

