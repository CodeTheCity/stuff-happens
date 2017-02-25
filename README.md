# stuff-happens
Chatbot project to help you find relevant events in your area
using RSS feeds from Angus, Aberdeen City and Aberdeenshire.

The Bot format follows the tutorial [here](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)

Instead of using virtualenv and environment variables we stored the SLACK_BOT_TOKEN, BOT_ID in a secrets.py file (which is not added to this repo - but see secrets.example for the format).

The sqlite database (created with FME) is populated by pulling in the RSS event feeds from:

- http://www.edinburghguide.com/rss.xml
- https://www.visitangus.com/rss/events
- http://aberdeencity.gov.uk/accapps/rss/eventrss.aspx
- http://www.whatsonscotland.com/listings/whats-on?target=0&type=rss
- http://www.scotlandfoodanddrink.org/site/rss/events.aspx
- http://www.aberdeenshireevents.org.uk/event/rss.xml 

The database can be updated on a schedule to ensure valid results are returned.