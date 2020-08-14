# importing the requests library
import requests
import json


key1 = '8611ac8b4c34ed96eb05fa14f3dfa78e'


# last "report"
def get_report(report_id):

    filename = f'../data/report_{report_id}.json'
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:

        # Port 443 actually redirects you to without it, but just gonna leave it in.
        url = f'https://www.warcraftlogs.com:443/v1/report/fights/{report_id}?api_key={key1}'

        r = requests.get(url=url)

        data = r.json()
        with open(filename, 'w') as outfile:
            json.dump(r.json(), outfile)

    return data

if __name__ == '__main__':

    report_id = '6vjRm3T7JHCnwWMB'

    data = get_report(report_id)

    print(data.keys())

    data['fights'][-1]['id']

    data_single = get_report(report_id + f"#fight={data['fights'][-1]['id']}")

    print(data_single.keys())





# api-endpoint
URL = f"https://www.warcraftlogs.com/v1/classes" + f'?api_key={key1}'

# defining a params dict for the parameters to be sent to the API
# PARAMS = {'address': location}
PARAMS = {}

# sending get request and saving the response as response object
r = requests.get(url=URL, params=PARAMS, auth=auth)

print(r.text)

# extracting data in json format
data = r.json()

print(data)
