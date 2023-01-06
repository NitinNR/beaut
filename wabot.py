import json
import requests
import datetime


class WABot():    
    def __init__(self):
        self.APIUrl = 'http://167.99.13.244:5007/5007/'
        self.token = 'j19ksi1mim1lksm5007'

   
    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        print(answer.text)
        return answer

    def send_message(self, chatID, text):
        # text = text.encode()
        # text = str(text)[2:-1]
        data = {"phone" : chatID,
                "body" : str(text)}  
        answer = self.send_requests('sendMessage', data)
        return answer
    
    def image(self,chatID,img_path,img_name,caption):
      # caption = caption.encode()
      # caption = str(caption)[2:-1]
      data = {
        "phone": chatID,
        "body":img_path,
        "filename": img_name,
        "caption": caption
      }
      return self.send_requests('sendFile', data)

    def time(self, chatID):
        t = datetime.datetime.now()
        time = t.strftime('%d:%m:%Y')
        return self.send_message(chatID, time)

    def show_chat_id(self,chatID):
        return self.send_message(chatID, f"Chat ID : {chatID}")

    def me(self, chatID, name):
        return self.send_message(chatID, name)

    def file(self, chatID,filename,path,caption):
        caption = caption.encode()
        caption = str(caption)[2:-1]
        data = {
                    'phone' : chatID,
                    'body': path,                      
                    'filename' : filename,
                    'caption' : (caption),
                }
        return self.send_requests('sendFile', data)
    
    def audio(self, chatID,audio_url):        
            data = {
            "audio" : audio_url,
            "phone" : chatID }
            return self.send_requests('sendAudio', data)

    def geo(self, chatID,lat,lng):
        
        data = {
                "lat" : lat,
                "lng" : lng,
                "phone" : chatID,
                "address":''
        }
        answer = self.send_requests('sendLocation', data)
        return answer
    
    def group(self, author):
        phone = author.replace('@c.us', '')
        data = {
            "groupName" : 'Group with the bot Python',
                        "phones" : phone,
                        'messageText' : 'It is your group. Enjoy'
        }
        answer = self.send_requests('group', data)
        return answer
    
