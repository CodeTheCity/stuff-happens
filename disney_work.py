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

# gets reset by @disney_work die command  - to kill off bot so it can be restarted
Alive = True

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_help(commands):
    """
      Process the help command
    """
    # Place holder for any attachments we want to send
    
    response = "My capabilities are few, but generally well-executed. \nI find that when mistakes do happen it is not at my end. So, to keep you right, here are some pointers:\n"

    # Add help message for each command
    response += "*" + HELP_COMMAND + "* - shows this message\n"
    
    return response
	
def handle_music(command):
    
    """
      Process the music command
    """
  #  conn = sqlite3.connect('myjazzalbums.sqlite')
  #  cur = conn.cursor()

    if command [-1] == "?": 
        music_name = command[5:-1].strip()
    else: 
        music_name = command[5:].strip()

    #cur.execute (" SELECT Artist.name FROM Album JOIN Artist ON Artist.id = Album.artist_id WHERE Album.title =?", (album_name,) )
    """    
    count = 0
    response =  'Albums called ' + album_name + '\n'

    for row in cur :
        response += "Artist: " + row[0]
        count = count + 1
    response = "I have "+ str (count) +" " +  response
    return response
    cur.close()
	"""
	
	location = music_name.split()[1]
	response = "I have found 2 music events in " + location.title
	return response

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
	
	if command.lower().startswith(HELP_COMMAND):
        response = handle_help (command)
	elif command.lower().starswith(MUSIC_COMMAND :
		response = handle_music (command)
    elif command.lower().startswith(DIE_COMMAND):
        Alive = False
	
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
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
