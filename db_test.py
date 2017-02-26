
import os, time, sqlite3

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

response = handle_query("music", "Church")

print response
