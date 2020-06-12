from licensing.models import *
from licensing.methods import Key, Helpers
import json
import os
from os import path

def main(key):

    pubKey = "<RSAKeyValue><Modulus>08yy3bS4xdfjrOcUMDDsWHQc9LqT3g4vboGATTk64eUfM2Fw0Z2EKl4SYXdLbXLd8l0zYZhvpkpMYEe00LGo0RoKGz5z+4l5dKro66s7TSoaJfIFUnevQUe/R/Hbf/8NGDvUPc/X1GsMowKMBKRZGeowvR07DYgGcncZSUwXsKlB0zPsunYZ8eoyqKzooDyqeAxftIVD1sv5d1HHbF10m8rq/hDInPyvgY0IwIxvWxvcsttIyHBdHIG/aWU2lfSgLZC6XP7T27YqOxgpwlDuPfN64qB3r3psboWEqtkBwjyc/mB1zU86gldPUevYX7zGq1GdsRLN8gVZeOqPtx35gw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
    bundle_dir = os.getcwd()
    # print(bundle_dir)
    path_to_key = path.join(bundle_dir,'autozoom/data','.keyFile')
    # print(path_to_key)
    path_to_license = path.join(bundle_dir,'autozoom/data','.licenseFile')
    try:
        f = open(path_to_license,'r')
        l_file = json.load(f)
        f.close()
        license = LicenseKey.load_from_string(pubKey,l_file)
        if license == None or not Helpers.IsOnRightMachine(license):
            # print('Valid License!')
            raise ValueError('no license file')
        else:
            return True, ''
            
    except:
        res,mess = Key.activate(token="WyIyMjkwNiIsIkZoZWRHeno4K3g2UXl1T2ZzMnJzNDRybkpTMTcyVkdmYURsZUYyL0siXQ==",\
               rsa_pub_key=pubKey,\
               product_id=6258, key=key,\
               machine_code=Helpers.GetMachineCode())
        # print('Invalid License!')
        # print(key)
        # print(Helpers.GetMachineCode())
        # print(res)
        # print(mess)
     


        if res == None or not Helpers.IsOnRightMachine(res):
            return False,mess
        else:
            saved_license = res.save_as_string()
            with open(path_to_license,'w') as f:
                # print(path_to_license)
                json.dump(saved_license,f)
            with open(path_to_key,'w') as f:
                f.write(key)
            return True,''

if __name__ == '__main__':
        main()