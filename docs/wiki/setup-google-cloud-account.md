# Set Up a Google Cloud Account


## Create a Google Account

Create an account at [Google Cloud](https://cloud.google.com).

When you have signed in, go to the [Getting Started](https://console.cloud.google.com/getting-started) page. Set your country and agree to the Terms of Service, then press "Agree and Continue".

You should be redirected to the Console Home screen.


## Set up Billing

To be able to access the resources required to create a Virtual Machine, we need to provide billing information, including credit card details. New accounts are given $300 credit to use for some cloud services, however we will need to upgrade to a paid account so that we can use GPUs for Elpis.

On the home screen, click "Billing" in the left hand navigation menu, then click "Add Billing Account". This will open a short, two-step form to provide credit card details and some address information. When this is complete, your account will be on a Free plan.

To use GPUs, we will need to upgrade the account to a paid service. Click the Billing menu item in the Nav menu, and click the "Upgrade" button, then "Activate". These steps seem to change often. For up-to-date information, check the Google documentation for [upgrading a free account](https://cloud.google.com/free/docs/free-cloud-features#to_upgrade_your_account). 


## Select APIs

The main resources we will use are Compute Engine Virtual Machines. To get access to Compute Engine we need to enable Compute Engine API, which provides access to the Compute Engine. Open the Navigation menu and click "Compute Engine", then "Enable".

This will take a few minutes to activate. 


## Increase Service Quotas 

To use GPUs we need to request an allocation. Open the Navigation menu and click the `IAM & Admin > Quotas` menu.

Filter the quota list by clicking the Filter button, select Quota, and type `GPUs (all regions)`. This should show you the `Compute Engine API` service. Tick the checkbox next to it and click the `Edit Quotas` button. Change the limit to 1 (or to match the number of VMs you want to run). Add a description for your request, for example "testing speech recognition systems". Provide contact details, and submit the request.

The request can take up to two days to be processed, but a small increase is likely to be quicker.
