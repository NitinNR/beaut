from flask import Flask, request,make_response,jsonify,session,render_template
from operation import dialog_op

# from time import sleep
# from twilio.twiml.messaging_response import MessagingResponse
import requests
import urllib.parse
from officialapi import LiveBot
# from operation import Bot
import json
from func import functions
from sendMassMessage import sendMassMessage

bot=functions()
app = Flask(__name__)
SECRET_KEY = 'Ketan'
send = LiveBot()
dg = dialog_op()

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET','POST'])
def verify():
  # print('sheet',bot.register_followup_1())
  return "Server is Working !\n", 200

@app.route('/sendMsg',methods = ['POST'])
def sendMsg():
  data = request.form.get('numbers')
  numbers = list(filter(None, data.split(",")))
  sendMassMessage(numbers)
  return "ok"

@app.route('/test',methods = ['GET','POST'])
def test():
  # print(data)
  message = request.form.get('message')
  number = request.form.get('number')
  print("\nMessage:",message," | Number:",number,"\n")
  reply = dg.fetch_reply(message, number,username=number)
  print("Reply:\n",reply)
  if reply is None:
    return "None"
  return "reply: \n\n"+str(reply)
  return 'a beautex'


@app.route('/official',methods = ['GET','POST'])
def official():
  try:
    data = request.json
    # print("Response:",data)
    reply = "*Try again later !*"
    if data['type']=='message':
      message = (data['payload']['payload']['text'])
      number = data['payload']['source']
      name = data['payload']['sender']['name']
      print("\nMEssage:",message," | Number:",number,"\n")
      reply = dg.fetch_reply(message, number,username=name)
      print("Reply:\n",reply)
      return reply if reply else ''
    elif(data['payload']['type'] == "failed"):
        # print("Response:",data)
        print("Failed@@@@@@@@@@@@@@@")
        destination = data['payload']['destination']
        code = data['payload']['payload']['code']
        reason = data['payload']['payload']['reason']
        if code == 1006 and "not opted in for template message" in reason:
            send.set_user_opt_in(destination)
        elif "not opted" in reason:
            send.set_user_opt_in(destination)
        else:
          print("Not sent")

        return ''


    return reply,200
  except Exception as e:
    print("Exception: %s" % e)
    return ''

@app.route('/wapi',methods=['GET','POST'])
def wapi():
  raw_data = (request.get_json())
  # print("raw_data",raw_data)
  #reply = "*Try agin later !*"
  if 'messages' in raw_data:
    data = raw_data['messages'][0]
    if not data['fromMe']:
      print("Data :",data)
      message = data['body']
      if 'chatId' in data:
        number = data['chatId'].split('@')[0]
        msg_type = data['type']
        if msg_type=="chat" and len(number) < 20:
          print("\nMEssage:",message," | Number:",number,"\n")
          reply = dg.fetch_reply(message, number)
          print("Reply:\n",reply)
          # bot.insert_user_query_in_db(number,message,reply)
          if reply is not None:
            send.send_message(number,reply)
          
        if msg_type=="location":
          lat = data['lat']
          lng = data['lng']
          print("Latitude:",lat,"Longitude:",lng,'number:',number)
          msg = 'location '+str(str(lat)+' and '+str(lng))

          reply = dg.fetch_reply(msg, number)
          send.send_message(number,reply)
          # lat = cordinates.split(';')[0]
          # lng = cordinates.split(';')[1]
          # print(send.geo(number,lat,lng))
    
  return 'cool',200


def run():
  if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=4007)


run() 
