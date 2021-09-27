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


def generate_local_distance():
    """ function that returns a list of zipcodes with locals distance
        in specific areas in germany"""
    locals = []

    with open('cleaned_lokaler_Zusammenhang.csv') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            #tübingen
            if row[0] == '72072':
                locals.append(row)

            #köln
            if row[0] == '50667':
                locals.append(row)

            #berlin
            if row[0] == '12045':
                locals.append(row)

            #rottenburg
            if row[0] == '72108':
                locals.append(row)

            #kiel
            if row[0] == '24111':
                locals.append(row)

            #hannover
            if row[0] == '30169':
                locals.append(row)

            #dresden
            if row[0] == '01139':
                locals.append(row)

            #erfurt
            if row[0] == '01139':
                locals.append(row)

    return locals


def create_local_consumers(locals, dummyData, zipcode_to_data):
    """ this function adds consumer households to the simulated
            community that have local distance to other households in
            the simulated community.
            It returns the python dictionary dummyData"""

    for pair in locals:
        consumer = {}
        zipcode = pair[0]
        consumer['meterId'] = str(uuid.uuid4())
        consumer['power'] = round(uniform(0.0, 1.5), 5)
        consumer['netzentgelt'] = zipcode_to_data[zipcode]['netzentgelt']
        consumer['Konzessionsabgabe'] = zipcode_to_data[zipcode]['Konzessionsabgabe']
        consumer['coordinates'] = zipcode_to_data[zipcode]['coordinates']
        dummyData['consumers'].append(consumer)

    return dummyData


def create_local_producers(locals, dummyData, zipcode_to_data):
    """ this function adds producer households to the simulated
                community that have local distance to other households in
                the simulated community.
                It returns the python dictionary dummyData"""

    for pair in locals:
        producer = {}
        zipcode = pair[1]
        producer['meterId'] = str(uuid.uuid4())
        producer['power'] = round(uniform(0.0, 1.5), 5)
        producer['netzentgelt'] = zipcode_to_data[zipcode]['netzentgelt']
        producer['Konzessionsabgabe'] = zipcode_to_data[zipcode]['Konzessionsabgabe']
        producer['coordinates'] = zipcode_to_data[zipcode]['coordinates']
        dummyData['producers'].append(producer)

    return dummyData


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

    #list of zipcodes with local distance
    locals = generate_local_distance()

   # for pair in locals:
    #    print(pair)

   # print(len(locals))

    # create dictionary
    dummyData = make_json_structure()

    #add local producers
    i = 0
    while i < 2:
        dummyData = create_local_producers(locals,dummyData, zipcode_to_data)

        dummyData = create_local_consumers(locals,dummyData, zipcode_to_data)

        i += 1

    #calculate for header
    dummyData['total_power_watt_producers'] = sum_up_total_power_watt_producers(dummyData)
    dummyData['total_power_watt_consumers'] = sum_up_total_power_watt_consumers(dummyData)
    dummyData['total_power_watt'] = sum_up_total_power_watts(dummyData)


    #--------------dumping file -----------------------------------
    with open('micro_local_clusters.json', 'w') as file:
        json.dump(dummyData, file)

if __name__ == '__main__':
    main()