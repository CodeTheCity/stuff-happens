# stuff-happens
Chatbot project to help you find relevant events in your area
using RSS feeds from Angus, Aberdeen City and Aberdeenshire.

The Bot format follows the tutorial [here](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)

Instead of using virtualenv and environment variables we stored the SLACK_BOT_TOKEN, BOT_ID in a secrets.py file (which is not added to this repo - but see secrets.example for the format).

The sqlite database is created by pulling in the RSS event feeds 
from VisitAngus.com, Aberdeencity.gov.uk, AberdeenshireEvents.org.uk,
EdinburghGuide, FoodAndDrink Scotland and What's On Scotland. Created
using FME.

