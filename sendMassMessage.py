from officialapi import LiveBot
sendmsg = LiveBot()
msg = "test"
message_status = []
def sendMassMessage(numbers):
    for number in numbers:
        message_ack = sendmsg.send_template_text_msg(number,"40aae5e0-3221-4cbe-abd0-50c4eaa711b5")
    return message_status