import os
import base64
import boto3
import botocore
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


ec2 = boto3.client('ec2')
key_names = []
decodedpublickeys = []
publickeys = []
privatekeys = []

def get_key_names():
    response = ec2.describe_key_pairs()
    kp = response.get('KeyPairs')
    for k in kp:
        n = (k.get('KeyName'))
        key_names.append(n)
    if len(key_names) == 0:
        key_names.append(None)

# Replacing the Key Pair

def replacing_key_pair():
    key = rsa.generate_private_key(backend=default_backend(), key_size=2048, public_exponent=65537)
    pubkey = key.public_key().public_bytes(encoding=serialization.Encoding.OpenSSH, format=serialization.PublicFormat.OpenSSH)
    publickeys.append(pubkey)
    pubkey_str = pubkey.decode('utf-8')
    decodedpublickeys.append(pubkey_str)
    prikey = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
    prikey_str = prikey.decode('utf-8')
    privatekeys.append(prikey_str)
    
    get_key_names()

    try:
        for name in key_names:
            ec2.describe_key_pairs(KeyNames=[name])
            
    except botocore.exceptions.ParamValidationError:           
        print("There are No Key Pairs to replace")
        
    else:
        print("Select the Key pair you want to replace \n")
        for k in key_names:
            print(f'{key_names.index(k)+1}.{k}')
        while True:    
            try:
                global i
                i = int(input())
            except:
                print(f"Please select an integer value form 1 to {len(key_names)}")
                continue
            else:
                try:
                    print(f"Replacing {key_names[i-1]} key !! ")
                    ec2.delete_key_pair(KeyName=key_names[i-1], DryRun=False)
                    ec2.import_key_pair(DryRun=False, KeyName=key_names[i-1], PublicKeyMaterial=publickeys[0])
                    print(f"{key_names[i-1]} Key is succesfully replaced !! ")
                    break
                except IndexError:
                   print(f"Please select an integer value form 1 to {len(key_names)}")
                   continue
             
# Saving Keys to Repository
    
def save_private_keys():
    try:
        f = open(key_names[i-1]+".pem", "w")
        f.writelines(privatekeys[0])
        f.close()
    except FileNotFoundError:
        f = open(key_names[i-1]+".pem", "x")
        f.writelines(privatekeys[0])
        f.close()

def save_public_keys():
    try:
        f = open(key_names[i-1]+".pub", "w")
        f.writelines(decodedpublickeys[0])
        f.close()
    except FileNotFoundError:
        f = open(key_names[i-1]+".pub", "x")
        f.writelines(decodedpublickeys[0])
        f.close()

def save_encoded_public_keys():
    try:
        f = open("encoded_"+key_names[i-1]+".txt", "w")
        f.writelines(str(publickeys[0]))
        f.close()
    except FileNotFoundError:
        f = open("encoded_"+key_names[i-1]+".txt", "x")
        f.writelines(str(publickeys[0]))
        f.close()

replacing_key_pair()

print("Successfully replaced the Key Pair on AWS !!! \n")

save_private_keys()
save_public_keys()
save_encoded_public_keys()


print("The Keys were successfully saved !!")
