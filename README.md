# stuff-happens
Chatbot project to help you find relevant events in your area
using RSS feeds from Angus, Aberdeen City, Aberdeenshire and Edinburgh.

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

Fields in the database are:

- Title
- Content
- Id
- PublishedDate
- LinkURI
- StartDate
- EndDate
- Venue

and we've added two more: 
- Category 
- Tags

Where there are categories in at least one of the RSS feeds most do not. 

Our aim is that programatically we will infer categorisation and tagging from fields such as Title and Content. 

It may also be possible to use a tool such as [Word2Vec](https://github.com/danielfrg/word2vec) to establish relationships to standard terminologies.

Finally it was suggested at CTC8 that once we get this running, we could then provide an enriched meta RSS feed back out from our system.

Not all RSS feeds are created equal!