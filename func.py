# import datefinder
from datetime import datetime,timedelta,date
import pytz
import pymysql as db
import requests
import urllib.parse
# import xlwt
import pandas.io.sql as sql
import pandas as pd
# Google sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from google.oauth2 import service_account
######

#E-Mail
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
##########


# Hostinger
# USER =  'u362881663_beautex'
# DB = 'u362881663_beautex' 
# PASSWORD = 'v7SLOataSA^'
# HOST = 'sql337.main-hosting.eu'
# PORT = 3306

# intechDc
USER =  'lifeelbo_lifeel'
DB = 'lifeelbo_beautex' 
PASSWORD = '2N2y]ZW?l@.#'
HOST = 'wh001.in.intechdc.com'
PORT = 3306




my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
date_time = my_date.strftime("%m/%d/%Y T %H:%M:%S")
print('mydate',date_time)
# date = my_date.strftime("%d/%m/%Y")
# time = my_date.strftime("%H:%M")
# print("date",date," and time:",time)




# -------- gspread ---------

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("apiKey.json", scope)
# creds = service_account.Credentials.from_service_account_file(
#         "beautex-bot.json", scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("Beautex WhatsApp Bot")

# -----------------------------

# USER =  'u362881663_restaurant'
# DB = 'u362881663_restaurant' 
# PASSWORD = '|T3gDRi+Ze'
# HOST = 'sql337.main-hosting.eu'
# PORT = 3306
# conn = db.Connection(host=HOST, port=PORT, user=USER,passwd=PASSWORD, db=DB)
# cur=conn.cursor()
# print(cur)

class functions:
  def check_number_exist_in_db(self,number):
    conn = db.Connection(host=HOST, port=PORT, user=USER,passwd=PASSWORD, db=DB)
    cur=conn.cursor()
    print("THIS IS number",number)
    sql="SELECT * FROM `users` WHERE `whatsapp_number` = %s"
    cur.execute(sql,(str(number)))
    users=cur.fetchone()
    print(users)
    conn.close()
    if users is None:
      #doesnt not exist
      return False
    if users is not None:
      #when Exist
      return True
    
  def insert_name_in_db(self,number,name):
    status = self.check_number_exist_in_db(number)
    conn = db.Connection(host=HOST, port=PORT, user=USER,passwd=PASSWORD, db=DB)
    cur=conn.cursor()
    my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    date_time = my_date.strftime("%m/%d/%YT%H:%M:%S")
    if status is False:
      sql="INSERT INTO `users`(`whatsapp_number`, `name`, `DateTime`) VALUES (%s,%s,%s)"
      cur.execute(sql,(number,name,date_time))
      conn.commit()
    conn.close()
  
  def insert_email_in_db(self,number,email):
    conn = db.Connection(host=HOST, port=PORT, user=USER,passwd=PASSWORD, db=DB)
    cur=conn.cursor()
    sql = "UPDATE `users` SET `email`=%s WHERE `whatsapp_number`=%s"
    cur.execute(sql,(email,number))
    conn.commit()
    conn.close()
    wrk = sheet.worksheet('user info')
    name = self.get_name_user(number)
    email = self.get_email_user(number)
    DateTime = self.get_datetime_user(number)
    wrk.append_row([str(number),name,email,str(DateTime)])
  
  def get_name_user(self,number):
    conn = db.Connection(host=HOST, port=PORT, user=USER,passwd=PASSWORD, db=DB)
    cur=conn.cursor()
    sql="SELECT `name` FROM `users` WHERE `whatsapp_number` = %s"
    cur.execute(sql,(str(number)))
    user=cur.fetchone()
    print(user[0])
    conn.close()
    return user[0]
    
  
  def get_email_user(self,number):
    conn = db.Connection(host=HOST, port=PORT, user=USER,passwd=PASSWORD, db=DB)
    cur=conn.cursor()
    sql="SELECT `email` FROM `users` WHERE `whatsapp_number` = %s"
    cur.execute(sql,(str(number)))
    user=cur.fetchone()
    print(user[0])
    conn.close()
    return user[0]
    
  def get_datetime_user(self,number):
    conn = db.Connection(host=HOST, port=PORT, user=USER,passwd=PASSWORD, db=DB)
    cur=conn.cursor()
    sql="SELECT `DateTime` FROM `users` WHERE `whatsapp_number` = %s"
    cur.execute(sql,(str(number)))
    user=cur.fetchone()
    print(user[0])
    conn.close()
    return user[0]

  def register_followup_1(self):
      wrk = sheet.worksheet('Main Menu logic')
      val = wrk.cell(21,1).value
      print("Followup - 1",val)
      return str(val)
    
  def register_followup_2(self):
      wrk = sheet.worksheet('Main Menu logic')
      val = wrk.cell(21,2).value
      print("Followup - 2",val)
      return str(val)
      
  def register_followup_3(self):
      wrk = sheet.worksheet('Main Menu logic')
      val = wrk.cell(21,2).value
      print("Followup - 2",val)
      return str(val)
  

  # ---------- Menu -----

  def main_menu(self):
    wrk = sheet.worksheet('main-menu')
    val = wrk.col_values(2)
    
    val = val[1:]
    reply= "*Main-menu* 〽️\n\n"
    for  value in val:
      reply = reply + value
      reply = reply + "\n"
    print("Followup - 2",reply)
    wrk = sheet.worksheet('Main Menu logic')
    val = wrk.cell(6,3).value
    print("offer from sheet",val)
    try:
      if len(val):
        offers = "\n-------------\n   offers\n-------------\n"+str(val)+"\n"
      else:
        offers = " "
    except:
      offers = ""
    header = wrk.cell(6,1).value+"\n"  
    footer = "\n\n"+wrk.cell(6,2).value+"\n"  
    main_menu = header+reply+offers+footer
    return str(main_menu)

  def option_menu(self,option,number):
    wrk = sheet.worksheet('Main Menu logic')
    val = wrk.col_values(4)
    val = val[5:]
    print(val)
    base_val=[5,6]
    for value in val:
      if option == int(value):
        print("option",option,"value",value)
        reply_val = int(5) + (option)
        reply = wrk.cell(reply_val,7).value

        return reply

  def sub_menu1(self,option):
    wrk = sheet.worksheet('Main Menu logic')
    sub_option = 9
    val = wrk.col_values(sub_option)
    val = val[5:]
    print(val)
    base_val=[5,6]
    for value in val:
      if option == int(value):
        print("option",option,"value",value)
        reply_val = int(sub_option) + (option)
        reply = wrk.cell(reply_val,7).value
        return reply
        
  def fetch_showrooms(self,city,pincode):
    main_wrk = sheet.worksheet('showrooms')
    fall_back = main_wrk.cell(26,1).value
    wrk = sheet.worksheet('showrooms')
    val = wrk.col_values(1)
    val = val[5:]
    print(val)
    for valuee in val:
      sh_city = valuee.split(',')[0]
      sh_pincode = valuee.split(',')[1]
      print("sh_city",sh_city,"sh_pincode",sh_pincode)
      if int(sh_pincode)== int(pincode):
          print("inside showing fetching")
          row = int(val.index(valuee))+6
          print("row",row)
          reply = wrk.cell(row,2).value
          return reply
      else:
        return "No Showrooms Found\n\n"+fall_back

  def fetch_selected_showrooms(self,option_number):
    wrk = sheet.worksheet('showrooms')
    col = wrk.col_values(1)
    col = col[1:]
    print(col)
    for valuee in col:
      print("fetching showrooms")
      row = int(col.index(str(option_number)))+2
      print("row",row)
      reply = wrk.cell(row,2).value
      return reply

  def fetch_brochures(self,option_number):
    wrk = sheet.worksheet('brochure')
    col = wrk.col_values(1)
    col = col[1:]
    print(col)
    for valuee in col:
      print("fetching brochure")
      row = int(col.index(str(option_number)))+2
      print("row",row)
      reply = wrk.cell(row,3).value
      return reply
  
  # ---------- Products replies ----------

  def comm_pro_search(self,row,col):
    # sh_options = [1,2]
    # if int(option) in sh_options:
    wrk = sheet.worksheet('Main Menu logic')
    val = wrk.cell(row,col).value
    print("Category Pro Followup - 1",val)
    return str(val)

  def comm_pro_city(self,number,city,col):
    prod_wrk = sheet.worksheet('Product Lead')
    number_cel = prod_wrk.findall(number)
    print("number_cel",number_cel[-1])
    number_cel = number_cel[-1]
    if len(str(number_cel)):
      user_row = number_cel.row
      print("user_row",user_row)
      prod_wrk.update_cell(user_row,col,city)
  
  # ------------------------------


  # ------------------------------ Products ------------------------------

  def prod_op1_qns(self,number,qns):
    name = self.get_name_user(number)
    email = self.get_email_user(number)
    prod_wrk = sheet.worksheet('Product Lead')
    prod_wrk.append_row([str(number),name,email,'',qns])
  
  def prod_comm(self,number,qns_ans,col):
    prod_wrk = sheet.worksheet('Product Lead')
    number_cel = prod_wrk.findall(number)
    print("number_cel",number_cel[-1])
    number_cel = number_cel[-1]
    if len(str(number_cel)):
      user_row = number_cel.row
      print("user_row",user_row)
      prod_wrk.update_cell(user_row,col,qns_ans)
  
  # ------------------------------ END Products ------------------------------



  # ------------------------------ Warranty ------------------------------

  def warranty_info(self,number,info):
    warranty_wrk = sheet.worksheet('Warranty & Bill')
    wrk = sheet.worksheet('Main Menu logic')
    name = self.get_name_user(number)
    email = self.get_email_user(number)
    warranty_wrk.append_row([str(number),name,email,info])
    val = wrk.cell(9,9).value
    print("warranty and Bill Followup - 5",val)
    return str(val)

  # ------------------------------ END Warranty ------------------------------

  # ------------------------------ Dealership & Enquiry ------------------------------

  def dealership_info(self,number,info):
    dealership_wrk = sheet.worksheet('Dealership & Enquiry')
    wrk = sheet.worksheet('Main Menu logic')
    name = self.get_name_user(number)
    email = self.get_email_user(number)
    dealership_wrk.append_row([str(number),name,email,info])
    val = wrk.cell(10,9).value
    print("dealership_wrk and Bill Followup - 5",val)
    return str(val)

  # ------------------------------ END Dealership & Enquiry ------------------------------


  # ------------------------------ Complaints ------------------------------

  def complaints_info(self,number,info):
    my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    date_time = my_date.strftime("%m/%d/%Y, %H:%M:%S")
    # date = my_date.strftime("%d/%m/%Y")
    # time = my_date.strftime("%H:%M")
    # print("date",date," and time:",time)
    complaints_wrk = sheet.worksheet('Complaints')
    wrk = sheet.worksheet('Main Menu logic')
    name = self.get_name_user(number)
    email = self.get_email_user(number)
    complaints_wrk.append_row([str(number),name,email,info,str(date_time)])
    val = wrk.cell(9,9).value
    print("Complaints_wrk Followup - 5",val)
    return str(val)

  # ------------------------------ END Complaints ------------------------------

  # ------------------------------ Others ------------------------------

  def others_info(self,number,info):
    my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    date_time = my_date.strftime("%m/%d/%Y, %H:%M:%S")
    others_wrk = sheet.worksheet('Others')
    wrk = sheet.worksheet('Main Menu logic')
    name = self.get_name_user(number)
    email = self.get_email_user(number)
    others_wrk.append_row([str(number),name,email,info,str(date_time)])
    val = wrk.cell(10,9).value
    print("others_wrk  Followup - 5",val)
    return str(val)

  # ------------------------------ END Others ------------------------------




  def insert_user_in_db(self,number):
    conn = db.Connection(host=HOST, port=PORT, user=USER,       passwd=PASSWORD, db=DB)
    cur=conn.cursor()
    sql="INSERT INTO `healthcare`(`From Number`,`status`) VALUES (%s,%s)"
    cur.execute(sql,(str(number),1))
    conn.commit()
    conn.close()
  
  def insert_user_query_in_db(self,number,user_query,bot_reply):
    my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    To_number = '918451058451'
    #date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date = my_date.strftime("%d/%m/%Y")
    time = my_date.strftime("%H:%M")
    print("date",date," and time:",time)
    conn = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
    cur=conn.cursor()
    sql="INSERT INTO `healthcare`( `From Number`,`To Number`, `Text`, `Date`,`Time`,`status`) VALUES (%s,%s,%s,%s,%s,%s)"
    cur.execute(sql,(number,To_number,user_query,str(date),str(time),1))
    conn.commit()
    conn.close()

#------------------------------------------------------


  def send_mail(self,fromaddr,toaddr,filename,path_of_file,subject,body):
    msg = MIMEMultipart() 
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(path_of_file, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "qwupdxeflwrkldmw")
    text = msg.as_string()
    print(s.sendmail(fromaddr, toaddr, text) )
    s.quit() 



#------------------------- Exporting -----------------------------


  def export_to_excel(self):
    conn = db.Connection(host=HOST, port=PORT, user=USER,       passwd=PASSWORD, db=DB)
    # cur=conn.cursor()
    my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    #date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date = my_date.strftime("%d/%m/%Y")
    time = my_date.strftime("%H:%M")
    print("date",date," and time:",time)
    # sqll = "SELECT * FROM `healthcare` WHERE `Date`=%s"
    # cur.execute(sqll,(str(date)))
    # users = cur.fetchall()
    # df=sql.read_sql(users,conn)
    
    df=sql.read_sql("SELECT  `From Number`, `To Number`, `Text`, `Date`, `Time` FROM `healthcare` WHERE `Date`='"+str(date)+"'",conn)
    print(df)
    # export the data into the excel sheet
    df.to_excel('daily_report.xls')
    # self.rename_file('daily_report.xls')
    
    fromaddr = "ravi.salvi935@gmail.com"
    toaddr_testing1 = "ketan.salvi21@gmail.com"
    filename = 'daily_report.xls'
    # filename = "messages-"+str(date)+".xls"
    path_of_file = filename
    subject = "Message Dump for the day "+str(date)
    body = "Report Dated : "+str(date)
    self.send_mail(fromaddr,toaddr_testing1,filename,path_of_file,subject,body)
    conn.close()


  def send_email_on_trigger(self,user_message,bot_reply,user_number):
    # cur=conn.cursor()
    my_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    #date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date = my_date.strftime("%d/%m/%Y")
    time = my_date.strftime("%H:%M")
    print("date",date," and time:",time)
    # sqll = "SELECT * FROM `healthcare` WHERE `Date`=%s"
    # cur.execute(sqll,(str(date)))
    # users = cur.fetchall()
    # df=sql.read_sql(users,conn)
    # df=sql.read_sql("SELECT * FROM `healthcare` WHERE `Date`='"+str(date)+"'",conn)
    # print(df)
    # # export the data into the excel sheet
    # df.to_excel('daily_report.xls')
    fromaddr = "ravi.salvi935@gmail.com"
    toaddr_testing1 = "ketan.salvi21@gmail.com"
    # subject = "Daily Report of "+str(date)
    body = "Adverse Effect Message Triggered"+"\n\n\nUser Message: "+str(user_message)+"User Number: "+str(user_number)+"\n\nBot Reply: "+str(bot_reply)+"\n\nDate: "+str(date)+" Time: "+str(time)
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    # s.login("ravi.salvi935@gmail.com", "qwupdxeflwrkldmw") 
    s.login(fromaddr, "qwupdxeflwrkldmw")
    message = body
    # s.sendmail(fromaddr, toaddr_testing, message)
    s.sendmail(fromaddr, toaddr_testing1, message)
    s.quit()  

  
#------------------------- END Exporting -----------------------------


bot=functions()
