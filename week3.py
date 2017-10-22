
import os
import codecs
from Crypto.Hash import SHA256

# hash = SHA256.new()
# hash.update('message'.encode('utf-8'))
# hash.update('message'.encode('utf-8'))
# hash.update('messagemessage'.encode('utf-8'))
# print(hash.hexdigest())

def calc_file_hash(file_path, block_size):
    if not os.path.isfile(file_path):
        return
    file_size = os.path.getsize(file_path)
    last_hash = ''
    with open(file_path, 'rb') as fb:
        data = read_reversed_chunks(fb, file_size, block_size)
        for chunk in data:
            hash = SHA256.new()
            hash.update(chunk)
            if last_hash:
                hash.update(last_hash)
            last_hash = hash.digest()
        return last_hash

def read_reversed_chunks(file_object, file_size, chunk_size):
    base_chunks = (file_size // chunk_size)
    last_chunk_size = file_size % chunk_size
    chunks = base_chunks + (last_chunk_size and 1)
    iter = chunks
    while iter > 0:
        pos = file_size - chunk_size * (chunks - iter) - last_chunk_size 
        file_object.seek(pos)
        data = file_object.read(chunk_size)
        iter -= 1
        if not data:
            break
        yield data

if __name__ == '__main__':
    file_name = '6.2.birthday.mp4_download'
    file_name = '6.1.intro.mp4_download'
    hash_check = '03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8'
    
    v = calc_file_hash(file_name, 1024)
    v = codecs.encode(v, 'hex').decode('utf-8')
    
    print(v, hash_check)
