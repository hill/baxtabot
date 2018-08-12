import json
import requests
import datetime

from rivescript import RiveScript

from environment import *

import functions
import models

# ==== rivescript bot setup ==== #

bot = RiveScript()
bot.load_directory("./brain")
bot.sort_replies()

# ==== message handling ==== #

def handleMessage(sender_psid, received_message):
	print("HANDLING MESSAGE!")
	response = {}

	#humanisePSID(sender_psid)

	received_message = received_message.lower()

	if ("dinner" in received_message or "lunch" in received_message or "breakfast" in received_message):
		response = {"text": functions.dinoRequest(received_message)}
	elif ("date" in received_message):
		response = {"text": "The date is: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))}
	elif ("dino is shit" in received_message or "dino is good" in received_message or "dinovote" in received_message):
		response = functions.dinoVote()
	elif ("duty tutor" in received_message or "locked out" in received_message):
		response = {
			"attachment":{
				"type":"template",
				"payload":{
					"template_type":"button",
					"text":"Locked out again?! 🤦‍♂️",
					"buttons":[
						  {
						    "type":"phone_number",
						    "title":"Call the Duty Tutor",
						    "payload":"9385 9786"
						  }
					]
				}
			}
		}
	else:
		reply = bot.reply(str(sender_psid), received_message)
		response = {"text": "{}".format(reply)}

	print("Sending back: ")
	print(response)

	callSendAPI(sender_psid, response)

	return 'OK'

def handlePostback(sender_psid, received_postback):

	print('RECEIVED POSTBACK: ', received_postback)
	response = {"text": "Worked!"}

	callSendAPI(sender_psid, response)

def callSendAPI(sender_psid, response):

	r = requests.post(
		"https://graph.facebook.com/v2.6/me/messages",
		params = { "access_token": PAGE_ACCESS_TOKEN },
		json = {
			#"messaging_type": "RESPONSE", # alternatively MESSAGE_TAG
			"recipient": {
				"id": sender_psid
			},
			"message": response
		}
	)

	if (r.status_code == 200):
		print("sent message to meatbag!")
		return "Sent message to meatbag!"
	else:
		print("It's all gone to shit!")
		return "It's all gone to shit", r.status_code

# ====== User functionality ===== #

def humanisePSID(PSID):
	url = "https://graph.facebook.com/" + PSID

	r = requests.get(
		url,
		params = {
			"fields" : "first_name,last_name,profile_pic",
			"access_token" : PAGE_ACCESS_TOKEN
		}
	)

	if r.status_code == 200:
		data = json.loads(r.json())
		print("Name: {} {}\nPicture: {}".format(data['first_name'], data['last_name'], data['profile_pic']))