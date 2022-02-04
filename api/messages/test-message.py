from twilio.rest import Client


account_sid = 'AC3f8d76c8146769f6f9626a866cf13d11'
auth_token = 'f892e358c4fa0bf19a750309803d39ba'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='All in the game, yo',
                              from_='+17754036939',
                              to='+918825464712'
                          )

print(message.sid)