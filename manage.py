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

def print_help_page():
    print(f'[i] Usage:\tpython {sys.argv[0]} <shadow_file> <password_list>\n')
    print(f'[d] Debugging')
    print(f'\tIn order to use the debugging command, you must add a 3rd argument with the name of the user you\'d like to compute')
    print(f'\n\tUsage:\n\t\tpython {sys.argv[0]} <shadow_file> <password_list> <user>')
    
    print()

##################################
#
#          Main Code
#
##################################

def main():
    
    # help list
    help_list:list = [ 'help', '--help', '-h' ]
    
    # Parses for help checking
    if len(sys.argv) == 2 and sys.argv[1].lower() in help_list:
        print_help_page()
        sys.exit(0)
    
    # Checks if all system arguments were set
    if len(sys.argv) < 3 or len(sys.argv) >= 5 :
        print("[X] Arguments failed to parse\n")
        print(f'[i] Usage:\tpython {sys.argv[0]} <shadow_file> <password_list>\n')
        sys.exit(-1)
        
    # Setting variables to passed args 
    shadow_file:str = sys.argv[1]
    passwd_file:str = sys.argv[2]
    selected_user:str = None
    if len(sys.argv) == 4:
        selected_user = sys.argv[3]
        print(f"[i] Selected User: {selected_user}\n")
        
    # Ensures file paths entered were Real
    if not os.path.exists(shadow_file):
        raise FileNotFoundError(shadow_file)
    if not os.path.exists(passwd_file):
        raise FileNotFoundError(passwd_file)

    # imports user accounts into data-structure
    all_accounts:list = Shaker.import_shadow(shadow_file)
    secured_accounts:list = [x for x in all_accounts if x.protected()]
    
    # Debugging logic
    if len(sys.argv) == 4:
        # Checks if user exists in shadow
        temp_list:list = list((x for x in secured_accounts if x.name == selected_user))
        if len(temp_list):
            cracked:str = Shaker.compute_hash(temp_list[0], passwd_file)
            temp:str = cracked if cracked != None else f"The account {selected_user} is not compromised"
            print(f"\n\t{temp}\n")
            sys.exit(0)
        else:
            print(f"\n[X] User not found in {shadow_file}")
            sys.exit(0)
            
        
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
        
if __name__ == "__main__":
    print()
    main()