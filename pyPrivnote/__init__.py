#!/usr/bin/python
# -*- coding: utf-8 -*-


from .model import PrivMessage as _PrivMessage


def create_note(data, manual_pass="", duration_hours=0,
                ask_confirm=True, notify_email="", email_ref_name=""):
    """
    Creates a note and returns link to it

    :param data: str
        String data for noting

    :param manual_pass: str, byte-like
        Every false value means auto generating pass 9 alphadigit chars
        manual password must be str or byte-like object. Using byte-like object may cause inability
        to read note via privnote web interface.

    :param duration_hours: integer [0-720]
        Hours of life for note, that will self-destroyed on expiry. 0 or every false value
        means self-destruct after reading. Anyway note life can't be more then 720 hours (30 days)

    :param ask_confirm:
        Every true value means ask for confirmation before showing and destroying the note.
        Every false value means do not ask for confirmation (Privnote Classic behaviour)

    :param notify_email: str
        E-mail to notify when note is destroyed. Every false value means no notification

    :param email_ref_name: str
        Reference name for the note that will be sent to notification email when it destruct

    :return: str
        Notelink for reading Note. If manual_pass was given, autogenerating password concatenate to link
    """

    message = _PrivMessage()
    message.set_settings(data, manual_pass, duration_hours,
                         ask_confirm, notify_email, email_ref_name)
    message.encrypt()
    message.send()
    return message.link


def read_note(link=None, password=None, _id=None):
    """
    Gets a note from privnote.com and returns note text

    :param link: str
        Link referring to note
    :param password: str or byte-like
        Password for decoding note (if not given with link)
    :param _id: str
        Id of the note (if no link)
    :return: str
        Text of read note
    """
    if link and _id:
        raise AttributeError("Required link or _id but no link and _id together")
    if _id and not password:
        raise AttributeError("Required password with _id argument")
    message = _PrivMessage()
    if link:
        message.link = link
    if _id:
        message.id = _id
    if password:
        message.password = password
    if not message.password:
        raise AttributeError("Link is incomplete or password was not given")

    message.read_and_destroy()
    message.decrypt()
    return message.plain_text
