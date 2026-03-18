# Entra ID Device Code Token Fetcher

A lightweight Python script to handle the Entra ID (Azure AD) Device Code flow while spoofing a Windows User-Agent. 

I wrote this because running tools like AzureHound or ROADrecon from a Linux machine often triggers Conditional Access Policies (CAPs) that block non-Windows platforms. If you try to use standard PowerShell scripts or curl commands to get your tokens, you'll just get hit with `invalid_grant` or conditional access blocks. 

This script handles the initial authentication request and the polling loop with a hardcoded Windows 11 Edge User-Agent. It allows you to bypass those basic OS restrictions, complete the MFA prompt in your browser, and dump a valid refresh token straight to your terminal.

## Requirements

You just need Python 3 and the `requests` library.

```bash
pip install requests

Usage
Run the script from your terminal:

Bash
python3 get_token.py
The script will output a device code and a URL (https://login.microsoft.com/device).

Open that URL in your browser, enter the code, and log in to the target account. (Tip: Make sure your browser is also using a Windows User-Agent switcher extension just to be safe).

The script will automatically poll in the background. Once you finish the browser login, it will print your Refresh Token.

Feeding the Token to AzureHound
Once you have the refresh token, you can pass it directly into AzureHound using the -r flag to map out the tenant without triggering the OS block:

Bash
./azurehound -r "0.ARwA6Wg..." list --tenant "target-tenant.onmicrosoft.com" -o output.json
Disclaimer
Created for authorised lab testing and cybersecurity research purposes only.


***
roadrecon.db
azure_bloodhound_data.json
