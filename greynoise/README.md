# GreyNoise

GreyNoise tells security analysts what not to worry about. We do this by curating data on IPs that saturate security 
tools with noise. This unique perspective helps analysts confidently ignore irrelevant or harmless activity, creating 
more time to uncover and investigate true threats. Includes tasks to allow IP enrichment and GNQL queries via 
the GreyNoise v2 API.

## Prerequisites

An API key for the GreyNoise API is required to use this integration.  If you don't have one, sign up for a free 
trial at [https://viz.greynoise.io/signup](https://viz.greynoise.io/signup)

## Capabilities

This plugin provides the following capabilities:

* Lookup IP in GreyNoise v2 Quick API
* Lookup IP in GreyNoise v2 Context API
* Lookup IP in GreyNoise v2 RIOT API
* Perform a GreyNoise Query (GNQL)
* Lookup GreyNoise Tag Details
* Get a list of all GreyNoise Tags

### Limitations

This integration was designed to work with the GreyNoise v2 API only.

## Asset Setup

Enter the GreyNoise API key in the Asset Configuration.  The test connection button will confirm the API key is valid 
and has a valid subscription associated with it.

## Tasks Setup
### Lookup IP in GreyNoise - Metadata mapping
By default, the "METADATA" portion of the Context API response is provided as a JSON object.
This section can be mapped to individual fields by using the JSONPATH output option, with the following JSONPATH:

```
$.metadata.asn
$.metadata.category
$.metadata.city
$.metadata.country
$.metadata.country_code
$.metadata.organization
$.metadata.os
$.metadata.rdns
$.metadata.region
$.metadata.tor
```

This can be applied to the GreyNoise Context Lookup and GreyNoise IP Lookup tasks.

### Using GreyNoise Query for Alerting
The GreyNoise Query Task can be used to create alerts for monitored IPs scheduling the task to run daily at a 
specified time, and outputting each result to a new record.

### Creating GreyNoise Visualizer Links
The Context, RIOT and Query tasks include a `viz_url` output that can be used to create a hyperlink to the GreyNoise
Visualizer.  To set this functionality up, create an output Template mapped to an RTF Field name "GN Visualizer URL"
and use the following value:

`<a target="_blank" href={{viz_url}}>View Details on the GreyNoise Visualizer</a>`

## Notes

* Additional content to support this integration can be found here: 
  [GrayNoise-Swimlane-Github-Repo](https://github.com/GreyNoise-Intelligence/greynoise-swimlane)
* For issues with this integration, please contact [hello@greynoise.io](mailto:hello@greynoise.io)

This plugin was last tested against product version: 10.2.2.
