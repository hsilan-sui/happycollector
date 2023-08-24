from ucryptolib import aes

# 16位的AES金鑰（這只是示例，請使用自己生成的安全金鑰）
aes_key = b'\xe7\xe4b\xe2\xc5.\x8f\xf4>\xd2l}\xf6\xc6\xb0\x19\xdf!\x86d\xa0*\xa9\xbd\x04k\xc7r\x9a\xffjh'
aes_iv = b'\xd8\x94\x8f\xc4~\x8d\x18\xb0)Tg\xe5\xa9\xdf\xdb\x9a'
#aes_key = b'[Secret Wokwi key with 256 bits]'
#aes_iv = uos.urandom(16) # In real life, uos.urandom(16)



def pad(data):
    padded = data + " " * (16 - len(data) % 16)
    return padded

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

#padded = plain + " " * (16 - len(plain) % 16)
#encrypted = cipher.encrypt(padded)
#print('Encrypted: {}'.format(encrypted))


def encrypt(data):
    cipher = aes(aes_key, 2, aes_iv)
    encrypted = cipher.encrypt(pad(data))
    return encrypted

def decrypt(data):
    cipher = aes(aes_key, 2, aes_iv)
    decrypted = (cipher.decrypt(data))
    return decrypted

# 讀取並解密配置文件
def read_encrypted_config(file_path):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')

# 主程式
def getconfig():
    config_path = 'config.bin'
    decrypted_config = read_encrypted_config(config_path)
    config_lines = decrypted_config.split('\n')
    
    config = {}
    for line in config_lines:
        key, value = line.strip().split('=')
        config[key] = value
    
    return config
