import requests


class LifeelCrm:
    adminId = 79
    def createLifeelNewuser(self,phone,**data):
        adminId = self.adminId
        whatsappNumber = phone
        fullName = data['username']
        email = f"{whatsappNumber}@tempmail.temp"
        displayName = fullName
        privateNote = "New User"

        payload = {"adminId":adminId,"whatsappNumber":whatsappNumber,"fullName":fullName,
                    "email":email,"displayName":displayName,"privateNote":privateNote
        }

        requests.post('http://localhost:4003/api/user/create',payload)

    def storeLifeelUsermessages(self,phone,**data):
        adminId = self.adminId
        whatsappNumber = phone
        print('whatsappNumberrrrrrrrrrrrr',whatsappNumber)
        fullName = data['username']
        message_content = data['userMsg']
        message_type = "Text"
        message_delivery = "Received"
        payload = {"adminId":adminId,"whatsapp_number":whatsappNumber,"fullName":fullName,
                    "message_content":message_content,"message_type":message_type,
                    "message_delivery":message_delivery
        }
        requests.post('http://localhost:4003/api/report/message-create',payload)