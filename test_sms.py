


i = 1
a = [1, 2, 3, 4]
b = [5, 6, 7, 8]
while i > 0:
    print('dddd')
    for aa, bb in zip(a[:], b[:]):
        if aa == 2:
            a.remove(aa)
            continue
        print(aa)




# from twilio.rest import Client

# def send_sms(txt_writing):
#     account_sid = 'ACfd0d66ac60f90069be9bcd0df5430922'
#     auth_token = '775c7f6a69678406892e660ae7294f5f'
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         to="+821020667742",
#         from_="+13305221240",
#         body=txt_writing)
#     print(message.sid)


# txt_writing = 'Job is done'
# send_sms(txt_writing)