# Nginx Proxy Manager Geo-Location Based Access Rules 

This project allows running a python script that adds geo-location based access rules to Nginx Proxy Manager using free IP location data from [db-ip](https://db-ip.com/db/download/ip-to-country-lite) (their free data is updated monthly but is not as complete as the commercial version). The script loads IP location data from either a local CSV file or it can download from db-ip.com directly.

## Usage

```
python geo_access.py --npm-host <npm_host> --npm-port <npm_port> --npm-email <npm_email> --npm-password <npm_password> --npm-accesslist-name <npm_accesslist_name> --allowed-countries <allowed_countries> [--ip-list-file <ip_list_file>]
```

* `--npm-host`: The host or IP address of the Nginx Proxy Manager instance to connect to (required)
* `--npm-port`: The admin port of the Nginx Proxy Manager instance (required)
* `--npm-email`: The email address of an admin user in the Nginx Proxy Manager instance (required)
* `--npm-password`: The password of the admin user in the Nginx Proxy Manager instance (required)
* `--npm-accesslist-name`: The name of the access list to add the rules to (required)
* `--allowed-countries`: A comma-separated list of country codes to allow (required)
* `--ip-list-file`: The path to the CSV file containing the IP location data (optional, if not provided, data will be fetched from db-ip.com)

## Output

The script will output the number of filtered entries and a success message if the access rules were added successfully. Any errors encountered during the process will be printed to the console.