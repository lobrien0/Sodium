# Sodium Checker
#
#   Author/s:       Luke O'Brien
#
#   Program Description:
#       The following contains functions that are designed to process and
#       audit salted unix-style hashes using all available resources
#
#       - Load a password file
#       - Print out a loading bar to terminal
#       - check a 'shadow_pattern' against a password list(list)
#       - A function to multi-process the hash checking 

import crypt, math, multiprocessing, time, threading, sys, os
from Sodium.Shadow import shadow_pattern

""" Print Loading Bar
        Will print out a dynamic loading bar in the terminal
"""
def print_loading_bar(iteration, total, bar_length=50):
    progress = iteration / total
    arrow = '=' * int(round(bar_length * progress))
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f'\r[{arrow + spaces}] {int(progress * 100)}%')
    sys.stdout.flush()
    
""" Parse Shadow
        Taking a raw shadow file generated by a unix,
        the following will split the lines and parse out
        the entire shadow entry into n 'shadow_pattern' 
        before storing it in a list
    Returns:
        list(obj:shadow_pattern)
"""
def import_shadow(shadow_file:str):
    shadow_list:list = list()
    account_list:list = list()
    
    # If the file exists, import shadow by line
    if os.path.exists(shadow_file):
        with open(shadow_file, 'r') as file:
            for x in file:
                # Only parses Non-empty or non-cemented lines
                if x != '\n' and x[0] != '#':
                    shadow_list.append(x[:-1])
    else:
        raise FileNotFoundError
    
    for x in shadow_list:
        account_list.append(shadow_pattern(x))
    return account_list

""" Import Password File
        Taking in a filepath, will process a file and import
        each password into a list.
        
    Returns:
        list -> passwords
"""
def import_passwd(file_path:str) -> list:
    pass_list:list = list()
    
    # Checks if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError
    
    # Checks if the file is too large
    if os.stat(file_path).st_size >= 1000000000:
        raise Exception("File too Large")
    
    # Imports each password by line
    with open(file_path, 'r') as file:
        for x in file:
            if x != "\n" and '\n' in x:
                pass_list.append(x[:-1])
            elif x != "\n":
                pass_list.append(x)
    return pass_list


""" Compute Hash
        multi-processes checking a shadow pattern against a pass_list.
        Based on your systems resources, splitting resources evenly.
        The passList will be split and passed accordingly.
        Uses all logical processors except for 1 (if there is 2 or more)
"""
def compute_hash(pattern:shadow_pattern, file_path:str) -> str:
    # Sets maximum processes based on system, defines list to hold processes, and Queue for results
    thread_limit:int = int(multiprocessing.cpu_count()-1)
    if thread_limit == 0:
        thread_limit = 1
    result_queue = multiprocessing.Queue()
    myThreads:list = list()
    
    # Reads in Password list
    pass_list:list = import_passwd(file_path)
    
    # These calculate how to split up the list of passwords between the processes
    list_length:int = len(pass_list)
    list_quantum:int = math.floor(list_length/thread_limit)
    
    # Generates each process for each of the logicalProcessors
    #   Splits up the PassList so each process has its own sublist
    #   Sets the target function to "check_user", which does the hash
    #   processing
    for x in range(1,thread_limit+1):
        if x == thread_limit:
            myThreads.append(multiprocessing.Process(target=check_user, args=(pattern, pass_list[((x-1)*list_quantum):], result_queue)))
        else:
            myThreads.append(multiprocessing.Process(target=check_user, args=(pattern, pass_list[((x-1)*list_quantum):((x)*list_quantum)], result_queue)))
            
    # Runs all the generated processes simultaneously
    print(f'There are {len(myThreads)} Threads being used for processing')
    print(f'Processing User: {pattern.name}...')
    for x in myThreads:
        x.start()
    
    # As the processes run, it will check to see if one has finished
    #   if it has, then it will end all other processes
    finished:bool = False
    while not finished:
        for x in myThreads:
            if not x.is_alive():
                finished = True
                for y in myThreads:
                    if y.is_alive():
                        y.terminate()
                break
        time.sleep(1)
    
    # Returns if account is compromised or not
    if result_queue.qsize() > 0:
        hash_result:str = result_queue.get()
        return hash_result
    return None

""" Check User
        A function built to audit a salted hash, taking a shadow_pattern and a 
        password list(list), comparing hashes to matches.
        - Function is standalone
        - Function be be threaded or multiprocessed
    
    Returns:
        String -> Matched Password (raw text)
"""
def check_user(pattern:shadow_pattern, pass_list:list, result_queue=None) -> str:
    # Defines variables and constants to be used
    search_pattern:str = pattern.get()
    search_result:str = None
    list_len = len(pass_list)
    
    # Steps through each password in PassList, if the saltedHash of said password matches pattern
    for x in range(list_len):
        # Creates hash
        new_hash:str = str(crypt.crypt(pass_list[x], f'${pattern.hash_type}${pattern.salt}'))
        
        # Checks Hash and updates loading bar
        if new_hash == search_pattern:
            search_result = str(pass_list[x])
            threading.Thread(target=print_loading_bar, args=(list_len, list_len)).start()
            break
        elif x % 500 == 0:
            threading.Thread(target=print_loading_bar, args=(x, list_len)).start()
        elif x == list_len-1:
            threading.Thread(target=print_loading_bar, args=(list_len, list_len)).start()
    time.sleep(0.005)
    print("\n")
    
    # Returns the result depending how the function was called
    if result_queue != None and search_result != None :
        result_queue.put(search_result)
    elif search_result != None:
        return search_result