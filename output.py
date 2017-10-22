# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:18:57 2016

@author: Cyrille
"""

import math
from Crypto.Cipher import AES

ctlst = [('140b41b22a29beb4061bda66b6747e14','4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'),('140b41b22a29beb4061bda66b6747e14','5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'),('36f18357be4dbd77f050515c73fcf9f2','69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'),('36f18357be4dbd77f050515c73fcf9f2','770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451')]
ptlst=[]

for index in range(len(ctlst)):
    #Key that encrypts the cypher text
    key = bytes.fromhex(ctlst[index][0])
    
    #The cypher text itself
    ct = bytes.fromhex(ctlst[index][1])
    
    #The plain text
    pt=[]
    
    
    
    
    #CBC
    if index<2:
        cipher = AES.new(key, AES.MODE_ECB)
        for i in range(int(len(ct)/16)-1):
            part1 = ct[16*i:16*(i+1)]
            part2 = cipher.decrypt(ct[16*(i+1):16*(i+2)])
            for j in range(16):
                pt.append(part1[j]^part2[j])
        
        pt=pt[:len(pt)-pt[-1]]
    
    
    
    
    
    #CTR
    else:
        cipher = AES.new(key, AES.MODE_ECB)
        iv=ct[0:16]
        for i in range(math.floor(len(ct)/16)-1):
            newiv=(int.from_bytes(iv, byteorder='big', signed=False)+i) & 0xffffffffffffffffffffffffffffffff
            newiv=bytes.fromhex(hex(newiv)[2:])
            
            part1 = ct[16*(i+1):16*(i+2)]
            part2 = cipher.encrypt(newiv)
            for j in range(16):
                pt.append(part1[j]^part2[j])
        
        newiv=(int.from_bytes(iv, byteorder='big', signed=False)+i+1) & 0xffffffffffffffffffffffffffffffff
        newiv=bytes.fromhex(hex(newiv)[2:])
            
        part1 = ct[16*(i+2):]
        part2 = cipher.encrypt(newiv)
        print(part2, part1)
        for j in range(len(part1)):
            pt.append(part1[j]^part2[j])
    
    
    
    
    #The array pt is finally converted to a string and added to the list
    pt = ''.join(chr(e) for e in pt)
    ptlst.append(pt)

print(ptlst)

