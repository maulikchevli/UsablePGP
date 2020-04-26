#!/usr/bin/env python
# coding: utf-8

# In[73]:


from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm
import pgpy
import os
import glob


# In[22]:


def key_generation(user_name,passphrase):
    key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 2048)
    uid = pgpy.PGPUID.new(user_name)

    key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
            ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
            compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed])
    key.protect(passphrase, SymmetricKeyAlgorithm.AES256, HashAlgorithm.SHA256)
    return key


# In[42]:


# message is in string given by User
# pub_key is fetched from Database i.e Receivers public Key
def encryption(pub_key,message):
    pub_key_enc_pgpy, _ = pgpy.PGPKey.from_blob(pub_key)
    text_message = pgpy.PGPMessage.new(message)
    encrypted_message = pub_key_enc_pgpy.encrypt(text_message)
    return encrypted_message


# In[104]:


# sec_key is Private key stored on local device
# enc_message is encrypted message
def decryption(sec_key,enc_message,passphrase):
    temp_pgpy = pgpy.PGPKey()
    temp_pgpy.parse(sec_key)
    try:
        with temp_pgpy.unlock(passphrase):
            decrypted_message = temp_pgpy.decrypt(enc_message)
            return decrypted_message.message
    except:
        print("Wrong passphrase")


# In[109]:


# sec_key is key stored at local machine i.e private key
# message is string
def sign(sec_key,message,passphrase):
    temp_pgpy = pgpy.PGPKey()
    temp_pgpy.parse(sec_key)
    try:
        with temp_pgpy.unlock(passphrase):
            message = pgpy.PGPMessage.new(message)
            signature = temp_pgpy.sign(message)
            return signature
    except:
        print("Wrong passphrase")


# In[88]:


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
