# -*- coding: utf-8 -*-

import json
def write_json():
    configs = {
            'ip': '192.168.43.100', 
            'port': 6666, 
            'plate_color': [40/225, 140/255, 200/255], 
            'plate_size': 20, 
            'debug': False, 
            'showing': True,
            'food_thre': 0.25,
            'background_thre': 0.2
                }
    with open("configs.json","w") as f:
        json.dump(configs, f)
    
write_json()

with open("configs.json",'r') as f:
    configs = json.load(f)
print(configs['ip'])