import galois_math
import random

prime = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF
field = galois_math.Galois(prime)
field.__mon_init__()
g = 2


def encrypt(message, y):
    block = int(bytearray(message, 'utf8').hex(), 16)
    k = random.randint(1, field.r-1)
    # print('sor_block', hex(block)[2:])
    a = field.mon_exp_kor(g, k)
    b = field.mult(field.mon_exp_kor(y, k), block)
    return a, b


def decrypt(a, b, x):
    a_t = field.mon_exp_kor(a, x)
    a_inv = field.inv(a_t)
    m = field.mult(b, a_inv)
    # print('dec_block', hex(m)[2:])
    message = bytearray.fromhex(hex(m)[2:]).decode('utf8')
    return message


x = random.randint(field.r >> 1, field.r-1)
y = field.mon_exp_kor(g, x)
message = "arlekino"
print('sor_message', message)
enc_message_a, enc_message_b = encrypt(message, y)
dec_message = decrypt(enc_message_a, enc_message_b, x)
print('dec_message', dec_message)