from cryptography.fernet import Fernet
import json
import os
key=Fernet.generate_key()
input_file="./singleuser/config/config.json"
if not os.path.exists(input_file):
    print('Database config.json file not exist')
    print('Please provide using singleuser/config/config_template.json')
output_file="./singleuser/config/config_encrypted.json"
with open(input_file, "rb") as fr:
    data=json.load(fr)
fernet=Fernet(key)
encrypted=fernet.encrypt(json.dumps(data))
with open(output_file, "wb") as fw:
    fw.write(encrypted)
with open("./singleuser/config/config.key", "wb") as fw:
    fw.write(key)
