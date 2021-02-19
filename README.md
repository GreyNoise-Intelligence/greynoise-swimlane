[![main](https://github.com/GreyNoise-Intelligence/greynoise-swimlane/workflows/Build/badge.svg)](https://github.com/GreyNoise-Intelligence/greynoise-swimlane/actions?query=workflow%3ABuild)
[![main](https://github.com/GreyNoise-Intelligence/greynoise-swimlane/workflows/python_linters/badge.svg)](https://github.com/GreyNoise-Intelligence/greynoise-swimlane/actions?query=workflow%3Apython_linters)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# GreyNoise Swimlane Integration

The GreyNoise Swimlane Integration is a set of tasks can be used in the Swimlane platform.

More details about Siemplify here: [https://www.swimlane.com/](https://www.swimlane.com/)

### Initial Configuration
In order to use the GreyNoise Integration for Swimlane, download the integration from 
[Swimlane AppHub](https://apphub.swimlane.com) and upload the plugin to the system under Integrations -> Plugins.

Then, configure a GreyNoise Asset from Integrations -> Assets by entering a GreyNoise API key and using the `Test
Connection` button to validate it is working.

If you don't have a GreyNoise API key, you can sign up for a free trial at 
[https://viz.greynoise.io/signup](https://viz.greynoise.io/signup)

### Tasks

The GreyNoise Tasks allow for IPs to be looked up in the different GreyNoise API endpoints and for a more complex 
GNQL query to be executed as part of a Case workflow.

#### Quick IP Lookup
The Quick IP Lookup action is designed to take all Address entities associated with a case/alert and enrich them against
the GreyNoise Quick API.

#### Context IP Lookup
The Context IP Lookup action is designed to take all Address entities associated with a case/alert and enrich them 
against the GreyNoise Context API.  It also provides an Insight on the Case for each IP entity that is found.

#### RIOT IP Lookup
The RIOT IP Lookup action is designed to take all Address entities associated with a case/alert and enrich them against
the GreyNoise RIOT API.  It also provides an Insight on the Case for each IP entity that is found.

#### IP Lookup
Uses the above endpoints to do a combination lookup following the flow: RIOT -> Quick -> Context and provides the 
appropriate output based on where the IP was located

#### Execute GNQL Query
The Execute GNQL Query action is designed to perform a GNQL query against the GreyNoise query endpoint and return all
matching records, up to the supplied limit (default is 10 results).

### Alerting

The GreyNoise GNQL Query task with a defined trigger can be used to generate alerts from the GreyNoise data.

It is primarily designed to be an alerting system for when GreyNoise
begins observing mass-internet scanning activity of a monitored IP.  The primary use case is to query daily for a CIDR
block, using a query similar to: `ip:85.32.32.0/24 last_seen:1d`

Using a query similar to the above, this would generate an alert for an IP in the provided range if GreyNoise observes
the IP performing mass-internet scanning.

To configure this, create a `GreyNoise Alerts` application in Swimlane, then add a `GreyNoise Query` task that is 
triggered to run once per day with the defined GNQL.  The output of the task should use the Create New Record option
to create a new record for each IP returned from the query.  These can then be triages as part of any standard alerting
workflow

 ## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting 
pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the 
[tags on this repository](https://github.com/GreyNoise-Intelligence/os-template/tags).

## Authors

* **Brad Chiappetta** - *Initial work* - [bradchiappetta](https://github.com/bradchiappetta)

See also the list of [contributors](https://github.com/GreyNoise-Intelligence/os-template/contributors) 
who participated in this project.

## Acknowledgments

* Thank you to the Swimlane Content team for their assistance in developing and testing this integration.

## Links

* [GreyNoise.io](https://greynoise.io)
* [GreyNoise Terms](https://greynoise.io/terms)
* [GreyNoise Developer Portal](https://developer.greynoise.io)

## Contact Us

Have any questions or comments about GreyNoise?  Contact us at [hello@greynoise.io](mailto:hello@greynoise.io)

## Copyright and License

Code released under [MIT License](LICENSE).

