import requests
import datetime
import gzip
import shutil

def fetch_ips():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m')
    filename = f"dbip-country-lite-{ts}.csv.gz"
    url = f'https://download.db-ip.com/free/{filename}'
    if (download_file(url, filename) == False):
        print (f'File not found for {ts}. Trying previous month')
        ts = (now - datetime.timedelta(days=now.day)).strftime('%Y-%m')
        filename = f"dbip-count-lite-{ts}.csv.gz"
        url = f'https://download.db-ip.com/free/dbip-country-lite-{ts}.csv.gz'
        if (download_file(url, filename) == False):
            print (f'File not found for {ts}.')
            return None
    return unzip(filename)

def download_file(url, filename):
    print(f'Downloading {url} to {filename}')
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f'Error downloading {url}. Status code: {response.status_code}')
        return False

def unzip(filename):
    extracted_file_name = filename[:-3]
    with gzip.open(filename, 'rb') as f_in:
        with open(extracted_file_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return extracted_file_name
