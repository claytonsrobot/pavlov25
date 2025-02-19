'''
```
```
'''

#C:\Users\user\Documents\clayton-personal-markdown


'''# Query:
Warning: get rid of hastag "#" marks in this message, and then answer the question: 
# Query: # Design a tool for me to talk to MS Fabric with Python scripting. Please #deliver in the format of the attached Python script, which can be launched as #a command line interface, with functions and arguments in the terminal #allowing for easy user interaction on a local installation of the software.
'''

# Microsoft Co-Pilot:
import argparse
import requests

def get_data(endpoint, params=None):
    """Fetch data from MS Fabric endpoint."""
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def post_data(endpoint, data):
    """Send data to MS Fabric endpoint."""
    response = requests.post(endpoint, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def main():
    parser = argparse.ArgumentParser(description='MS Fabric Command Line Interface Tool')
    parser.add_argument('action', choices=['get', 'post'], help='Action to perform: get or post')
    parser.add_argument('--endpoint', required=True, help='MS Fabric API endpoint')
    parser.add_argument('--params', nargs='*', help='Parameters for GET request')
    parser.add_argument('--data', nargs='*', help='Data for POST request in key=value format')

    args = parser.parse_args()

    if args.action == 'get':
        params = {k: v for k, v in (x.split('=') for x in args.params)} if args.params else None
        data = get_data(args.endpoint, params)
        print(data)
    elif args.action == 'post':
        data = {k: v for k, v in (x.split('=') for x in args.data)} if args.data else {}
        response = post_data(args.endpoint, data)
        print(response)

if __name__ == "__main__":
    main()
'''#This script provides a basic CLI tool for interacting with MS Fabric. 
You can 
#perform `GET` and `POST` requests by specifying the endpoint and any necessary
#parameters or data. Adjust the script as needed to fit your specific use case.
#Let me know if you need any further assistance or additional features!
'''