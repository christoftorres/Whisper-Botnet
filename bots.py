#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading

from web3 import HTTPProvider, Web3
from web3.shh import Shh

class Bot(threading.Thread):
    def __init__(self, name):
        super(Bot, self).__init__()
        self.name = name
        self.shh = Shh(Web3(HTTPProvider('http://localhost:8545')))
        print(self.name+': Whisper version: '+self.shh.version)
        print(self.name+': Whisper info: [memory: '+str(self.shh.info.memory)+', messages: '+str(self.shh.info.messages)+', max_message_size: '+str(self.shh.info.maxMessageSize)+', min_pow: '+str(self.shh.info.minPow))
        self.symKeyID = self.shh.generateSymKeyFromPassword('shh!! this is a secret password')
        print(self.name+': Identity: '+self.symKeyID)
        print(self.name+': Symmetric key: '+self.shh.getSymKey(self.symKeyID))

    def filter(self):
        message_filter = self.shh.newMessageFilter({'topic': '0x12340000', 'symKeyID': self.symKeyID})
        return message_filter

    def run(self):
        filter_id = self.filter().filter_id
        print(self.name+': Waiting for messages...')
        while True:
            messages = self.shh.getMessages(filter_id)
            for message in messages:
                print(self.name+': Received message: '+Web3.toText(message['payload']))
                print(self.name+': Envelope: '+str(message))
            time.sleep(0.3)

bots = []
for i in range(4):
    bot = Bot('Bot-'+str(i+1))
    bots.append(bot)
    bot.start()
