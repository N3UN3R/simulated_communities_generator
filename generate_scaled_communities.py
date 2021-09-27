import csv
# importing random module
import random
import json
import uuid
from random import uniform, sample


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


def get_local_pairs():
    """ function that reads in csv file lokalerZusammenhang.csv
        which contains all householdpairs with a distance lower
        than 4.5 kilometers"""

    # list for local distance pairs
    localDistance = []
    with open('cleaned_lokaler_Zusammenhang.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # first value in csv is emtpy
            if len(row) > 0:
                localDistance.append(row)

    return localDistance


def local_distance_households(localDistance):
    """ function that selects an optional number of households
        with local distance and returns the meter ids of those
        households as lists local_consumer_Ids and local_producer_Ids"""

    random_selected = sample(localDistance, 250)
    local_producer_Ids = []
    local_consumer_Ids = []

    for householdPair in random_selected:
        producerId = householdPair[0]
        consumerId = householdPair[1]
        local_producer_Ids.append(producerId)
        local_consumer_Ids.append(consumerId)

    return local_consumer_Ids, local_producer_Ids


def clean_keyList(local_consumer_Ids, local_producer_Ids, keylist):
    """ this function removes all local distance households from
        keylist"""

    test = local_producer_Ids + local_consumer_Ids
    cleaned_keyList = []
    for zipcode in keylist:
        if zipcode not in test:
            cleaned_keyList.append(zipcode)

    return cleaned_keyList, test


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

def create_local_consumer_households(local_consumer_Ids, dummyData, zipcode_to_data):
    """ this function adds consumer households to the simulated
            community that have local distance to other households in
            the simulated community.
            It returns the python dictionary dummyData"""

    counter = 0
    while counter < len(local_consumer_Ids):
        consumer = {}
        # using uuid to generate random meterIds
        consumer['meterId'] = str(uuid.uuid4())
        consumer['power'] = round(uniform(0.0, 0.7),5)
        zipcode = local_consumer_Ids[counter]
        consumer['zipcode'] = zipcode
        consumer['netzentgelt'] = zipcode_to_data[zipcode]['netzentgelt']
        consumer['Konzessionsabgabe'] = zipcode_to_data[zipcode]['Konzessionsabgabe']
        consumer['coordinates'] = zipcode_to_data[zipcode]['coordinates']
        dummyData['consumers'].append(consumer)

        counter += 1

    return dummyData


def create_local_producers_households(local_producer_Ids, dummyData, zipcode_to_data):
    """ this function adds producer households to the simulated
                community that have local distance to other households in
                the simulated community.
                It returns the python dictionary dummyData"""

    counter = 0
    while counter < len(local_producer_Ids):
        producer = {}
        producer['meterId'] = str(uuid.uuid4())
        producer['power'] = -round(uniform(0.0, 2.5),5)
        zipcode = local_producer_Ids[counter]
        producer['zipcode'] = zipcode
        producer['netzentgelt'] = zipcode_to_data[zipcode]['netzentgelt']
        producer['Konzessionsabgabe'] = zipcode_to_data[zipcode]['Konzessionsabgabe']
        producer['coordinates'] = zipcode_to_data[zipcode]['coordinates']
        dummyData['producers'].append(producer)

        counter += 1

    return dummyData


#--------------------------add generated households--------------------------------------

def create_random_consumers(cleaned_keyList, zipcode_to_data,dummyData):
    """ This function creates random consumer households.
        The number after counter could be used to decide how many
        consumers should be generated.
        keep in mind that there are already local distance households"""

    counter = 0
    while counter < 250:
        consumer = {}
        # using uuid to generate random meterIds
        consumer['meterId'] = str(uuid.uuid4())
        consumer['power'] = round(uniform(0.0, 1.5),5)
        zipcode = random.choice(cleaned_keyList)
        consumer['zipcode'] = zipcode
        consumer['netzentgelt'] = zipcode_to_data[zipcode]['netzentgelt']
        consumer['Konzessionsabgabe'] = zipcode_to_data[zipcode]['Konzessionsabgabe']
        consumer['coordinates'] = zipcode_to_data[zipcode]['coordinates']
        dummyData['consumers'].append(consumer)
        counter += 1

    return dummyData


def create_random_producers(cleaned_keyList, zipcode_to_data,dummyData):
    """ This function creates random producer households.
        The number after counter could be used to decide how many
        producers should be generated.
        keep in mind that there are already local distance households"""

    counter = 0
    while counter < 500:
        producer = {}
        producer['meterId'] = str(uuid.uuid4())
        producer['power'] = -round(uniform(0.0, 3.0),5)
        zipcode = random.choice(cleaned_keyList)

        producer['zipcode'] = zipcode
        producer['netzentgelt'] = zipcode_to_data[zipcode]['netzentgelt']
        producer['Konzessionsabgabe'] = zipcode_to_data[zipcode]['Konzessionsabgabe']
        producer['coordinates'] =zipcode_to_data[zipcode]['coordinates']

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


#function that sums up total power watts
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

    #get local pairs from file
    localDistance = get_local_pairs()
    #get list of producer and consumer households with local distance
    local_consumer_Ids, local_producer_Ids = local_distance_households(localDistance)

    #removing local distance households from key list
    cleaned_keyList, test = clean_keyList(local_consumer_Ids, local_producer_Ids, keylist)

    #create dictionary
    dummyData = make_json_structure()

    #add local distance consumers
    dummyData = create_local_consumer_households(local_consumer_Ids, dummyData, zipcode_to_data)

    #add local distance producers
    dummyData = create_local_producers_households(local_producer_Ids, dummyData, zipcode_to_data)

    #add random households
    dummyData = create_random_consumers(cleaned_keyList, zipcode_to_data, dummyData)
    dummyData = create_random_producers(cleaned_keyList, zipcode_to_data, dummyData)

    #calculate for header
    dummyData['total_power_watt_producers'] = sum_up_total_power_watt_producers(dummyData)
    dummyData['total_power_watt_consumers'] = sum_up_total_power_watt_consumers(dummyData)
    dummyData['total_power_watt'] = sum_up_total_power_watts(dummyData)


    #--------------dumping file -----------------------------------
    with open('500750consumer500_producer750.json', 'w') as file:
        json.dump(dummyData, file)

if __name__ == '__main__':
    main()