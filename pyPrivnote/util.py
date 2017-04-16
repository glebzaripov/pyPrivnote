#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import choice, randint
from .constants import email_pattern, auto_pass_chars


def is_email(email_adr):
    """
    Email validation test
    :param email_adr: str
        Email fot validation
    :return: boolean
        True if email match email pattern, False otherwise
    """
    return bool(email_pattern.match(email_adr))


def score_password(length=9):
    """
    Scores auto password if manual one was not given
    :param length: Integer
        Length of password in chars (Privnote default 9 chars)
    :return: bytearray
        (length) bytes generated password
    """
    password = bytearray()
    for i in range(length):
        password.append(ord(choice(auto_pass_chars)))
    return password


def score_salt(length=8):
    """
    Scores random salt
    :param length: Integer
        Length of salt in bytes
        Defoult: 8. Other values may cause incorrect work with privnote
    :return: byteaaray
        Generated random salt
    """
    salt = bytearray()
    for i in range(length):
        salt.append(randint(0, 255))
    return salt
