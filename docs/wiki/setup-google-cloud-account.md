# Set up a Google Cloud account


## Create a Google account

Create an account at [Google Cloud](https://cloud.google.com).

When you have signed in, go to the [Getting Started](https://console.cloud.google.com/getting-started) page. Set your country and agree to the Terms of Service, then press "Agree and Continue".

You should be redirected to the Console Home screen.


## Set up billing

To be able to access the resources required to create a virtual machine, we need to provide billing information including credit card details. New accounts are given $300 credit to use for some cloud services, however to use GPUs requires a paid account.

On the home screen, click "Billing" in the left hand navigation menu, then click "Add Billing Account". This will open a short, two-step form to provide credit card details and some address information.  

To use GPUs, we will need to upgrade the account to a paid service. Click the Billing menu item in the Nav menu, and click the "Upgrade" button, then "Activate".


## Create a project and select APIs

The main resources we will use are Compute Engine Virtual Machines. To get access to Compute Engine we need to enable Compute Engine API, which is a code library that provides access to the Compute Engine. Open the Navigation menu and click "Compute Engine", then "Enable".

This will take a few minutes to activate. 


## Increase service quotas 

To use GPUs we need to request an allocation. Open the Navigation menu and click the `IAM & Admin > Quotas` menu.

Filter the quota list by clicking the Filter button, select Quota, and type `GPUs (all regions)`. This should show you the `Compute Engine API` service. Tick the checkbox next to it and click the "Edit Quotas" button. Change the limit to 1 (or to match the number of VMs you want to run). Add a description for your request, for example "testing speech recognition systems". Provide contact details, and submit the request.

The request can take up to two days to be processed. 


## Add a server

To add a server to the project, open the left side Navigation Menu and select "Compute Engine". Then select "VM Instances". If this is the first time your Google account has used Cloud Platform you may be offered a free trial! If so, go through the process of signing up for it. Otherwise, you may need to add billing details to access VM instances (TODO add more info about that). You will need to enter credit card details during the free trial opt-in process, but you won't be billed unless you turn on Automatic Billing.

