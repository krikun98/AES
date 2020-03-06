import galois_math
import random
import time

prime = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF
field = galois_math.Galois(prime)
field.__mon_init__()
g = 2
a = random.randint(field.r >> 1, field.r-1)
b = random.randint(field.r >> 1, field.r-1)
g_a = field.mon_exp_kor(g, a)
g_b = field.mon_exp_kor(g, b)
t0 = time.perf_counter()
k_a = field.exp(g_b, a)
t1 = time.perf_counter()
print('sta_exp', field.k, t1 - t0, k_a)
t0 = time.perf_counter()
k_a = field.mon_exp(g_b, a)
t1 = time.perf_counter()
print('mon_exp', field.k, t1 - t0, k_a)
t0 = time.perf_counter()
k_a = field.mon_exp_kor(g_b, a)
t1 = time.perf_counter()
print('acc_exp', field.k, t1 - t0, k_a)
k_b = field.mon_exp_kor(g_a, b)
message = 'TEST'
enc_message = message ^ k_a
dec_message = enc_message ^ k_b
print(k_a)
print(k_b)
