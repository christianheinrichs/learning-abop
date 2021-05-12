#!/usr/bin/env python2
# -*- coding: utf-8 -*-

def reverse(text):
    return text[::-1]

def is_palindrome(text):
    return text == reverse(text)

# The following is a tuple containing the forbidden characters which are:
# . ? ! : ; - — () [] ... ’ “ ” / , ' " and the space character
forbidden = (".", "?", "!", ":", ";", "-", "—", "(", ")", "[", "]", "..." \
            "’", "“", "”", "/", ",", "'", "\"", " ")

something = raw_input("Enter text: ")
something = something.lower()

# Iterate through every character of the user's input
for x in something:
    # If the character is one of the forbidden
    if x in forbidden:
        # Replace it with nothing
        for char in forbidden:
            something = something.replace(char, "")
    else:
        # Else, continue
        pass

if is_palindrome(something):
    print "Yes, it is a palindrome"
else:
    print "No, it is not a palindrome"
