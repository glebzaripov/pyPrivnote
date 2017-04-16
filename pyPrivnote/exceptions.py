#!/usr/bin/python
# -*- coding: utf-8 -*-


class PrivnoteException(Exception):

    def __str__(self):
        return self.message


class NoteDestroyedException(PrivnoteException):

    def __init__(self, note_id, destroyed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destroyed_date = destroyed
        self.note_id = note_id
        self.message = "The note with id %s was read and destroyed at %s. " \
                       "If you haven't read this note it means someone else has. " \
                       "If you read it but forgot to write it down, " \
                       "then you need to ask whoever sent it to re-send it." % (self.note_id, self.destroyed_date)


class IncorrectPasswordException(PrivnoteException):

    def __init__(self, note_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.note_id = note_id
        self.message = "The note (id=%s) link or password is incomplete or incorrect, " \
                       "and the note could not be decrypted." % self.note_id


class IncorrectIDException(PrivnoteException):

    def __init__(self, note_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.note_id = note_id
        self.message = "The note with id %s was not found." % self.note_id
