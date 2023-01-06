import json
import requests
import datetime


class LiveBot():
    APIUrl = 'http://api.gupshup.io/sm/api/v1/'
    source_no = "918591109247"
    src_name = "Beautex"
    # def __init__(self):
        
    #     # self.token = 'j19ksi1mim1lksm5007'
    #     # ?token={self.token}

    # 'apikey': 'adcc11aa6aec4c70ccd1aa19041b8267'
    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}"
        headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Apikey': 'faedad2160824b72cbf6b46b48cf8744'
        }
        answer = requests.post(url, data = data, headers=headers)
        print("req. ack:",answer.json())
        return answer.json()

    def send_message(self, destination, text):
        # text = text.encode()
        # text = str(text)[2:-1]
        data = {
                "channel" : "whatsapp",
                "destination" : destination,
                "source" : self.source_no,
                "message" : "test",
                "src.name" : self.src_name,
                "disablePreview":False
                } 
        answer = self.send_requests('msg', data)
        return answer

    def set_user_opt_in(self,userNumber):
        data = {
            "user":userNumber
        }
        self.send_requests(f'app/opt/in/{self.src_name}', data)

    def set_user_opt_out(self,userNumber):
        data = {
            "user":userNumber
        }
        return self.send_requests(f'app/opt/out/{self.src_name}', data)

    def send_template_text_msg(self, destination,template_msg_id):
        template_obj = '{"id": "template_msg_id","params": []}'.replace('template_msg_id',template_msg_id)
        data = {
                "destination" : destination,
                "source" : self.source_no,
                "template":f"{template_obj}"
            }
        answer = self.send_requests('template/msg', data)
        # messsage_status = {"number":destination,"msg":"Sent Successfully"}
        # if(answer['payload']['type'] == "failed"):
        #     code = answer['payload']['payload']['code']
        #     reason = answer['payload']['payload']['reason']
        #     if code == 1006 and "not opted in for template message" in reason:
        #         optIn_status = self.set_user_opt_in(destination)
        #         msg = "Sent" if optIn_status['payload']['type'] != "failed" else optIn_status['payload']['payload']['reason']
        #         messsage_status['msg'] = msg
        #     else:
        #         msg = answer['payload']['payload']['reason']
        #         messsage_status['msg'] = msg
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
    
