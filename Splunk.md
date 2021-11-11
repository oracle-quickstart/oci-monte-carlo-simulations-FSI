## Monitoring

### Access your Splunk Management GUI
You can reach the Splunk Management GUI: *loadbalancer_externalip:8000*

Credentials: *admin/password*

#### Create the Splunk dashboard
Access to the URL: *loadbalancer_externalip:8000/en-US/app/search/search* and select *Dashboard* page:
![](https://github.com/oracle-quickstart/oci-monte-carlo-simulations-FSI/blob/main/images/splunk_dashboards.png)

Select *Create New Dashboard* and set the configuration (this configuration will be overwrited in the next step):
![](https://github.com/oracle-quickstart/oci-monte-carlo-simulations-FSI/blob/main/images/splunk_createdashboard.png)

Select *Edit* on your dashboard, replace the *Source* content with the XML file: [Splunk XML Dashboard](splunk/FSI_dashboard.xml), and save.
![](https://github.com/oracle-quickstart/oci-monte-carlo-simulations-FSI/blob/main/images/splunk_replaceXML.png)

Data is going to be automatically loaded when executions take place.
