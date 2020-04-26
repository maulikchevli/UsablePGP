#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm
import pgpy
import os
import glob


# In[2]:


def key_generation(user_name):
    key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 2048)
    uid = pgpy.PGPUID.new(user_name)
    # print(uid)

    key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
            ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
            compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed])
    return key
    # print(key)


# In[3]:


# message is in string given by User
# pub_key is fetched from Database i.e Receivers public Key
def encryption(pub_key,message):
    pub_key_enc_pgpy, _ = pgpy.PGPKey.from_blob(pub_key)
    text_message = pgpy.PGPMessage.new(message)
    encrypted_message = pub_key_enc_pgpy.encrypt(text_message)
    return encrypted_message


# In[4]:


# sec_key is Private key stored on local device
# enc_message is encrypted message
def decryption(sec_key,enc_message):
    temp_pgpy = pgpy.PGPKey()
    temp_pgpy.parse(sec_key)
    decrypted_message = temp_pgpy.decrypt(enc_message)
    return decrypted_message.message


# In[5]:


# sec_key is key stored at local machine i.e private key
# message is string
# function will return signature only, that is not attached to message
def sign(sec_key,message):
    temp_pgpy = pgpy.PGPKey()
    temp_pgpy.parse(sec_key)
    message = pgpy.PGPMessage.new(message)
    signature = temp_pgpy.sign(message)
    return signature


# In[7]:


# pub_key is key fetched from DB
# message is signed string message
def verify(pub_key,message,signature):
    pub_key, _ = pgpy.PGPKey.from_blob(pub_key)
    temp_pgpy = pgpy.PGPSignature()
    temp_pgpy.parse(signature)
    if pub_key.verify(message,temp_pgpy):
        return True
    else:
        return False


