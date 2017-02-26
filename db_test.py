
import os, time, sqlite3

def handle_query(nature, location):
    
    """
      Process the album command
    """
    conn = sqlite3.connect('events.sqlite')
    cur = conn.cursor()

    
    loc2 = "%"+location+"%"
    
    cur.execute (" SELECT * FROM rssevents  WHERE rssevents.Venue LIKE ? OR rssevents.Content LIKE ? ", (loc2,loc2))
        
    
    for row in cur: 
        count = 0
        for field in row:
            if count == 5:
                startdate = field.split()[0]
                print "startdate = " + startdate
            print field, " count " + str(count)
            count +=1
    cur.close()

response = handle_query("music", "Blue")

print response
