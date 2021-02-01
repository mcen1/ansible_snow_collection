# Ansible Collection - mcen1.servicenow.snow_ci

Create, update, and get CMDB CIs in ServiceNow.

```
options:
    action:
        description: Whether to create, get, or update the CI.
        required: true
        type: str
    snow_url:
        description: Your ServiceNow URL. example: https://servicenow.company.com
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
```

Example:
```
  tasks:
    - name: Query SNOW for a cmdb_ci_linux_server CI named servername
      mcen1.servicenow.snow_ci:
        action: "get"
        snow_url: "https://servicenow.company.com"
        table_name: "cmdb_ci_linux_server"
        sn_username: "username"
        sn_password: "password"
        query: "name=servername"
      register: cioutput
```
