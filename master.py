#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web3 import HTTPProvider, Web3
from web3.shh import Shh

def main():
    w3 = Web3(HTTPProvider('http://localhost:8545'))
    print(w3.admin.peers)
    print('Peers:')
    for peer in w3.admin.peers:
        print(' -> '+peer['network']['remoteAddress']+' '+peer['name']+' '+str(peer['caps']))

    shh = Shh(w3)
    print('Whisper version: '+shh.version)
    print('Whisper info: [memory: '+str(shh.info.memory)+', messages: '+str(shh.info.messages)+', max_message_size: '+str(shh.info.maxMessageSize)+', min_pow: '+str(shh.info.minPow))

    symKeyID = shh.generateSymKeyFromPassword('shh!! this is a secret password')
    print('Identity: '+symKeyID)
    print('Symmetric key: '+shh.getSymKey(symKeyID))

    result = shh.post({'payload': Web3.toHex(text='Hello world!'), 'symKeyID': symKeyID, 'topic': '0x12340000', 'powTarget': 2.5, 'powTime': 2})
    print('Message sent: '+str(result))

if __name__ == '__main__':
    main()
