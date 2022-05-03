# Unit test suggestion
import requests
from requests.auth import HTTPBasicAuth

# Making a get request
response = requests.get('{URL}',
                        auth=HTTPBasicAuth('username', 'password'))

# print request object
print(response)
