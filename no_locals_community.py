import json
import csv
import random
import json
import uuid
from random import uniform, sample
import pandas as pd


def get_zipcode_to_data():
    """ this functions reads in a json file which contains
                the netCost, the coordinates and the konzessioncost
                for all zipcodes in Germany.
                It returns the python dictionary zipcode_to_data and
                a list of the keys"""

    with open('zipcodes_to_specificData.json', 'r') as file:
        zipcode_to_data = json.load(file)

    keylist = []
    for k, v in zipcode_to_data.items():
        keylist.append(k)

    return zipcode_to_data, keylist


def get_no_local_distance_households():
    """ function that reads in the list of all households which
        dont have local distance and returns a list of those
        households"""

    # list for local distance pairs
    no_local_distance = []
    file = 'cleaned_kein_lokaler_Zusammenhang.csv'
    df = pd.read_csv(file, skipinitialspace=True)
    random_pairs = df.sample(n=150)

    for _, row in random_pairs.iterrows():
        no_local_distance.append((row[0], row[1]))

    return no_local_distance


def no_local_distance_households(no_local_distance):
    """ function that returns zipcodes for consumer
        and producer households from randomly choosed
        150 hoouseholds"""
    no_local_producer_Ids = []
    no_local_consumer_Ids = []

    for householdPair in no_local_distance:
        producerId = str(householdPair[0].item())
        consumerId = str(householdPair[1].item())
        no_local_producer_Ids.append(producerId)
        no_local_consumer_Ids.append(consumerId)

    return no_local_consumer_Ids, no_local_producer_Ids


def make_json_structure():
    """ this function creates a structure for the exported
                json file which is similar to the original BloGPV-data."""

    dummyData = {}
    dummyData['total_power_watt'] = None
    dummyData['total_power_watt_producers'] = None
    dummyData['total_power_watt_consumers'] = None
    dummyData['producers'] = []
    dummyData['consumers'] = []

    return dummyData


#-------------------add local pair househols-------------------------------------------------------

def create_no_local_consumer_households(no_local_consumer_Ids, dummyData, zipcode_to_data):
    """ function that adds consumer households to the community which
        don't have local distance to any other households within the community"""

    counter = 0
    while counter < len(no_local_consumer_Ids):
        consumer = {}
        # using uuid to generate random meterIds
        consumer['meterId'] = str(uuid.uuid4())
        consumer['power'] = round(uniform(0.0, 0.7),5)
        zipcode = no_local_consumer_Ids[counter]
        consumer['zipcode'] = zipcode


        consumer['netzentgelt'] = zipcode_to_data[zipcode]['netzentgelt']
        consumer['Konzessionsabgabe'] = zipcode_to_data[zipcode]['Konzessionsabgabe']
        consumer['coordinates'] = zipcode_to_data[zipcode]['coordinates']

        dummyData['consumers'].append(consumer)

        counter += 1

    return dummyData


def create_no_local_producers_households(no_local_producer_Ids, dummyData, zipcode_to_data):
    """ function that adds producer households to the community which
        don't have local distance to any other households within the community"""

    counter = 0
    while counter < len(no_local_producer_Ids):
        producer = {}
        producer['meterId'] = str(uuid.uuid4())
        producer['power'] = -round(uniform(0.0, 0.5),5)
        zipcode = no_local_producer_Ids[counter]

        producer['zipcode'] = zipcode
        producer['netzentgelt'] = zipcode_to_data[zipcode]['netzentgelt']
        producer['Konzessionsabgabe'] = zipcode_to_data[zipcode]['Konzessionsabgabe']
        producer['coordinates'] = zipcode_to_data[zipcode]['coordinates']
        dummyData['producers'].append(producer)
        counter += 1

    return dummyData


# --------------- header for json------------------------------------------------

def sum_up_total_power_watt_producers(dummyData):
    """ function that sums up the total produced power watt hours of
            all producers"""

    producer_watts = []
    for value in dummyData['producers']:
        producer_watts.append(value['power'])

    sum_producer_watts = sum(producer_watts)

    return sum_producer_watts


def sum_up_total_power_watt_consumers(dummyData):
    """ function that sums up the total consumer power watt hours of
            all consumers"""

    consumer_watts = []
    for value in dummyData['consumers']:
        consumer_watts.append(value['power'])

    sum_consumer_watts = sum(consumer_watts)

    return sum_consumer_watts


def sum_up_total_power_watts(dummyData):
    """ function that sums up the total amount of watts of all producer
            households and all consumer households"""

    totalWatts = []
    totalWatts.append(sum_up_total_power_watt_consumers(dummyData))
    totalWatts.append(sum_up_total_power_watt_producers(dummyData))

    sum_totalWatts = sum(totalWatts)

    return sum_totalWatts


def main():
    # get specific data to zipcodes
    zipcode_to_data, keylist = get_zipcode_to_data()

    print("step 1")

    #get pairs without local distance
    no_local_distance = get_no_local_distance_households()

    print("step 2")
    no_local_consumer_Ids, no_local_producer_Ids = no_local_distance_households(no_local_distance)

    print(len(no_local_producer_Ids))
    print(len(no_local_consumer_Ids))

    # create dictionary
    dummyData = make_json_structure()
    print("step 3")
    # add local distance consumers
    dummyData = create_no_local_consumer_households(no_local_consumer_Ids, dummyData, zipcode_to_data)
    print("step 4")
    # add local distance producers
    dummyData = create_no_local_producers_households(no_local_producer_Ids, dummyData, zipcode_to_data)

    print("step 5")
    # calculate for header
    dummyData['total_power_watt_producers'] = sum_up_total_power_watt_producers(dummyData)
    dummyData['total_power_watt_consumers'] = sum_up_total_power_watt_consumers(dummyData)
    dummyData['total_power_watt'] = sum_up_total_power_watts(dummyData)

    # --------------dumping file -----------------------------------
    with open('150_no_locals_community.json', 'w') as file:
        json.dump(dummyData, file)


if __name__ == '__main__':
    main()