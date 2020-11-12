import urllib.request
import urllib.error
import socket
import json
import time

county_data = {
    "alameda": {"name": "Alameda", "population": 1671329},
    "alpine": {"name": "Alpine", "population": 1129},
    "amador": {"name": "Amador", "population": 39752},
    "butte": {"name": "Butte", "population": 219186},
    "calaveras": {"name": "Calaveras", "population": 45905},
    "colusa": {"name": "Colusa", "population": 21547},
    "contra-costa": {"name": "Contra Costa", "population": 1153526},
    "del-norte": {"name": "Del Norte", "population": 27812},
    "el-dorado": {"name": "El Dorado", "population": 192843},
    "fresno": {"name": "Fresno", "population": 999101},
    "glenn": {"name": "Glenn", "population": 28393},
    "humboldt": {"name": "Humboldt", "population": 135558},
    "imperial": {"name": "Imperial", "population": 181215},
    "inyo": {"name": "Inyo", "population": 18039},
    "kern": {"name": "Kern", "population": 900202},
    "kings": {"name": "Kings", "population": 152940},
    "lake": {"name": "Lake", "population": 64386},
    "lassen": {"name": "Lassen", "population": 30573},
    "los-angeles": {"name": "Los Angeles", "population": 10039107},
    "madera": {"name": "Madera", "population": 157327},
    "marin": {"name": "Marin", "population": 258826},
    "mariposa": {"name": "Mariposa", "population": 17203},
    "mendocino": {"name": "Mendocino", "population": 86749},
    "merced": {"name": "Merced", "population": 277680},
    "modoc": {"name": "Modoc", "population": 8841},
    "mono": {"name": "Mono", "population": 14444},
    "monterey": {"name": "Monterey", "population": 434061},
    "napa": {"name": "Napa", "population": 137744},
    "nevada": {"name": "Nevada", "population": 99755},
    "orange": {"name": "Orange", "population": 3175692},
    "placer": {"name": "Placer", "population": 398329},
    "plumas": {"name": "Plumas", "population": 18807},
    "riverside": {"name": "Riverside", "population": 2470546},
    "sacramento": {"name": "Sacramento", "population": 1552058},
    "san-benito": {"name": "San Benito", "population": 62808},
    "san-bernardino": {"name": "San Bernardino", "population": 2180085},
    "san-diego": {"name": "San Diego", "population": 3338330},
    "san-francisco": {"name": "San Francisco", "population": 881549},
    "san-joaquin": {"name": "San Joaquin", "population": 762148},
    "san-luis-obispo": {"name": "San Luis Obispo", "population": 283111},
    "san-mateo": {"name": "San Mateo", "population": 766573},
    "santa-barbara": {"name": "Santa Barbara", "population": 446499},
    "santa-clara": {"name": "Santa Clara", "population": 1927852},
    "santa-cruz": {"name": "Santa Cruz", "population": 273213},
    "shasta": {"name": "Shasta", "population": 180080},
    "sierra": {"name": "Sierra", "population": 3005},
    "siskiyou": {"name": "Siskiyou", "population": 43539},
    "solano": {"name": "Solano", "population": 447643},
    "sonoma": {"name": "Sonoma", "population": 494336},
    "stanislaus": {"name": "Stanislaus", "population": 550660},
    "sutter": {"name": "Sutter", "population": 96971},
    "tehama": {"name": "Tehama", "population": 65084},
    "trinity": {"name": "Trinity", "population": 12285},
    "tulare": {"name": "Tulare", "population": 466195},
    "tuolumne": {"name": "Tuolumne", "population": 54478},
    "ventura": {"name": "Ventura", "population": 846006},
    "yolo": {"name": "Yolo", "population": 220500},
    "yuba": {"name": "Yuba", "population": 78668},
}

ballot_measures = [
    {"number": 14, "name": "Bonds to Continue Stem Cell Research"},
    {"number": 15, "name": "Property Tax to Fund Schools, Government Services"},
    {"number": 16, "name": "Affirmative Action in Government Decisions"},
    {"number": 17, "name": "Restores Right to Vote After Prison Term"},
    {"number": 18, "name": "17-year-old Primary Voting Rights"},
    {"number": 19, "name": "Changes Certain Property Tax Rules"},
    {"number": 20, "name": "Parole Restrictions for Certain Offenses"},
    {"number": 21, "name": "Expands Governments’ Authority to Rent Control"},
    {"number": 22, "name": "App-Based Drivers and Employee Benefits"},
    {"number": 23, "name": "State Requirements for Kidney Dialysis Clinics"},
    {"number": 24, "name": "Amends Consumer Privacy Laws"},
    {"number": 25, "name": "Eliminates Money Bail System"},
]

presidential_candidates = [
    {"name": "Joseph R. Biden", "party": "Dem"},
    {"name": "Donald J. Trump", "party": "Rep"},
    {"name": "Roque \"Rocky\" De La Fuente Guerra", "party": "AI"},
    {"name": "Howie Hawkins", "party": "Grn"},
    {"name": "Jo Jorgensen", "party": "Lib"},
    {"name": "Gloria La Riva", "party": "P&F"},
]

def retry_if_timeout(func):
    def with_retry(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except (urllib.error.URLError, socket.timeout) as e:
                print(e)
    return with_retry

@retry_if_timeout
def get_json_resource(url):
    resp = urllib.request.urlopen(url, timeout=1)
    return json.load(resp)

def get_ballot_measure_results_for_county(county_name):
    print("getting ballot measure results for", county_name)
    results_url = "https://api.sos.ca.gov/returns/ballot-measures/county/{name}".format(name=county_name)
    print(results_url)
    results =  get_json_resource(results_url)
    ballot_measures = {}
    for ballot_measure in results["ballot-measures"]:
        ballot_measures["prop-{0}".format(ballot_measure["Number"])] = {
            "yes": int(ballot_measure["yesVotes"]),
            "no": int(ballot_measure["noVotes"]),
        }
    return ballot_measures


def get_presidential_candidate_results_for_county(county_name):
    print("getting presidential candidate results for", county_name)
    results_url = "https://api.sos.ca.gov/returns/president/county/{name}".format(name=county_name)
    print(results_url)
    results =  get_json_resource(results_url)
    presidential_candidate_results = {}
    for candidate in results[0]["candidates"]:
        presidential_candidate_results[candidate["Name"]] = int(candidate["Votes"].replace(",", ""))
    return presidential_candidate_results


for county_name, data in county_data.items():
    data["contests"] = get_ballot_measure_results_for_county(county_name)
    data["contests"]["president"] = get_presidential_candidate_results_for_county(county_name)

with open('counties.json', 'w') as fp:
    json.dump(county_data, fp, indent='  ')
