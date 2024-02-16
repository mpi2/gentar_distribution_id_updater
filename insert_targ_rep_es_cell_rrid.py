import json
import requests
import os
import sys

class Updater:

    def __init__(self):
        # Set service URL based on environment variable
        env = os.getenv('GENTAR_ENV', 'LOCAL')
        self.service = self.get_service_url(env)
        self.api = "api/"
        self.token = None
        self.obtain_token()
        self.targ_rep_es_cell_rr_ids = set()

    def get_service_url(self, env):
        # Define service URLs based on the environment
        if env == 'PRODUCTION':
            return "https://www.gentar.org/tracker-api/"
        elif env == 'SANDBOX':
            return "https://www.gentar.org/production-tracker-sandbox-api/"
        else:
            return "http://127.0.0.1:8080/"

    def read_targ_rep_es_cell(self, file):
        # Read targ_rep_es_celldata from a text file and store in a set
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

        if os.path.isfile(filepath):
            with open(filepath, 'rt') as targ_rep_es_cell_file:
                for line in targ_rep_es_cell_file:
                    # Split the line into words and take the first word as the targ_rep_es_cell
                    self.targ_rep_es_cell_rr_ids.add(line)

    def process_targ_rep_es_cell_rr_ids(self):
        # Process targ_rep_es_cell_rr_ids and update outcomes
        for targ_rep_es_cell_rr_id in self.targ_rep_es_cell_rr_ids:
            try:
                # Split the targ_rep_es_cell_rr_ids
                targ_rep_es_cell_request = targ_rep_es_cell_rr_id.split("\\t")
                print("Processing {}".format(targ_rep_es_cell_request))
                if len(targ_rep_es_cell_request) < 5:
                    sys.exit(
                        "column size must be 5 ")
                es_cell_name = targ_rep_es_cell_request[0]
                distributionNetworkName = targ_rep_es_cell_request[1]
                startDate = targ_rep_es_cell_request[2]
                endDate = targ_rep_es_cell_request[3]
                distributionIdentifier = targ_rep_es_cell_request[4]

                if distributionIdentifier.startswith("RRID:"):

                    # Fetch the outcome data
                    es_cell_update_url = self.service + self.api + "targ_rep/es_cell/distribution_product"
                    # Update the distributionIdentifier with the provided rr_id
                    es_cell_dto = {
                        "esCellName": es_cell_name,
                        "distributionNetworkName": distributionNetworkName,
                        "startDate": startDate,
                        "endDate": endDate,
                        "distributionIdentifier": distributionIdentifier
                    }

                    # Revise the outcome data on the GenTaR service
                    self.revise_service(es_cell_update_url, es_cell_dto)
                    print("Successfully Updated: {}".format(targ_rep_es_cell_request))
                else:
                    print("RRID is not in the correct format: {}".format(targ_rep_es_cell_request[4]))
            except ValueError:
                print("Format your file please. Broken line is {}".format(targ_rep_es_cell_request))
            except Exception as error:
                if hasattr(error, 'response') and error.response.text:
                    try:
                        response_data = error.response.text.encode('utf-8')
                        response_json = json.loads(response_data)
                        message = response_json['apierror']['message']
                        print("Message:", message)
                    except (json.JSONDecodeError, KeyError):
                        print("Unable to extract message from response.")
                else:
                    print("No response received or unable to extract message from response.")

    def obtain_token(self):
        # Obtain authentication token
        user = os.getenv('GENTAR_USER')
        password = os.getenv('GENTAR_PASSWORD')
        if user is None or password is None:
            sys.exit("Please export your GENTAR_USER and GENTAR_PASSWORD to the environment before running the script.")

        url = self.service + "auth/signin"
        headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'}
        credentials = {'userName': user, 'password': password}

        # Send a POST request to obtain the token
        r = requests.post(url, headers=headers, json=credentials)

        if r.status_code == 200:
            self.token = r.json()['accessToken']
        else:
            r.raise_for_status()

    def fetch_one_entry(self, url):
        # Fetch data from a given URL using the authentication token
        headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache',
                   'Authorization': 'Bearer ' + self.token}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

    def revise_service(self, url, data):

        # Revise data at a given URL using the authentication token
        headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache',
                   'Authorization': 'Bearer ' + self.token}
        r = requests.put(url, headers=headers, json=data)

        r.raise_for_status()
        return r.json(), r.status_code


if __name__ == '__main__':
    # Instantiate the Updater class
    updater = Updater()

    # Read targ_rep_es_cell data from the specified file
    updater.read_targ_rep_es_cell("targ_rep_es_cell_rr_ids.txt")

    # Process targ_rep_es_cell and update outcomes
    updater.process_targ_rep_es_cell_rr_ids()
