# pagerduty-api-dumper

```
usage: pagerduty_api_dumper.py [-h] -k KEY [-o OUTPUT] [-f]

Dump all available data having PagerDuty API key

optional arguments:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     PagerDuty API key
  -o OUTPUT, --output OUTPUT
                        Local directory to dump data
  -f, --full            Distinct API request for each item
```

Full mode could retrieve a bit more data, but will take much longer time.


## Example

```
$ ./pagerduty_api_dumper.py -k REDACTED
... abilities
... addons
... business_services
    [SNIP]
```
