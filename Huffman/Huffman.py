import sys
import time
from bitarray import bitarray
import pickle

class Node:
    def __init__(self, byte = None, count = 0, left = None, right = None):
        self.byte = byte
        self.count = count
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.count < other.count

def code_huffman(dict, node, code):
    if node.byte == None:
        code_huffman(dict, node.left, code + bitarray('0'))
        code_huffman(dict, node.right, code + bitarray('1'))
    else: 
        dict[node.byte] = code


def huffman(byte_frec):
    nodes = [] # list of Node(byte, count)
    for byte, count in byte_frec.items():
        nodes.append(Node(byte, count))
    #for x in nodes:
        #print(x.byte, x.count)
    #print("\n")
    while len(nodes) > 1:
        min1 = min(nodes)
        nodes.remove(min1)
        min2 = min(nodes)
        nodes.remove(min2)
        nodes.append(Node(None, min1.count + min2.count, min1, min2))
    #for i in nodes:
        #print(i.byte, i.count)
    #print("\n")
    byte_code = {} # dict: byte_code[byte] = huff_code_of_this_byte
    code_huffman(byte_code, nodes[0], bitarray())
    #print(byte_code)
    return byte_code

def enc(path):
    f = open(path, 'rb')
    file = f.read()
    f.close()
    #print(file)
    byte_frec = {} # dict: byte_frec[byte] = count_of_this_byte_in_file
    for byte in file:
        if byte in byte_frec:
            byte_frec[byte] += 1
        else:
            byte_frec[byte] = 1
    #print(byte_frec)
    byte_code = huffman(byte_frec)

    new_path = path.split('.')[0] + '.zmh'
    extension = path.split('.')[1]
    new_f = open('encoded_file.zmh', 'wb')
    """
    new_f.write(b'Table:\n')
    for byte in byte_code:
        new_f.write(byte.to_bytes(1,"big"))
        new_f.write(b'\n')
        new_f.write(len(byte_code[byte]).to_bytes(1,"big"))
        new_f.write(b'\n')
        byte_code[byte].tofile(new_f)
        new_f.write(b'\n')
    new_f.write(b'\nText:\n')
    enc_text = bitarray()
    enc_text.encode(byte_code, file)
    enc_text.tofile(new_f)
    """
    enc_text = bitarray()
    enc_text.encode(byte_code, file)
    result = {'extension' : extension, 'table' : byte_code, 'text' : enc_text }
    #print(result)
    pickle.dump(result, new_f)
    new_f.close()
    print('Your file is encoded into "encoded_file.zmh"')

def dec(path):
    f = open(path, 'rb')
    """
    #file = f.read()
    str1 = f.readline() # b'Table\n'
    print(str)
    str1 = f.readline()
    str2 = f.readline()
    code_byte = {} # dict: code_byte[huff_code] = byte
    while str1 != b'Text:\n':
        code_byte[str1] = bitarray.frombytes(str2)
        str1 = f.readline()
        str2 = f.readline()
    enc_text = f.read()
    """
    result = pickle.load(f)
    enc_text = result['text']
    byte_code = result['table']
    extension = result['extension']
    #print(byte_code)
    #print(enc_text)
    """
    code_byte = {} # dict: code_byte[huff_code] = byte
    for byte in byte_code:
        code = byte_code[byte]
        code_byte[code] = byte
    text = enc_text.decode(byte_code)
    """
    dec_text = enc_text.decode(byte_code)
    #print('DECTEXT:', dec_text)
    f.close()
    dec_path = 'decoded_file.' + extension
    dec_f = open(dec_path, 'wb')
    for i in dec_text:
        tmp = i.to_bytes(1,"big")
        dec_f.write(tmp)
    dec_f.close()
    print('Your file is decoded into "decoded_file.' + str(extension) + '"')

# main
if len(sys.argv) > 2:   
    mode = sys.argv[1]
    path = sys.argv[2]
elif len(sys.argv) > 1: 
    mode = sys.argv[1]
    path = str(input('Enter path to the file:'))
else:
    mode = str(input('Enter mode (enc or dec):'))
    path = str(input('Enter path to the file:'))
start_time = time.time()
if mode == 'enc':
    print('ENCRYPTION_mode:')
    enc(path)
elif mode == 'dec':
    print('DECRYPTION_mode:')
    dec(path)
else:
    print('Wrong input')
print('Time in seconds: ', time.time() - start_time)
