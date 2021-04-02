#!/usr/bin/env python2

#############################################################################
#                                                                           #
#  more_address-book.py - An interactive address book written in Python 2   #
#  Copyright (C) 2014 Christian Heinrichs <christian.heinrichs@mykolab.ch>  #
#                                                                           #
#  This program is free software: you can redistribute it and/or modify     #
#  it under the terms of the GNU General Public License as published by     #
#  the Free Software Foundation, either version 3 of the License, or        #
#  (at your option) any later version.                                      #
#                                                                           #
#  This program is distributed in the hope that it will be useful,          #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#  GNU General Public License for more details.                             #
#                                                                           #
#  You should have received a copy of the GNU General Public License        #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                           #
#############################################################################

# more_address-book.py written by Christian Heinrichs - 02/04/2021

# This is my version of the address book task from ‘A Byte of Python’
# The following scripts helped me a lot with different problematic parts of
# the address book program:
# http://codetique.jimsaunders.net/raw/jLRgWZyA
# https://github.com/akshar-raaj/Python-Programs/blob/master/address-book.py
# http://www.bobgolobish.com/creating-an-address-book-program-in-python-part-4/
# http://www.daniweb.com/software-development/python/threads/285866/address-book-python-project#post1323357

import pickle
import sys

class AddressBook():
    """
        This is our address book class.
        It has all methods we need to modify the address book objects
    """

    def __init__(self):
        """
        Check if the contacts file exists.
        If not, create an empty dictionary.
        This routine is very important as I had tons of problems with
        getting the pickle object to save persistently.
        Also note the double underscores "self.__a".
        That way we can make the ‘a’ variable accessible to all methods within
        this class without making it global.
        """
        self.__contactsfile = "contacts.data"
        try:
            f = open(self.__contactsfile, "rb")
            self.__a = pickle.load(f)
        except IOError:
            self.__a = {}

    def add(self):
        # Add a contact
        toadd = raw_input("Do you want to add a colleague, family member, friend or generic contact? ")
        toadd = toadd.lower()
        
        # Decide which instance should be created and thus determine the
        # contact type
        if toadd == "generic":
            toadd = Person()
        elif toadd == "colleague":
            toadd = Colleague()
        elif toadd == "family":
            toadd = Family()
        elif toadd == "friend":
            toadd = Friend()
        else:
            toadd = Person()
        
        # Use the dictionary method update() to add a new key with its values
        self.__a.update({toadd.full_name : [toadd.first_name, toadd.last_name, \
                         toadd.age, toadd.country, toadd.email, \
                         toadd.contacttype]})
        # You can also use this:
        """ self.__a[toadd.full_name] = [toadd.first_name, toadd.last_name, \
                                         toadd.age, toadd.country, toadd.email, \
                                         toadd.contacttype] """
        # Save the dictionary to the ‘contacts.data’ file
        self.savetofile()

        print "You successfully added {} to your address book!".format(toadd.full_name)

    def browse(self):
        # Browse contact list

        # Iterate through the sorted keys of the dictionary ‘self.__a’
        for x in sorted(self.__a.keys()):
            # Ask if the next or previous entry should be displayed
            userinput = raw_input("Next or previous entry? ")
            userinput = userinput.lower()

            # If the user enters ‘n’ or ‘next’, the current key where the
            # iteration is now located, gets displayed.
            # Otherwise, break out of the for loop
            if userinput == "n" or userinput == "next":
                print "Full name:", x
                print "First name:", self.__a[x][0]
                print "Last name:", self.__a[x][1]
                print "Age:", self.__a[x][2]
                print "Country:", self.__a[x][3]
                print "Email address:", self.__a[x][4]
                print "Contact type:", self.__a[x][5]
            else:
                break
            # I tried to implement a for loop which shows the previous entry.
            # However, the following code is extremely buggy:
            """
            elif userinput == "p" or userinput =="prev":
                for x in reversed(sorted(self.__a.keys())):
                    userinput = raw_input("next or prev: ")
                    if userinput == "p":
                        print x
                        continue
                    else:
                        break
            """

    def delete(self):
        # Delete a contact
        todel = raw_input("Who do you want to delete? ")
        # If the entered person exists in the address book, delete it with the
        # use of the dictionary method pop()
        if todel in self.__a.keys():
            self.__a.pop(todel)
            self.savetofile()
            print todel, "got deleted"
        else:
            print todel, "does not exist in the address book"

    def modify(self):
        # Edit a contact entry
        question = raw_input("Which contact to do you want to edit? ")
        # If the key exists
        if self.__a.has_key(question):
            # Show the user whom he/she is editing
            print "You are now editing", question
            firstname = raw_input("Edit first name: ")
            lastname = raw_input("Edit last name: ")
            fullname = firstname + " " + lastname
            age = raw_input("Edit age: ")
            country = raw_input("Edit country: ")
            email = raw_input("Edit email address: ")
            ct = raw_input("Edit contact type: ")
            # After all changes have been made, update the key, its values and
            # call the savetofile() method
            self.__a[fullname] = self.__a.pop(question)
            self.__a.update({fullname : [firstname, lastname, age, country, email, ct]})
            self.savetofile()
        else:
            print question, "is not in the address book!"

    def savetofile(self):
        # Open the address book and dump the dictionary as pickle object
        f = open(self.__contactsfile, "wb")
        pickle.dump(self.__a, f)
        f.close()

    def search(self):
        # Search for contacts
        tosearch = raw_input("Who are you looking for? ")
        # If the key exists
        if self.__a.has_key(tosearch):
            # Ask the user to view the entry
            print tosearch, "has been found."
            another_q = raw_input("Do you want to show her/his entry or exit? ")
            another_q = another_q.lower()
            # If the user wrote ‘yes’
            if another_q == "y" or another_q == "yes":
                # Show all information about the requested contact
                print "\nFull name: %s" % (tosearch)
                print "First name: %s" % (self.__a[tosearch][0])
                print "Last name: %s" % (self.__a[tosearch][1])
                print "Age: %s" % (self.__a[tosearch][2])
                print "Country: %s" % (self.__a[tosearch][3])
                print "Email address: %s" % (self.__a[tosearch][4])
                print "Contact type: %s" % (self.__a[tosearch][5])
            else:
                pass
        else:
            print tosearch, "has not been found."

    def showall(self):
        # Show all contacts

        # If the dictionary is not empty
        if self.__a != {}:
            # Iterate with two variables through the tuples of the dictionary
            # method items() and then display the key, value pair
            for key, value in sorted(self.__a.items()):
                print "\nFull name: %s" % (key)
                print "First name: %s" % (value[0])
                print "Last name: %s" % (value[1])
                print "Age: %s" % (value[2])
                print "Country: %s" % (value[3])
                print "Email address: %s" % (value[4])
                print "Contact type: %s" % (value[5])
        else:
            print "Contact list is empty!"

    def showsingle(self):
        # Show single contact
        toshow = raw_input("Which contact entry do you want to view? ")
        # If the key exists
        if self.__a.has_key(toshow):
            # Print the information about that contact
            print "\nFull name: %s" % (toshow)
            print "First name: %s" % (self.__a[toshow][0])
            print "Last name: %s" % (self.__a[toshow][1])
            print "Age: %s" % (self.__a[toshow][2])
            print "Country: %s" % (self.__a[toshow][3])
            print "Email address: %s" % (self.__a[toshow][4])
            print "Contact type: %s" % (self.__a[toshow][5])
        else:
            print "Key does not exist"

class Person():
    # Initialise the needed information with help of arguments and raw_input()
    def __init__(self):
        self.first_name = raw_input("Enter the contact's first name: ")
        self.last_name = raw_input("Enter the contact's last name: ")
        self.full_name = self.first_name + " " + self.last_name
        self.age = raw_input("Enter the contact's age: ")
        self.country = raw_input("From what country is the contact from? ")
        self.email = raw_input("Please enter the contact's email address: ")
        self.contacttype = "Generic contact"

# The next three classes inherit everything from the ‘Person’ object
# These classes were created to differentiate the contact types
class Colleague(Person):
    def __init__(self):
        Person.__init__(self)
        self.contacttype = "Colleague"

class Family(Person):
    def __init__(self):
        Person.__init__(self)
        self.contacttype = "Family"

class Friend(Person):
    def __init__(self):
        Person.__init__(self)
        self.contacttype = "Friend"

print '''
 ________________________________________________________________
|                                                                |
|  more_address-book.py  Copyright (C) 2014  Christian Heinrichs |
|  This program comes with ABSOLUTELY NO WARRANTY.               |
|  This is free software, and you are welcome to redistribute it |
|  under certain conditions.                                     |
|________________________________________________________________|   


Add a contact - add
Browse address book - browse
Delete a contact - delete
Edit a contact - modify
Search for a contact - search
Show all contacts - showall
Show one contact - showsingle

To exit the program, just type exit
'''

# Endless while loop for user decision
while True:
    ab_method = raw_input("Which method? ")
    # Either one of the specified methods gets executed, or
    if ab_method == "add":
        AddressBook().add()
    elif ab_method == "browse":
        AddressBook().browse()
    elif ab_method == "delete":
        AddressBook().delete()
    elif ab_method == "modify":
        AddressBook().modify()
    elif ab_method == "search":
        AddressBook().search()
    elif ab_method == "showall":
        AddressBook().showall()
    elif ab_method == "showsingle":
        AddressBook().showsingle()
    # The program quits with code 0, which indicates there are no problems
    elif ab_method == "exit":
        sys.exit(0)
    else:
        print "The entered method does not exist!"
