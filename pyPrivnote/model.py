#!/usr/bin/python
# -*- coding: utf-8 -*-


from datetime import datetime
import requests

from .exceptions import *
from .constants import HEADERS
from .util import is_email, score_password
from .crypt import dec, enc


class PrivMessage(object):

    def __init__(self):
        self._plain_text = None
        self._crypt_text = None
        self._link = None
        self._id = None
        self._password = None
        self._is_crypted = False
        self._settings = None
        self._response = None

    @property
    def password(self):
        if not self._password:
            raise ValueError("Password is not set - This note needs a password")
        return self._password.decode()

    @password.setter
    def password(self, value):
        if isinstance(value, str):
            self._password = value.encode("utf-8")
        elif isinstance(value, bytearray) or isinstance(value, bytes):
            self._password = value

    @property
    def link(self):
        """
        Form link fallowing privnote rules
        :return: str
            Link to read the note. If no manual_password was given then password concatenates to link with '#' sep
        """
        if self._response:
            if self._response["has_manual_pass"]:
                return self._response['note_link']
            else:
                return "%s#%s" % (self._response['note_link'], self.password)
        else:
            return "https://privnote.com/" + self._id

    @link.setter
    def link(self, value):
        """Set link and parse"""

        if value.startswith("privnote.com/"):
            value = "https://" + value
        value = value.split(r"https://privnote.com/")[1]
        value = value.split("#", maxsplit=1)
        self._id = value[0]
        if len(value) == 2 and value[1]:
            self._password = bytes(value[1], encoding="utf-8")

    @property
    def id(self):
        if self._id:
            return self._id
        else:
            return self._response['note_link'].replace(r"https://privnote.com/", "")

    @id.setter
    def id(self, value):
        self._id = value
        self._link = "https://privnote.com/" + value

    @property
    def plain_text(self):
        return self._plain_text

    def read_and_destroy(self):
        """
        Receives note from privnote.com thereby destroy note and nobody can read it anymore
        :raises
            NoteDestroyedException if note already readed or self-destructed
            IncorrectIDException if note with id cant be fond

        """
        resp = requests.delete(self.link, headers=HEADERS)

        exc = None
        try:
            self._response = resp.json()
        except ValueError:
            exc = True
        if exc:
            raise IncorrectIDException(note_id=self._id)

        if not self._response.get("data"):
            if self._response.get("destroyed"):
                raise NoteDestroyedException(note_id=self._id,
                                             destroyed=datetime.strptime(self._response["destroyed"],
                                                                         "%Y-%m-%dT%H:%M:%S.%f"))
            else:
                raise PrivnoteException("No data in response")
        self._crypt_text = self._response['data']

    def set_settings(self, data, manual_pass=False, duration_hours=None,
                     ask_confirm=True, notify_email=False, email_ref_name=''):
        """
        Parse and stores arguments. Forms settings dict to send. Forms data and password to encrypt

        :param data: str
            String data for noting

        :param manual_pass: str, byte-like
            Every false value means auto generating pass 9 alphadigit chars
            manual password must be str or byte-like object. Using byte-like object may cause inability
            to read note via privnote web interface.

        :param duration_hours: integer [0-720]
            Hours of life for note, that will self-destroyed on expiry. 0 or every false value
            means self-destruct after reading. Anyway note life can't be more then 720 hours (30 days)

        :param ask_confirm: boolean
            Every true value means ask for confirmation before showing and destroying the note.
            Every false value means do not ask for confirmation (Privnote Classic behaviour)

        :param notify_email: str
            E-mail to notify when note is destroyed. Every false value means no notification

        :param email_ref_name: str
            Reference name for the note that will be sent to notification email when it destruct

        :return: str
            Notelink for reading Note. If manual_pass was given, autogenerating password concatenate to link
        """

        settings = {}

        if type(data) != str:
            raise TypeError("Argument 'data' must be string, not %s" % type(data))
        if data == "":
            raise ValueError("Argument data must not be empty")
        settings['data_type'] = 'T'

        if manual_pass:
            if isinstance(manual_pass, (str, bytearray, bytes)):
                password = manual_pass
                settings['has_manual_pass'] = "true"
            else:
                raise TypeError("Argument 'manual_pass' must be str or bytes-like")
        else:
            password = score_password()
            settings['has_manual_pass'] = "false"

        if duration_hours:
            settings['duration_hours'] = duration_hours
        else:
            settings['duration_hours'] = 0

        if ask_confirm:
            settings['dont_ask'] = "false"
        else:
            settings['dont_ask'] = "true"

        if notify_email:
            if is_email(notify_email):
                settings['notify_email'] = notify_email
                if email_ref_name:
                    settings['notify_ref'] = email_ref_name
                else:
                    settings['notify_ref'] = ""
            else:
                raise ValueError("Notify email is incorrect")
        else:
            settings['notify_email'] = settings['notify_ref'] = ""

        self._plain_text = data
        self.password = password
        self._settings = settings

    def decrypt(self):
        """Decrypts note"""

        try:
            self._plain_text = dec(self._crypt_text, self._password)
        except ValueError:
            raise IncorrectPasswordException(note_id=self._id)

    def encrypt(self):
        """Encrypts note"""

        try:
            self._crypt_text = enc(self._plain_text, self._password)
        except ValueError:
            raise IncorrectPasswordException(note_id=self._id)

    def send(self):
        """Sends data with note settings to privnote server and stores response"""

        data_to_send = self._settings.copy()
        data_to_send['data'] = self._crypt_text.decode()
        response = requests.post("https://privnote.com/legacy/", data=data_to_send, headers=HEADERS)
        self._response = response.json()
