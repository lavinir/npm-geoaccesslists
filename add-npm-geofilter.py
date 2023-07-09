from npmgeo import npmclient, dbip_client
import argparse
import ipaddress
import pandas as pd
import getpass

def csv_list(string):
    return string.split(',')

def ip_range_to_cidr(ip_start, ip_end):
    # Convert IP addresses to integers
    start = int(ipaddress.IPv4Address(ip_start))
    end = int(ipaddress.IPv4Address(ip_end))

    # Determine the common prefix length in bits
    mask = 0xffffffff ^ (start ^ end)
    prefix_length = 32 - (mask.bit_length() - 1)

    # Return the CIDR notation
    return f"{ip_start}/{prefix_length}"

parser = argparse.ArgumentParser(description='Add npm geofilter')
parser.add_argument('--npm-host', help='The npm host / ip to connect to', required=True)
parser.add_argument('--npm-port', help='The npm port admin port', required=False)
parser.add_argument('--npm-email', help='npm admin email address', required=False)
parser.add_argument('--npm-password', help='npm admin password', required=False)
parser.add_argument('--npm-accesslist-name', help='The name of the access list', required=True)
parser.add_argument('--allowed-countries', help='The list of allowed country codes',type=csv_list, required=True)
parser.add_argument('--ip-list-file', help='The file containing the ip list', required=False)

args = parser.parse_args()

npmclient.BASE_URL = args.npm_host
if args.npm_port is not None: npmclient.BASE_PORT = args.npm_port

# Get IP file data
if args.ip_list_file is None:
    print('Fetching ip list from db-ip.com')
    ip_file = dbip_client.fetch_ips()
else:
    ip_file = args.ip_list_file

#load ip file data
ip_df = pd.read_csv(ip_file, header=None, names=['start_ip', 'end_ip', 'country_code'])
filtered_entries = (ip_df[(ip_df['country_code'].str.lower().isin([c.lower() for c in args.allowed_countries])) & (ip_df['start_ip'].apply(lambda x: isinstance(ipaddress.ip_address(x), ipaddress.IPv4Address)))])
print(f'Found {len(filtered_entries)} entries for {args.allowed_countries}')

# create Access_Rule_Client list
access_rule_list = [npmclient.Access_Rule_Client(address=ip_range_to_cidr(row.start_ip, row.end_ip), directive='allow') for row in filtered_entries.itertuples(index=False)]

#Check if npm email and password are provided
if args.npm_email is None: args.npm_email = input('Enter npm email: ')
if args.npm_password is None: args.npm_password = getpass.getpass('Enter npm password: ')

#Get auth token
print('Getting auth token')
token = npmclient.get_auth_token(args.npm_email, args.npm_password)

#Getting existing access lists
existing_rule_id = npmclient.get_access_list_id(args.npm_accesslist_name, token)

#Add access list
print('Adding access list')
npmclient.add_access_list(args.npm_accesslist_name, token, existing_rule_id, *access_rule_list)


