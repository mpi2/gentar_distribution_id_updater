
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
        self.colonies_and_rr_ids = set()

    def get_service_url(self, env):
        # Define service URLs based on the environment
        if env == 'PRODUCTION':
            return "https://www.gentar.org/tracker-api/"
        elif env == 'SANDBOX':
            return "https://www.gentar.org/production-tracker-sandbox-api/"
        else:
            return "http://127.0.0.1:8080/"

    def read_rr_ids_and_colony(self, file):
        # Read colony and rr_id data from a text file and store in a set
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

        if os.path.isfile(filepath):
            with open(filepath, 'rt') as colony_and_rr_id_file:
                for line in colony_and_rr_id_file:
                    # Split the line into words and take the first word as the colony_and_rr_id
                    self.colonies_and_rr_ids.add(line)

    def process_colonies(self):
        # Process colonies and update outcomes
        for colony_and_rr_id in self.colonies_and_rr_ids:
            try:
                # Split the colony_and_rr_id into colony and rr_id
                colony, rr_id = map(str.strip, colony_and_rr_id.split("\\t"))
                print("Processing {}".format(colony_and_rr_id))

                if rr_id.startswith("RRID:"):
                    # Fetch GenTaR plan data for the given colony
                    colony_data = self.fetch_gentar_plan(colony)

                    # Construct the URL for the outcome associated with the colony
                    tpo_url = self.service + "api/plans/{}/outcomes/{}".format(colony_data['pin'], colony_data['tpo'])

                    # Fetch the outcome data
                    outcome = self.fetch_one_entry(tpo_url)

                    # Update the distributionIdentifier with the provided rr_id
                    outcome["colony"]["distributionProducts"][0]["distributionIdentifier"] = rr_id

                    # Revise the outcome data on the GenTaR service
                    self.revise_service(tpo_url, outcome)
                    print("Updated: {}".format(colony_and_rr_id))
                else:
                    print("RRID is not in the correct format: {}".format(colony_and_rr_id))
            except ValueError:
                print("Format your file please. Broken line is {}".format(colony_and_rr_id))
            except Exception as error:
                print('Error: ', error)

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
        headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

    def revise_service(self, url, data):
        # Revise data at a given URL using the authentication token
        headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(url, headers=headers, json=data)
        r.raise_for_status()
        return r.json(), r.status_code

    def fetch_gentar_plan(self, colony_name):
        # Fetch GenTaR plan data for a given colony
        url = self.service + self.api + "colony?name=" + colony_name
        return self.fetch_one_entry(url)


if __name__ == '__main__':
    # Instantiate the Updater class
    updater = Updater()

    # Read colony and rr_id data from the specified file
    updater.read_rr_ids_and_colony("rr_ids.txt")

    # Process colonies and update outcomes
    updater.process_colonies()
