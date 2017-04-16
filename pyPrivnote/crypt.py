#!/usr/bin/python
# -*- coding: utf-8 -*-


from base64 import b64decode, b64encode
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

from .util import score_salt


def openSSLkey(password_bytes, salt_arr):
    """
    OpenSSLkey for privnote (en/de)cryption
    :param password_bytes: byte-like
        Privnote password
    :param salt_arr: byte-like
        Salt block
    :return: dict
        Key and initialization vector (iv) for (en/de)cryption
    """
    passalt = password_bytes + salt_arr
    result = cur_hash = md5(passalt).digest()
    for i in range(2):
        cur_hash = md5(cur_hash + passalt).digest()
        result += cur_hash

    return {
        "key": result[0  : 4*8],
        "iv": result[4*8 : 4*8+16]
    }


def enc(plain_text, password):
    """
    Encrypts fallowing privnote rules
    :param plain_text: str
        Data to encrypt
    :param password: byte-like
        Password for encryption
    :return: bytes
        Encrypted data
    """
    salt = score_salt()
    salt_block = b"Salted__" + salt

    pbe = openSSLkey(password, salt)
    key = pbe["key"]
    iv = pbe["iv"]

    cipher = AES.new(key, AES.MODE_CBC, iv, use_aesni=True)
    cipher_blocks = cipher.encrypt(pad(plain_text.encode(), cipher.block_size))
    cipher_blocks = salt_block + cipher_blocks
    return b64encode(cipher_blocks)


def dec(crypt_data, password):
    """
    Encrypts fallowing privnote rules
    :param crypt_data: byte-like
        Encrypted data gotten from enc function or privnote.com
    :param password: byte-like
        Password for decryption that was used for encryption
    :return: str
        Decrypted plain text
    """
    crypt_bytes = b64decode(crypt_data)
    salt = crypt_bytes[8:16]
    crypt_bytes = crypt_bytes[16:]

    pbe = openSSLkey(password, salt)
    key = pbe["key"]
    iv = pbe["iv"]

    cipher = AES.new(key, AES.MODE_CBC, iv, use_aesni=True)
    return unpad(cipher.decrypt(crypt_bytes), cipher.block_size).decode()
