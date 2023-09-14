# CHANGELOG

## 1.2.0 - 2021-12-09

* Added cap to raw_data output to limit 1000 items per subsection
* Added support for RIOT Trust Levels
* Changed classification on RIOT IPs to "RIOT" instead of "benign"
* Updated GreyNoise SDK to version 1.1.0  
* Product version tested against: GreyNoise v2 APIs

## 1.1.0 - 2021-05-24

* Added Support for GreyNoise Community (Free) API Lookups
* Product version tested against: 10.2.2

## 1.0.1 - 2021-05-05

* Fixed Bug in IP Lookup where multiple outputs were provided
* Fixed Bug in IP Lookup where no classification was provided for RIOT only IPs
* Update outputs on Context and IP Lookup to include BOT output
* Fixed issue where GNQL was providing blank records when used for alerting with no returned output

## 1.0.0 - 2021-02-25

* Initial Release
* Product version tested against: 10.2.2