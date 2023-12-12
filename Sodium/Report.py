# Report
#
#   Author/s:       Luke O'Brien
#
#   Program Description:
#       The following will generate a markdown report with data
#       passed from the calling program
import os

default_filepath:str = "final_report.md"
default_title:str = "Potentially Vulnerable Accounts"
default_desc:str = "The following report details accounts that have been processed and flagged as a potential risk to this organization. Bellow contains a list of flagged accounts"
default_dataTitle:str = "Flagged Accounts: Password"

def generate_report(_data:list, file_path:str=default_filepath, _title:str=default_title, _desc:str=default_desc, _data_title:str=default_dataTitle):
    if file_path[-3:] != '.md':
        index = file_path.rfind('.')
        if not index > 0:
            file_path += '.md'
    if os.path.exists(file_path):
        print("File Already Exists")
        raise FileExistsError
    
    with open(file_path, 'w') as file:
        file.write(f'# {_title}\n\n')
        file.write(f'{_desc}\n\n')
        file.write(f'## {_data_title}\n\n')
        
        for x in _data:
            file.write(f'- {x}  \n')
    print(f'Report Generated: {file_path}')