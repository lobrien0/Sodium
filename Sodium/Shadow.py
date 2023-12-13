# Shadow
#
#   Author/s:       Luke O'Brien
#
#   Program Description:
#       Defines the "shadow_pattern" class, which can hold any 
#       shadow entry from a shadow file in Unix-systems.
#       Additionally parses out hashes to respective parts

import datetime

class shadow_pattern:
    def __init__(self, line:str=None):
        # Username
        self.name:str = None
        
        # Hash
        #pass_hash.index('$', 4)
        self.hash_type:str = None #pass_hash[1]
        self.salt:str = None #pass_hash[3:salt_index]
        self.hash:str = None #pass_hash[salt_index+1:]
        
        # Last Password Change (last Changed)(Unix Time)
        self.last_changed:int = None
        
        # Minimum days before Password change
        self.pass_min:int = None
        
        # Maximum days before Password change
        self.pass_max:int = None
        
        # Days until Password warning
        self.pass_warn:int = None
        
        # Days until account expiries after password has expired
        self.pass_inactive:int = None
        
        # Date of expirations (Unix Time)
        self.date_expire:int = None
        
        if line != None: 
            if self.parse(line):
                print(f'[X] Parse Failed on {self.name}. Skipping...\n')
        
    
    # Parser
    def parse(self, line:str) -> int:
        # splitting text by ":"
        temp_list:list = line.split(':')
        self.name = temp_list[0]
        
        # If there is a hash
        hash:str = temp_list[1]
        
        # Parses and sets the Hash values
        if len(hash) >= 6:
            
            # Checks to ensure YesCrypt is not used
            if hash[1] in ['Y', 'y']:
                return -1
            
            salt_index = hash.index('$', 3)
            self.hash_type = hash[1]
            self.salt = hash[3:salt_index]
            self.hash = hash[salt_index+1:]
        
        # if Setting exists, print it
        if len(temp_list[2]) > 0:
            self.last_changed = int(temp_list[2])
        if len(temp_list[3]) > 0:
            self.pass_min = int(temp_list[3])
        if len(temp_list[4]) > 0:
            self.pass_max = int(temp_list[4])
        if len(temp_list[5]) > 0:
            self.pass_warn = int(temp_list[5])
        if len(temp_list[6]) > 0:
            self.pass_inactive = int(temp_list[6])
        if len(temp_list[7]) > 0:
            self.date_expire = int(temp_list[7])
            
        return 0
    
    # Getter function
    def get(self) -> str:
        return f'${self.hash_type}${self.salt}${self.hash}'
    
    # Returns true if account is password protected
    def protected(self) -> bool:
        if self.hash != None:
            return True
        return False
    
    """ Compare
            Checks each value of the salt-hash combo, only
            returning true if all match
        Returns:
            bool
    """
    def compare(self, __type:str, __salt:str, __hash:str) -> bool:
        type_bool:bool = (self.hash_type == __type)
        salt_bool:bool = (self.salt == __salt)
        hash_bool:bool = (self.hash == __hash)
        return type_bool and salt_bool and hash_bool
    
    # Prints out the data stored
    def __str__(self):
        time_offset = datetime.date(1970,1,1)
        final_str:str = str()
        crypt_type:dict = {'1': 'MD5', '2a': 'BLOWFISH', '5': 'SHA-256', '6': 'SHA-512'}
        final_str += f'#{self.name}:\n'
        
        if self.hash != None:
            final_str += f'\tHash Type:\t{crypt_type[self.hash_type]}\n'
            final_str += f'\tHash Salt:\t{self.salt}\n'
            final_str += f'\tHash:\t\t{self.hash}\n'
            
        if self.last_changed != None:
            final_str += f'\tLastChanged:\t{datetime.timedelta(self.last_changed) + time_offset}\n'
        if self.pass_min != None and self.pass_min != 0:
            final_str += f'\tPasswd Min:\t{datetime.timedelta(self.pass_min) + datetime.timedelta(self.last_changed) + time_offset}\n'
        if self.pass_max != None and self.pass_max != 99999:
            final_str += f'\tPasswd Expire:\t{datetime.timedelta(self.pass_max) + datetime.timedelta(self.last_changed) + time_offset}\n'
        if self.pass_warn != None and self.pass_max != 99999:
            final_str += f'\tPasswd Warn:\t{datetime.timedelta(self.pass_warn) + datetime.timedelta(self.last_changed) + time_offset}\n'
        if self.pass_inactive != None:
            final_str += f'\tInactive Exp:\t{datetime.timedelta(self.pass_inactive) + datetime.timedelta(self.pass_max) + datetime.timedelta(self.last_changed) + time_offset}\n'
        if self.date_expire != None:
            final_str += f'\tAccount Exp:\t{datetime.timedelta(self.date_expire) + time_offset}\n'
            
        return final_str
    
    # Defines how to check password similarity
    def __eq__(self, other) -> bool:
        if isinstance(other, shadow_pattern):
            return self.get() == other.get()
        return False