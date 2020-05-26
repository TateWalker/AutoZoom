from licensing.models import Response, RSAPublicKey, LicenseKey
from licensing.methods import Key, Helpers
import json
import os
from os import path
import sys

def main(key):

    pubKey = "<RSAKeyValue><Modulus>08yy3bS4xdfjrOcUMDDsWHQc9LqT3g4vboGATTk64eUfM2Fw0Z2EKl4SYXdLbXLd8l0zYZhvpkpMYEe00LGo0RoKGz5z+4l5dKro66s7TSoaJfIFUnevQUe/R/Hbf/8NGDvUPc/X1GsMowKMBKRZGeowvR07DYgGcncZSUwXsKlB0zPsunYZ8eoyqKzooDyqeAxftIVD1sv5d1HHbF10m8rq/hDInPyvgY0IwIxvWxvcsttIyHBdHIG/aWU2lfSgLZC6XP7T27YqOxgpwlDuPfN64qB3r3psboWEqtkBwjyc/mB1zU86gldPUevYX7zGq1GdsRLN8gVZeOqPtx35gw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"

    res = Key.activate(token="WyIxODk3NCIsIlRsd1JNVytGY1FRTndkTW9IUFAxci94UG44UXk1SVRDaXVheExLMmsiXQ==",\
                       rsa_pub_key=pubKey,\
                       product_id=6258, key=key, machine_code="")

    bundle_dir = os.getcwd()
    path_to_key = path.join(bundle_dir, '.keyFile')
    path_to_license = path.join(bundle_dir, '.licenseFile')
    # print(bundle_dir)
    if res[0] == None:
        try:      
            with open(path_to_license) as f:
                l_file = json.load(f)
                license = LicenseKey.load_from_string(pubKey,l_file)
                if license:
                    # print('Valid License!')
                    return True, ''
                else:
                    # print('Invalid License!')
                    return False,''
        except:
            return False,''
    else:
        # print("Success")
        saved_license = res[0].save_as_string()
        with open(path_to_license,'w') as f:
            json.dump(saved_license,f)
        with open(path_to_key,'w') as f:
            f.write(key)
        return True,''


if __name__ == '__main__':
        main()