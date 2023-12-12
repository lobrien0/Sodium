# Main
#
#   Author/s:       Luke O'Brien
#
#   Program Description:
#       The following will act as a settings file, and coordinate
#       the process of checking a shadow file for potential password
#       breaches

from Sodium import Shaker
from Sodium import Report
from Sodium.Shadow import shadow_pattern
import os, sys

##################################
#
#          Main Code
#
##################################

# Checks if all system arguments were set
if len(sys.argv) < 3:
    print("[X] Too few arguments")
    print(f'[i] Usage: python {sys.argv[0]} <shadow_file> <password_list>\n')
    sys.exit(1)

shadow_file:str = sys.argv[1]
passwd_file:str = sys.argv[2]

# Ensures file paths entered were Real
if not os.path.exists(shadow_file):
    raise FileNotFoundError(shadow_file)
if not os.path.exists(passwd_file):
    raise FileNotFoundError(passwd_file)

# imports user accounts into data-structure
all_accounts:list = Shaker.import_shadow(shadow_file)
secured_accounts:list = [x for x in all_accounts if x.protected()]

# Debugging: single user run
if len(sys.argv) == 4:
    print("\n[+] Entered: Debugging mode\n")
    single_user:str = sys.argv[3]
    usr_pattern = None
    check:bool = False
    # Searches for the user entered
    for x in secured_accounts:
        if x.name == single_user:
            check = True
            usr_pattern = x
            break
    # If the user wasn't found
    if not check:
        print(f'{single_user} Was not found in shadow file')
        exit(1)
    # Computes the hash
    __passwd:str = Shaker.compute_hash(usr_pattern, passwd_file)
    if len(__passwd) > 1:
        print(f'\nPassword for {single_user} found\n\t\tPass:\t{__passwd}')
    exit(0)
    
# Scans Each account for potentially compromised passwords
cracked_accounts:list = list()
for x in secured_accounts:
    cracked_passwd:str = Shaker.compute_hash(x, passwd_file)
    if cracked_passwd != None:
        cracked_accounts.append(f'{x.name}: {cracked_passwd}')
        
# Generates a Markdown report
if len(cracked_accounts) > 0:
    Report.generate_report(cracked_accounts)
else:
    print("There were no compromised accounts detected\nGood job!\n")