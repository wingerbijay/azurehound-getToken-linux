# Entra ID Device Code Token Fetcher

A lightweight Python script to handle the Entra ID (Azure AD) Device Code flow while spoofing a Windows User-Agent. 

I wrote this because running tools like AzureHound or ROADrecon from a Linux machine often triggers Conditional Access Policies (CAPs) that block non-Windows platforms. If you try to use standard PowerShell scripts or curl commands to get your tokens, you'll just get hit with `invalid_grant` or conditional access blocks. 

This script handles the initial authentication request and the polling loop with a hardcoded Windows 11 Edge User-Agent. It allows you to bypass those basic OS restrictions, complete the MFA prompt in your browser, and dump a valid refresh token straight to your terminal.

## Requirements

You just need Python 3 and the `requests` library.

```bash
pip install requests
