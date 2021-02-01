#!/bin/env python3
# https://github.com/ServiceNowITOM/servicenow-ansible/blob/devel/plugins/modules/snow_record.py
# https://encoretechnologies.github.io/blog/2017/10/servicenow-automation/
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import json

DOCUMENTATION = r'''
---
module: snow_ci
short_description: Get, update, create CIs in ServiceNow CMDB.
version_added: "1.0.0"
description: I think you get the gist.
options:
    action:
        description: Whether to create, get, or update the CI.
        required: true
        type: str
    snow_url:
        description: Your ServiceNow URL. example: https://company.service-now.com
        required: true
        type: str
    table_name:
        description: The CMDB table we wish to use. example: cmdb_ci_linux_server
        required: true
        type: str
    payload:
        description: Information about CI for create and update actions.
        required: false
        type: str
    snow_username:
        description: ServiceNow username.
        required: true
        type: str
    snow_password:
        description: ServiceNow password.
        required: true
        type: str
    sys_id:
        description: The sys_id of the relevant CI. Only used for the update action.
        required: false
        type: str
    query:
        description: What to query for the get action. example: 'name=servername'
        required: false
        type: str
    validate_certs:
        description: Whether to validate certs.
        required: false
        type: bool







author:
    - Matt Cengic (@mcen1)
'''

def getCI(table_name,snow_url,sn_username,sn_password,query,validate_certs):
  # https://<instance>.service-now.com/api/now/table/incident?sysparm_query=company.stock_symbol=NYX
  url = "{0}/api/now/table/{1}?sysparm_query={2}".format(snow_url,table_name,query)

  headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

  result = requests.get(url,
                         headers=headers,
                         auth=(sn_username, sn_password),verify=validate_certs)

  return result.content.decode()

def createCI(table_name,snow_url,payload,sn_username,sn_password,validate_certs):
  url = "{0}/api/now/table/{1}".format(snow_url,table_name)
  headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
  result = requests.post(url,
                         json=payload,
                         headers=headers,
                         auth=(sn_username, sn_password),verify=validate_certs)

  return result.content.decode()

# sys_id is required to edit existing ci
def editCI(table_name,sys_id,snow_url,payload,sn_username,sn_password,validate_certs):
  url = "{0}/api/now/table/{1}/{2}".format(snow_url, table_name, sys_id)
  headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
  # example:
  #payload = {
  #          'install_status': 'Retired',
  #          'short_description': 'Change the install_status of this CI'
  #        }

  result = requests.patch(url,
                          json=payload,
                          headers=headers,
                          auth=(sn_username, sn_password),verify=validate_certs)
  return result.content.decode()



def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        action=dict(type='str', required=True),
        snow_url=dict(type='str', required=True),
        table_name=dict(type='str', required=True),
        payload=dict(type='str', required=False),
        sn_username=dict(type='str', required=True),
        sn_password=dict(type='str', required=True, no_log=True),
        sys_id=dict(type='str', required=False),
        query=dict(type='str', required=False),
        validate_certs=dict(type='bool', required=False, default=True),
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    myout={"error":"something horrible happened."}
    if module.params['action']=="create":
      myout=json.loads(createCI(module.params['table_name'],module.params['snow_url'],module.params['payload'],module.params['sn_username'],module.params['sn_password'],module.params['validate_certs']))
    elif module.params['action']=="get":
      myout=json.loads(getCI(module.params['table_name'],module.params['snow_url'],module.params['sn_username'],module.params['sn_password'],module.params['query'],module.params['validate_certs']))
    elif module.params['action']=="edit":
      myout=json.loads(editCI(module.params['table_name'],module.params['sys_id'],module.params['snow_url'],module.params['payload'],module.params['sn_username'],module.params['sn_password'],module.params['validate_certs']))
    else:
      raise Exception("action parameter not supported.")
    if module.check_mode:
        module.exit_json(**result)

    result['output']=myout
    if len(result['output'])==0 or "something horrible happened" in result['output']:
      result['failed'] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
