#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
""" cipher.app.filecrypt

    File encryption script.

    Current uses an 'extended' AES algorithm.

    2002 by Paul A. Lambert
    Read LICENSE.txt for license information.
"""

import sys
import getpass
import getopt
import os
from crypto.cipher.trolldoll import Trolldoll
from crypto.errors import DecryptNotBlockAlignedError
from binascii_plus import *


def main():
    """ Main is the command line interface to filecrypt """
    path, progName = os.path.split(sys.argv[0])
    usage = """Usage: %s [-d | -e][a][?] [-k <passPhrase>] [-i <infile>] [-o <outfile>]\n""" % progName
    try:
        # use get opt to parse and validate command line
        optlist, args = getopt.getopt(sys.argv[1:], 'edk:i:o:')
    except getopt.GetoptError as err:
        sys.exit("Error: %s\n%s" % (err, usage))
    print(optlist, '\n------\n', args)
    # make a dictionary and check for one occurance of each option
    optdict = {}
    for option in optlist:
        if option[0] not in optdict:
            optdict[option[0]] = option[1]
        else:
            sys.exit("Error: duplicate option '%s'\n%s" % (option[0], usage))

    if '-e' in optdict and '-d' in optdict:
        sys.exit("Error: Can not do both encrypt and decrypt, pick either '-e' or '-d'\n%s" % usage)
    if not ('-e' in optdict or '-d' in optdict):
        sys.exit("Error: Must select encrypt or decrypt, pick either '-e' or '-d'\n%s" % usage)

    # determine the passphrase from the command line or by keyboard input
    if '-k' in optdict:
        passPhrase = optdict['-k']
    else:
        passPhrase = getpass.getpass('Key: ')
    # should really test for a good passphrase  ...................

    # get input from file or stdin
    if '-i' in optdict:
        infile = open(optdict['-i'], 'rb')
        input = infile.read()
    else:
        input = sys.stdin.read()

    print("input (%d bytes): %s" % (len(input), b2a_pt(input)))
    alg = Trolldoll(ivSize=160)
    alg.setPassphrase(passPhrase)

    # Encrypt or decrypt depending on the option selected
    if '-e' in optdict:
        output = alg.encrypt(input)
    elif '-d' in optdict:
        try:
            output = alg.decrypt(input)
        except DecryptNotBlockAlignedError as errMessage:
            sys.exit("""Error: %s\n    Note this can be caused by inappropriate modification \n    of binary files (Win issue with CR/LFs).  Try -a mode. """ % errMessage)
        # should check for integrity failure
    else:
        sys.exit("Error: Must select encrypt or decrypt, pick either '-e' or '-d'\n%s" % usage)

    print("output (%d bytes): %s" % (len(output), b2a_pt(output)))
    # put output to file or stdout
    if '-o' in optdict:
        outfile = open(optdict['-o'], 'wb')
        outfile.write(output)
    else:
        sys.stdout.write(output)

    sys.exit()  # normal termination


if __name__ == "__main__":
    """ Called when run from the command line """
    main()
