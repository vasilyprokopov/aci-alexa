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
        message = 'Token received OK'
        return token, message
    else:
        errorCode = response.status_code
        errorMessage = response.json()['imdata'][0]['error']['attributes']['text']
        message = f'Error code: {errorCode}\n{errorMessage}'
        token = ''
        return token, message


def getHealth(apicUrl,token):
    # Function to get fabric health
    url = apicUrl+'/api/node/mo/topology/health.json'
    header = {'DevCookie': token}
    response = requests.get(url, headers=header, verify=False)
    
    if response.status_code == 200:
        health = response.json()['imdata'][0]['fabricHealthTotal']['attributes']['cur']
        message = f'Fabric health is {health} points out of 100.'
        return message
    else:
        errorCode = response.status_code
        errorMessage = response.json()['imdata'][0]['error']['attributes']['text']
        message = f'Error code: {errorCode}\n{errorMessage}'
        return message


def getControllers(apicUrl,token):
    # Function to get controller health
    url = apicUrl+'/api/node/class/infraWiNode.json'
    header = {'DevCookie': token}
    response = requests.get(url, headers=header, verify=False)
    
    if response.status_code == 200:
        message = ''
        for controller in response.json()['imdata']:
            nodeName = controller['infraWiNode']['attributes']['nodeName']
            operSt = controller['infraWiNode']['attributes']['operSt']
            health = controller['infraWiNode']['attributes']['health']
            message = message + f'Controller {nodeName} is {operSt} and {health}.\n'
        message = message + 'That\'s all your controllers.'
        return message
    else:
        errorCode = response.status_code
        errorMessage = response.json()['imdata'][0]['error']['attributes']['text']
        message = f'Error code: {errorCode}\n{errorMessage}'
        return message


def getNodes(apicUrl,token):
    # Function to get node health
    url = apicUrl+'/api/node/class/fabricNode.json'
    header = {'DevCookie': token}
    response = requests.get(url, headers=header, verify=False)

    if response.status_code == 200:
        message = ''
        
        for node in response.json()['imdata']:
            name = node['fabricNode']['attributes']['name']
            role = node['fabricNode']['attributes']['role']
            fabricSt = node['fabricNode']['attributes']['fabricSt']
            
            if not role == 'controller' and not fabricSt == 'active':
                message = message + f'Current operational status of {role} {name} is {fabricSt}.\n'
        
        if message == '':
            message = 'All leafs and spines are up and running.'
        else:
            message = message + 'All other nodes are OK.'
        
        return message
    else:
        errorCode = response.status_code
        errorMessage = response.json()['imdata'][0]['error']['attributes']['text']
        message = f'Error code: {errorCode}\n{errorMessage}'
        return message


token, message = aaaLogin(apicUrl, apicUser, apicPassword)
if token == '':
    print (message)
    quit()

message = getHealth(apicUrl,token)
print (message)
print ('----------')

message = getControllers(apicUrl,token)
print (message)
print ('----------')

message = getNodes(apicUrl,token)
print (message)
print ('----------')