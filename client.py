import requests

# response = requests.post('http://127.0.0.1:5000/notif', json={"title": 'Notification_3',
#                                                               "description": 'Описание_2',
#                                                               "owner": 'Punisher'
#                                                               })
# print(response.status_code)
# print(response.text)

response = requests.get('http://127.0.0.1:5000/notif/1')
print(response.status_code)
print(response.text)


# response = requests.delete("http://127.0.0.1:5000/notif/7")
# print(response.status_code)
# print(response.text)
#
