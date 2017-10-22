
from Crypto.Cipher import AES
import codecs
import math

cbc_key = '140b41b22a29beb4061bda66b6747e14'
cbc_cypher_text1 = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
cbc_cypher_text2 = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'

ctr_key = '36f18357be4dbd77f050515c73fcf9f2'
ctr_cypher_text1 = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'
ctr_cypher_text2 = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'

def cbc_decrypt(key, cypher_text, block_size=16):
    key = codecs.decode(key, 'hex')
    cypher_text = codecs.decode(cypher_text, 'hex')
    ctb = [cypher_text[i:i+block_size] for i in range(0, len(cypher_text), block_size)]

    pt = ''
    cypher = AES.new(key, AES.MODE_ECB)
    for i in range(len(ctb)-1):
        part = cypher.decrypt(ctb[i+1])
        text = ''
        text = intxor(ctb[i], part)
        pt += text

    return pt

def ctr_decrypt(key, cypher_text, block_size=16):
    key = codecs.decode(key, 'hex')
    cypher_text = codecs.decode(cypher_text, 'hex')
    iv = cypher_text[:block_size]
    ctb = [cypher_text[i:i+block_size] for i in range(0, len(cypher_text), block_size)]
    cypher = AES.new(key, AES.MODE_ECB)
    pt = ''
    for i in range(math.floor(len(ctb)) - 2):
        newiv = int(codecs.encode(iv, 'hex'), 16) + i
        newiv = bytes.fromhex(hex(newiv)[2:])
        part = cypher.encrypt(newiv)
        text = ''
        text = intxor(ctb[i+1], part)
        pt += text

    newiv = int(codecs.encode(iv, 'hex'), 16) + i + 1
    newiv = bytes.fromhex(hex(newiv)[2:])
    newiv = codecs.decode(codecs.encode(newiv, 'hex'), 'hex')
    part = cypher.encrypt(newiv)
    pt += intxor(ctb[i+2], part)

    return pt

def strxor(a, b):     # xor two strings of different lengths
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

def intxor(a, b):
    return "".join([chr(x ^ y) for (x, y) in zip(a, b)])

def main():
    p1 = cbc_decrypt(cbc_key, cbc_cypher_text1)
    p2 = cbc_decrypt(cbc_key, cbc_cypher_text2)
    p3 = ctr_decrypt(ctr_key, ctr_cypher_text1)
    p4 = ctr_decrypt(ctr_key, ctr_cypher_text2)
    print(p1)
    print(p2)
    print(p3)
    print(p4)

if __name__ == '__main__':
    main()
