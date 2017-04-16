# pyPrivnote
A Python Interface to Privnote service


#### [privnote.com](https://privnote.com): Send notes that will self-destruct after being read.

Privnote allows you to create one-time-pad encrypted, burn-after-reading notes over the internet. It's a great way to share passwords or other sensitive peices of information.

### Installation

```shell
pip install pyPrivnote
```

### Usage

Functions **create_note** and **read_note** thats all you need to use full functionality of Privnote

#### To make a simple note call function create_note.

```python
import pyPrivnote as pn

note_link = pn.create_note("Private message")
# "https://privnote.com/hl5R6EqM#UFgVC2UHD"
```

#### To read note call read_note with note link.

```python
note_text = pn.read_note(note_link)
# "Private message"
```

##### Making/reading notes with manual password.

```python
import pyPrivnote as pn

note_link = pn.create_note("Super secret message", manual_pass="12345")
# "https://privnote.com/w0q6kGlR"

note_text = pn.read_note(note_link, password="12345")
# "Super secret message"
```

#### Full functionality of privnote
**Manual password** <br>
**E-mail notification** with _reference name_ <br>
Note **self-destructs** after reading or _expire lifetime_ <br>
**Asking confirmation** before reading _(only for web reading)_

```python
import pyPrivnote as pn

note_link = pn.create_note(
                "Super secret message",
                manual_pass="12345",
                duration_hours=5,
                ask_confirm=False,
                notify_email="address@domain.com",
                email_ref_name="Note sent to Bob"
                )
```

#### Release History

v0.0.1 - First release
