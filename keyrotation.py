import os
import boto3
import base64
import botocore
import tkinter
from tkinter import filedialog
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

ec2 = boto3.client('ec2')
response = ec2.describe_key_pairs()
key_name = []
decodedpublickeys = []
publickeys = []
privatekeys = []

def get_key_pair_names():
    kp = response.get('KeyPairs')
    for k in kp:
        n = (k.get('KeyName'))
        key_name.append(n)

#Function generating Keys

def gen_keys():
    get_key_pair_names()
    counter = len(key_name)
    i=0
    while i<counter:
        key = rsa.generate_private_key(backend=default_backend(), key_size=2048, public_exponent=65537)
        pubkey = key.public_key().public_bytes(encoding=serialization.Encoding.OpenSSH, format=serialization.PublicFormat.OpenSSH)
        publickeys.append(pubkey)
        pubkey_str = pubkey.decode('utf-8')
        decodedpublickeys.append(pubkey_str)
        prikey = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
        prikey_str = prikey.decode('utf-8')
        privatekeys.append(prikey_str)
        i+=1

gen_keys()

print("Generated Keys Successfully !!")

#Importing Key pairs to aws

def import_key_pairs():
    try:
        for name in key_name:
            ec2.describe_key_pairs(KeyNames=[name])
            ec2.delete_key_pair(KeyName=name, DryRun=False)

    except botocore.exceptions.ClientError:
        for keys in publickeys:
            for names in key_name:
                if publickeys.index(keys) == key_name.index(names):
                    ec2.import_key_pair(DryRun=False, KeyName=names, PublicKeyMaterial=keys)
    else:
        for keys in publickeys:
            for names in key_name:
                if publickeys.index(keys) == key_name.index(names):
                    ec2.import_key_pair(DryRun=False, KeyName=names, PublicKeyMaterial=keys)

import_key_pairs()

print("Imported new sets of key pairs successfully !! ")            

#Saving public keys
def save_pub_keys():
    for name in key_name:
        for item in decodedpublickeys:
            if key_name.index(name) == decodedpublickeys.index(item):
                f = filedialog.asksaveasfile(mode="w", defaultextension=".pub", title=f"Save your {name} Public Key File ")
                f.writelines(item)
                f.close()

save_pub_keys()

print("Updated repository with public keys !!!")

def save_private_keys():
    for name in key_name:
        for item in privatekeys:
            if key_name.index(name) == privatekeys.index(item):
                f = filedialog.asksaveasfile(mode="w", defaultextension=".pem", title=f"Save your {name} private key File ")
                f.writelines(item)
                f.close()
        
save_private_keys()

print("Updated local private key folder !!!")
