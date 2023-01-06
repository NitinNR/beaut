import redis
import os
from google.cloud import dialogflow as df
from datetime import datetime
import pytz
from func import functions
# import pycountry
import pytz
from wabot import WABot
import requests
import redis

# Google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from lifeelCrm import LifeelCrm as lfc

bot = functions()
send = WABot()

####### Redis Credentials

# r = redis.Redis(host='redis-19410.c93.us-east-1-3.ec2.cloud.redislabs.com', port=19410,password='UEGVlcMlyFqHu6ISqtQEqbvVnrsa65Vv')
# #r = redis.Redis(host='localhost', port=6379, db='')
# r.set('check', 'REdis working')
# print(r.get('check'))

#########################


# -------- gspread ---------

# scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
scope = ['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("apiKey.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Beautex WhatsApp Bot")

# -----------------------------


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apiKey.json"
CLIENT_ACCESS_TOKEN = 'f3b2b76ec414246af75fb85098dfd3b67a7a32d5'
df_session_client = df.SessionsClient()
PROJECT_ID = "beautex-cqwu"
my_date = datetime.now(pytz.timezone('Asia/Kolkata'))

date = my_date.date()
time = str(my_date).split('.')[0]
rw_lst = []

class dialog_op(lfc):

  def fetch_reply(self,query, session_id,**userinfo):
    # self.storeLifeelUsermessages(session_id,username=userinfo['username'],userMsg=query)
    return  self.dialogflow_operation(query, session_id,userinfo['username'])


  def detect_intent2(self,query,session_id):
    session = df_session_client.session_path(PROJECT_ID, session_id)
    text_input = df.TextInput(text=query, language_code='en')
    query_input = df.QueryInput(text=text_input)
    response = df_session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response

  def dialogflow_operation(self,query, session_id,username):
    response = self.detect_intent2(query, session_id)
    rrp=response.query_result.parameters
    d_name=response.query_result.intent.display_name
    print("rrp",rrp,"\n\nIntents:",d_name)
    session_id=session_id
    number=session_id
    print(session_id)
    number=session_id
    intent=d_name
    parameter=rrp
    text = query

    if intent == "menu":
      status = bot.check_number_exist_in_db(number)
      print(status)
      # check user
      if not status:
        # Doesn't Exist
        # self.createLifeelNewuser(session_id,username=username)
        print("doesn't Exist")
        return self.register_dialogflow_operation('register', session_id)
      elif status:
        # Doesn't Exist
        print("User Exist")
        return self.menu_operation(text,number,intent,parameter)
    
    if "menu" in intent:
      return self.menu_operation(text,number,intent,parameter)

    if "register" in intent:
      return self.register_operation(text,number,intent,parameter) 
    if "location" in intent:
      return self.location_operation(text,number,intent,parameter)
    if "category" in intent:
      return self.category_operation(text,number,intent,parameter)
    if "brochure" in intent:
      return self.brochure_operation(text,number,intent,parameter)
    if "Warranty&Bill" in intent:
      return self.waranty_operation(text,number,intent,parameter)
    if "Dealership&Enquiry" in intent:
      return self.dealership_operation(text,number,intent,parameter)
    if "Complaints" in intent:
      return self.complaints_operation(text,number,intent,parameter)
    if "Others" in intent:
      return self.others_operation(text,number,intent,parameter)
      
      

  def register_dialogflow_operation(self,query, session_id):
    response = self.detect_intent2(query, session_id)
    rrp=response.query_result.parameters
    d_name=response.query_result.intent.display_name
    print("rrp",rrp,"\n\nIntents:",d_name)
    intent=d_name

    if intent == "register":
      #print("Registering")
      reply = bot.register_followup_1()
      return reply
    
  def location_dialogflow_operation(self,query, session_id):
    response = self.detect_intent2(query, session_id)
    rrp=response.query_result.parameters
    d_name=response.query_result.intent.display_name


  def category_dialogflow_operation(self,query, session_id):
    response = self.detect_intent2(query, session_id)
    rrp=response.query_result.parameters
    d_name=response.query_result.intent.display_name

  def brochure_dialogflow_operation(self,query, session_id):
    response = self.detect_intent2(query, session_id)
    rrp=response.query_result.parameters
    d_name=response.query_result.intent.display_name

    #---- Register

  def register_operation(self,text,number,intent,parameter):
    # if intent == "register":
    #   print("Registering")
    #   reply = bot.register_followup_1()
    #   return reply
    if intent == "register - name":
      name = parameter['name']
      print("Name :",name)
      bot.insert_name_in_db(number,name)
      reply = bot.register_followup_2()
      return reply
    elif intent == "register - name - mail":
      email = parameter['email']
      print("email :",email)
      bot.insert_email_in_db(number,email)
      reply = bot.main_menu()
      self.location_dialogflow_operation('menu', number)
      return reply


  def location_operation(self,text,number,intent,parameter):

    if intent == "location - loc":
      # city = parameter['city'].string_value
      # # state = parameter['state'].string_value
      # pincode = parameter['pincode'].string_value
      # print("Locations", city, "pincode",pincode)
      # # Fetch and send showroom location
      # reply = bot.fetch_showrooms(city,pincode)
      # return reply
      option_number = int(parameter['number'])
      print("option_number", option_number)
      # Fetch and send showrooms
      reply = bot.fetch_selected_showrooms(option_number)
      return reply
    
  def category_operation(self,text,number,intent,parameter):
    if intent == "category - op1":
      intent = "category - op1 - temp"
    b_elem = 3
    n_elem = len(intent.split("-"))
    diff_elem = int(n_elem) - b_elem
    b_row = 7
    b_col = 13
    b_val1 = 8
    b_val2 = 9
    n_col = b_col + 2*(diff_elem)
    n_val1 = b_val1 + 2*(diff_elem)
    n_val2 = n_val1 + 1
    print("n_val1",n_val1,"n_val2",n_val2)
    if intent == "category - requirement":
      
      option_number = text #int(parameter['number'].number_value)
      reply = bot.comm_pro_search(7,9)
      bot.prod_comm(number,option_number,n_val1)
      bot.prod_comm(number,reply,n_val2)
      return reply

    elif intent == "category - op1 - temp":
      
      option_number = text #int(parameter['number'].number_value)
      reply = bot.comm_pro_search(7,11)
      bot.prod_comm(number,option_number,n_val1)
      bot.prod_comm(number,reply,n_val2)
      return reply

    elif "DW" in intent:
      
      rw_lst.append(7)
      option_number = text #int(parameter['number'].number_value)
      print("b_elem",b_elem,"n_col",n_col,"n_val1",n_val1)
      reply = bot.comm_pro_search(b_row,n_col)
      bot.prod_comm(number,option_number,n_val1)
      bot.prod_comm(number,reply,n_val2)
      return reply
    
    elif "FlyMesh" in intent:
      
      rw_lst.append(8)
      b_row = b_row + 1
      option_number = text #int(parameter['number'].number_value)
      print("b_elem",b_elem,"n_col",n_col,"n_val1",n_val1)
      reply = bot.comm_pro_search(b_row,n_col)
      bot.prod_comm(number,option_number,n_val1)
      bot.prod_comm(number,reply,n_val2)
      return reply
      
    elif "facades" in intent:
      
      rw_lst.append(9)
      b_row = b_row + 2
      option_number = text #int(parameter['number'].number_value)
      print("b_elem",b_elem,"n_col",n_col,"n_val1",n_val1)
      reply = bot.comm_pro_search(b_row,n_col)
      bot.prod_comm(number,option_number,n_val1)
      bot.prod_comm(number,reply,n_val2)
      return reply

    elif "railings" in intent:
      
      rw_lst.append(10)
      b_row = b_row + 3
      option_number = text #int(parameter['number'].number_value)
      print("b_elem",b_elem,"n_col",n_col,"n_val1",n_val1)
      reply = bot.comm_pro_search(b_row,n_col)
      bot.prod_comm(number,option_number,n_val1)
      bot.prod_comm(number,reply,n_val2)
      return reply
    elif "Glass&Aluwood" in intent:
      
      rw_lst.append(11)
      b_row = b_row + 4
      option_number = text #int(parameter['number'].number_value)
      print("b_elem",b_elem,"n_col",n_col,"n_val1",n_val1)
      reply = bot.comm_pro_search(b_row,n_col)
      bot.prod_comm(number,option_number,n_val1)
      bot.prod_comm(number,reply,n_val2)
      return reply
    
    elif "category - city - city_loc" in intent:
      print("rw_lst",rw_lst)
      b_row = rw_lst[0]
      n_col = 23
      n_val2 = 4
      user_city = (parameter['city'])
      print("b_elem",b_elem,"n_col",n_col,"n_val1",n_val1)
      reply = bot.comm_pro_search(b_row,n_col)
      # bot.prod_comm(number,user_city,n_val1)
      bot.prod_comm(number,user_city,n_val2)
      rw_lst.clear()
      return reply

    
    # # Prod
    # if intent == "category - op1- DW":
    #   option_number = int(parameter['number'].number_value)
    #   print("number",option_number)
    #   reply = bot.comm_pro_search(7,11)
    #   bot.prod_comm(number,option_number,7)
    #   bot.prod_comm(number,reply,8)
    #   return reply
    
    # if intent == "category - op1- DW - feature":
    #   option_number = int(parameter['number'].number_value)
    #   print("number",option_number)
    #   reply = bot.comm_pro_search(7,13)
    #   bot.prod_comm(number,option_number,9)
    #   bot.prod_comm(number,reply,10)
    #   return reply

    # if intent == "category - op1- DW - feature - prod":
    #   option_number = int(parameter['number'].number_value)
    #   print("number",option_number)
    #   reply = bot.comm_pro_search(7,15)
    #   bot.prod_comm(number,option_number,11)
    #   bot.prod_comm(number,reply,12)
    #   return reply
    
    # if intent == "category - op1- DW - feature - prod - qn":
    #   option_number = int(parameter['number'].number_value)
    #   print("number",option_number)
    #   reply = bot.comm_pro_search(7,17)
    #   bot.prod_comm(number,option_number,13)
    #   bot.prod_comm(number,reply,14)
    #   return reply
    
    # if intent == "  category - op1- DW - feature - prod - qn - looking":
    #   option_number = int(parameter['number'].number_value)
    #   print("number",option_number)
    #   reply = bot.comm_pro_search(7,19)
    #   bot.prod_comm(number,option_number,14)
    #   bot.prod_comm(number,reply,15)
    #   return reply

    # ************ 2nd Fascases ************
    
    # if intent == "  category - op1- DW - feature - prod - qn - looking
    # ":
    #   option_number = int(parameter['number'].number_value)
    #   print("number",option_number)
    #   reply = bot.comm_pro_search(7,19)
    #   bot.prod_comm(number,option_number,14)
    #   bot.prod_comm(number,reply,15)
    #   return reply

  # ---------------------------

  def brochure_operation(self,text,number,intent,parameter):

    if intent == "brochure - options":
      option_number = int(parameter['number'])
      print("option_number", option_number)
      # Fetch and send brochure's
      reply = bot.fetch_brochures(option_number)
      return reply


  # ------------ Warranty ---------------

  def waranty_operation(self,text,number,intent,parameter):
    if intent == "Warranty&Bill - info":
      info = (parameter['info'])
      print("info", info)
      reply = bot.warranty_info(number,info)
      return reply

  # ------------ END Warranty ---------------

  # ------------ Dealership & Enquiry ---------------

  def dealership_operation(self,text,number,intent,parameter):
    if intent == "Dealership&Enquiry - info":
      info = (parameter['info'])
      print("info", info)
      reply = bot.dealership_info(number,info)
      return reply

  # ------------ END Dealership & Enquiry ---------------

  # ------------ Complaints  ---------------

  def complaints_operation(self,text,number,intent,parameter):
    if intent == "Complaints - info":
      info = (parameter['info'])
      print("info", info)
      reply = bot.complaints_info(number,info)
      return reply

  # ------------ END Complaints  ---------------

  # ------------ Others  ---------------

  def others_operation(self,text,number,intent,parameter):
    if intent == "Others - info":
      info = (parameter['info'])
      print("info", info)
      reply = bot.others_info(number,info)
      return reply

  # ------------ END Others  ---------------


  #------------------------ Menu ---------------------------

  def menu_operation(self,text,number,intent,parameter):
    if intent == "menu":
      reply = bot.main_menu()
      return reply
    elif intent == "menu - options":
      option_number = int(parameter['number'])
      print("number",option_number)
      return self.option_menu(option_number,number)
    
  def option_menu(self,option,number):
    wrk = sheet.worksheet('Main Menu logic')
    val = wrk.col_values(4)
    val = val[5:]
    print(val)
    base_val=[5,6]
    for value in val:
      if option == int(value):
        
        reply_val = int(5) + (option)
        print("option",option,"value",value,"reply_val",reply_val)
        reply = wrk.cell(reply_val,7).value
        if reply_val == 6:
          # show showrooms
          self.location_dialogflow_operation("location", number)
        elif reply_val == 7:
          # products explore
          bot.prod_op1_qns(number,reply)
          self.location_dialogflow_operation("category", number)
        elif reply_val == 8:
          # show brochure
          self.brochure_dialogflow_operation("brochure", number)
        # if reply_val == 9:
        #   # warrany and bill
        #   self.location_dialogflow_operation("warranty", number)
        # if reply_val == 10:
        #   # Dealership and Inquiry
        #   self.location_dialogflow_operation("Dealership", number)
        elif reply_val == 9:
          # complaints
          self.location_dialogflow_operation("Complaints", number)
        elif reply_val == 10: 
          # Others 
          self.location_dialogflow_operation("others", number)
          
        return reply
