import configparser

config = configparser.ConfigParser()
config.read('config.ini')
YA_KEY = config['DEFAULT']['YA_KEY']
SPEECH_UUID = config['DEFAULT']['SPEECH_UUID']
