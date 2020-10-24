#!/usr/bin/env python

# Copyright: (c) 2020, Vasily Prokopov (@vasilyprokopov)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# APIC credentials
apicUrl = 'https://sandboxapicdc.cisco.com'
apicUser = 'admin'
apicPassword = 'ciscopsdt'


def aaaLogin(apicUrl, apicUser, apicPassword):
    # Function to log into APIC and get a token (DevCookie)
    # Receives URL, username and password
    # Returnes token
    data = {
        "aaaUser": {
            "attributes": {
            "name": apicUser,
            "pwd": apicPassword
            }
        }
    }
    
    url = apicUrl+'/api/mo/aaaLogin.json'
    
    response = requests.post(url, json=data, verify=False)
    
    if response.status_code == 200:
        token = response.json()['imdata'][0]['aaaLogin']['attributes']['token']
        return token
    else:
        print ('Error code: ', response.status_code)
        print (response.json()['imdata'][0]['error']['attributes']['text'])
        quit()


def getHealth(apicUrl,token):
    # Function to get fabric health
    url = apicUrl+'/api/node/mo/topology/health.json'
    header = {'DevCookie': token}
    response = requests.get(url, headers=header, verify=False)
    
    if response.status_code == 200:
        health = response.json()['imdata'][0]['fabricHealthTotal']['attributes']['cur']
        return health
    else:
        print ('Error code: ', response.status_code)
        print (response.json()['imdata'][0]['error']['attributes']['text'])
        quit()


token = aaaLogin(apicUrl, apicUser, apicPassword)

health = getHealth(apicUrl,token)

print ('Fabric health:', health)
