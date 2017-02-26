import os, time, sqlite3
from slackclient import SlackClient
from secrets import SLACK_BOT_TOKEN, BOT_ID # <== Storing my authentication there


# starterbot's ID as an environment variable
#BOT_ID = os.environ.get("BOT_ID")

#print SLACK_BOT_TOKEN
#print BOT_ID

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
DIE_COMMAND = "die"
MUSIC_COMMAND = "music"
EXHIBITION_COMMAND = "exhibition"
OUTDOOR_COMMAND = "outdoor"
HELP_COMMAND = "help"

# gets reset by @disney_work die command  - to kill off bot so it can be restarted
Alive = True

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_query(nature, location):
    
    """
      Process the album command
    """
    conn = sqlite3.connect('events.sqlite')
    cur = conn.cursor()
    event_list = []
    
    loc2 = "%"+location+"%"
    nat2 = "%" + nature +"%"

    cur.execute (" SELECT * FROM rssevents  WHERE (rssevents.Venue LIKE ? OR rssevents.Content LIKE ? ) AND (rssevents.Content LIKE ?)", (loc2,loc2, nat2))
        
    
    for row in cur: 
        count = 0
        event = []
        for field in row:
            if count == 0:
                event.append(field) # title
            elif count == 1:
                event.append(field) #content
            elif count == 4:
                event.append(field) #url
            elif count == 5:
                event.append(field) #startdate
            elif count ==6:
                event.append(field) #endate
            elif count == 7:
                event.append(field) #venue
            count +=1
        event_list.append(event)
    cur.close()
    return event_list

def handle_help(commands):
    """
      Process the help command
    """
    # Place holder for any attachments we want to send
    
    response = "My capabilities are few, but generally well-executed. \nI find that when mistakes do happen it is not at my end. So, to keep you right, here are some pointers:\n"

    # Add help message for each command
    response += "*" + HELP_COMMAND + "* - shows this message\n\n"
    response += "Try formatting your query as *Subject Location* \n"
    response += "e.g. *Music Aberdeen*  \n"
    response += "or *exhibition Forfar* "
    
    return response
    
def handle_music(command):
    
    """
      Process the music command
    """
  
    location_name = command.split()[1]
    

    response = handle_query ( 'music', location_name)
    rsp2 = ""
    for phrase in response:
        rsp2 = rsp2 + str(phrase) + " "

    response = "Here's what I found: \n" + rsp2
    return response

def handle_exhibition(command):
    
    """
      Process the exhibition command
    """

    location_name = command.split()[1]


    response = "I have found 4 exhibitions happening in " + location_name.title()
    return response

def handle_outdoor(command):
    
    """
      Process the outdoor command
    """
  #  conn = sqlite3.connect('myjazzalbums.sqlite')
  #  cur = conn.cursor()


    location_name = command.split()[1]

    response = "I have found 1 outdoors event happening in " + location_name.title()

    return response

def handle_command(command, channel):
    
    if command.lower().startswith(HELP_COMMAND):
        response = handle_help(command)
    elif command.lower().startswith(MUSIC_COMMAND):
        response = handle_music(command)
    elif command.lower().startswith(EXHIBITION_COMMAND):
        response = handle_exhibition(command)
    elif command.lower().startswith(OUTDOOR_COMMAND):
        response = handle_outdoor(command)
    elif command.lower().startswith(DIE_COMMAND):
        Alive = False
    else:
        response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("DisneyWork connected and running!")
        while True and Alive :
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
