#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

email_pattern = re.compile("^([a-zA-Z0-9\\._\\-\\+%]+)@([a-zA-Z0-9\\.\\-]+)\\.([a-zA-Z]){2,24}$")

auto_pass_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"

HEADERS = {
    "X-Requested-With"  : "XMLHttpRequest",
}
