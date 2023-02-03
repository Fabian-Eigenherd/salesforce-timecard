import click
import keyring
from subprocess import Popen, PIPE
import distutils.spawn
import json
from simple_salesforce.exceptions import SalesforceExpiredSession, SalesforceError, SalesforceAuthenticationFailed


def manual_refresh():
    username = click.prompt('Please enter your salesforce username', type=str)
    access_token = click.prompt("Insert your Saleforce Access_Token", prompt_suffix=': ', hide_input=True, show_default=False, type=str)
    click.echo()
    keyring.set_password("salesforce_cli", f"{username}_access_token", access_token)
    
def sfdx_token_refresh(instance):
    instanceURL = f"https://{instance}"
    sfdx_webauth_process = Popen([distutils.spawn.find_executable("sfdx"), 'auth:web:login', "-r", instanceURL], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
    sfdx_process = Popen([distutils.spawn.find_executable("sfdx"), 'force:org:display', '--json', '--targetusername', 'dedwards@bishopfox.com' ], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    cmd_output, cmd_error = sfdx_process.communicate() 
    sfdx_results = json.loads(cmd_output.decode("utf-8")) 
    
    try:
        username = sfdx_results['result']['username']
        access_token = sfdx_results['result']['accessToken']
    except Exception as e:
        print(e)
        print(cmd_error)
    return(username,access_token)


