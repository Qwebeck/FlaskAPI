import argparse
import api
import sys
import requests
import json
from datetime import date,datetime
import subprocess
# from requests.exceptions import Timeout

try:
    requests = __import__('requests')
except ImportError:
    subprocess.check_call("pip install requests")
    requests = __import__('requests')

Timeout = requests.exceptions.Timeout

parser = argparse.ArgumentParser(description='Wrapper to works with api from command line')
parser.add_argument('-A','--addOne',nargs=1,default=None,help='''Command in format: -a FILENAME\n
                                                                               Add's all test examples from file''')


parser.add_argument('-R','--readable',action="store_true",help='If passed, convert timestamps from server output to human-readable format')


group3 = parser.add_mutually_exclusive_group()
group3.add_argument('-D','--deleteAll',action="store_true",help='''
                                                                Delete all records from database''')
group3.add_argument('-d','--deleteOne',nargs=1,type=int,help='''Command in format: -d TEST_ID\n
                                                                Delete test with specific id from server''')
group = parser.add_mutually_exclusive_group()
group.add_argument('-g','--getOne',nargs=1,type=int,default=None,help='''Command in format: -g TEST_ID\n
                                                                        Return test with specific id ''')
group.add_argument('-G','--getAll',action="store_true",help='Return all data from the server')

group2 = parser.add_mutually_exclusive_group()

group2.add_argument('-o','--output',nargs=1,type=str,default=['data_from_server'],help='''Command in format: -o FILENAME\n
                                                    File to store output''')
group2.add_argument('-a','--append',nargs=1,help='If given -- append data from server to existing file')

parser.add_argument('-H','--hostname',type=str,help='''Send requests to specified hostname.
                                                       Hostname should be in format:
                                                       http://some_address/
                                                       If argument not passed - default hostname is 
                                                       http://127.0.0.1:5000/
                                                       ''',
default='http://127.0.0.1:5000/')

def human_readable(input):
   
    for test in input:
        if test['timestamp']:
            test['timestamp'] = str(datetime.fromtimestamp(int(test['timestamp'])))
    return input

def save_data(data,args):
    output = data
    output_file_name = args.output[0]
    tsReplaced = False
    # Variable created to handle filenames  without .json extension 
    input_wrong_name = output_file_name.split('.')
    if args.append:
        try:
            output_file_name = args.append[0] 
            with open(output_file_name,'r') as file:
                content = json.load(file)
                content = content['data']
                tsReplaced = True
                for test in content:
    #To avoid looping two times:
    # 1. Here
    # 2. In function human_readable 
                    if args.readable and test['timestamp']:
                        test['timestamp'] = str(datetime.fromtimestamp(int(test['timestamp'])))
                    output.append(test)
                file.close()
        except IOError:
            dt_string = datetime.now().strftime("%H_%M_%S_%d")
            
            input_wrong_name = output_file_name.split('.')
            
            if len(input_wrong_name) != 1 and input_wrong_name[1] != '.json': 
                output_file_name = input_wrong_name[0] + '.json'
                print("No file found!\n Creating a new one with name ",output_file_name)
            
            elif output_file_name != 'data_from_server':
                input_wrong_name = output_file_name.split('.')
            
    
    elif len(input_wrong_name) != 1 and input_wrong_name[1] != '.json': 
        output_file_name = input_wrong_name[0] + '.json'
        print("No file found!\n Creating a new one with name ",output_file_name)
    else:
        dt_string = datetime.now().strftime("%H_%M_%S_%d")
        output_file_name +=  dt_string + '.json'
    if args.readable and not tsReplaced:
        output=human_readable(output)
    with open(output_file_name,'w') as  output_file:
        output ={"data":output}
        json.dump(output, output_file,indent=4)
        output_file.close()
    print("The data was added to the file: ", output_file_name)


def main():
    args = parser.parse_args()
    
    if args.getAll:
        request_url = args.hostname + 'getAll' 
        response = requests.get(request_url)
        if response.status_code == 200 and response.json()['message'] == 'ok':
            print('Success!')
            save_data(response.json()['data'],args)
        else :

            print(response.json()['message'])
        
    if args.addOne:
        input = args.addOne[0]
        request_url = args.hostname + 'addOne'
        
        try:
            with open(input) as file:
                data = json.load(file)
                if 'data' in data.keys():
                    try:
                        response = requests.post(request_url, json=data, timeout = 2 )
                        if response.status_code == 200:
                            print(response.json()['message'])
                        elif response.status_code == 500:
                            print('Server error !')
                    except Timeout:
                        print('The request timed out')
                else:
                    print('No data section specified in file')

        except IOError:
            print('File does not exist !')
    
    if args.getOne:
        request_url = args.hostname + 'getOne/:' + str(args.getOne[0]) 
        response = requests.get(request_url)
        if response.status_code == 200 and response.json()['message'] == 'ok':
            output = response.json()
            
            if args.readable:
             
                print("\n      \"timestamp\": {}, \n      \"value\": {}\n    ".format(datetime.fromtimestamp(int(output['data'][0]['timestamp'])),output['data'][0]['value']))

            save_data(output['data'],args)
        else:
            print(response.json()['message'])
    
    if args.deleteOne:
        request_url = args.hostname + 'deleteOne/:' + str(args.deleteOne[0]) 
        response = requests.delete(request_url)
        if response.status_code == 200:
            print(response.json()['message'])
            
        else:
            print(response.headers)
    
    if args.deleteAll:
        request_url = args.hostname + 'drop' 
        response = requests.delete(request_url)
        if response.status_code == 200:
            print(response.json()['message'])
            
        else:
            print('Error')

if __name__ == '__main__':
    main()