import os
#from dotenv import load_dotenv
from flask.cli import load_dotenv
from twilio.rest import Client 



load_dotenv()

#my_request_client = MyRequestClass()

twilioSID = os.getenv("TWILIO_SID")
twilioTOKEN = os.getenv("TWILIO_TOKEN")
twilioNUMBER = os.getenv("TWILIO_NUMBER")

client = Client(twilioSID, twilioTOKEN)




