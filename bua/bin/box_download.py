# -*- coding: utf-8 -*-

from boxsdk import JWTAuth
from boxsdk import Client

# Configure JWT auth object
sdk = JWTAuth.from_settings_file(
        'C:/Users/user/Desktop/*********_******_config.json')

client = Client(sdk)

userid="*********"
user=client.user(user_id = userid)

###file name = photo.png, folder path = '0'
box_file = client.as_user(user).file(file_id='***********').get()
output_file = open(box_file.name, 'wb')
box_file.download_to(output_file)