import json
from random import *
from geopy.distance import geodesic

def calculate_costs_and_reductions():
    """ this function calculates the cost dictionary for
        simulated communities. It receives the simulated data
        which contains information like the zipcode, netCost and
        konzessioncost and returns a cost dictionary for this
        community as well as all used reductions in 2 .json files"""

    with open('150_no_locals_community.json') as file:
        household_data = json.load(file)

    #dictionarys for data
    nested_cost_dictionary = {}
    pairs_and_usedReduction = {}

    x,y,z =[0,0,0]

    for producer in household_data['producers']:
        #producer data
        firstKey = producer['meterId']
        producer_konz = float(producer['Konzessionsabgabe'].replace(',', '.'))
        producer_netz = float(producer['netzentgelt'].replace(',', '.'))
        producer_coordinates = producer['coordinates']

        nested_cost_dictionary[firstKey] = {}
       # pairs_and_usedReduction[firstKey] = {}

        for consumer in household_data['consumers']:
            #consumerData
            secondKey = consumer['meterId']
            consumer_konz = float(consumer['Konzessionsabgabe'].replace(',', '.'))
            consumer_netz = float(consumer['netzentgelt'].replace(',', '.'))
            consumer_coordinates = consumer['coordinates']
            konz_difference = producer_konz - consumer_konz
            reduction = 0

            if float(konz_difference) > float(0):
                x = 1
                reduction += konz_difference
            else:
                x = 0

            netz_difference = producer_netz - consumer_netz
            if float(netz_difference) > float(0):
                y = 1
                reduction += netz_difference
            else:
                y = 0

            distance = float(geodesic(producer_coordinates,consumer_coordinates).km)
            if distance < float(4.5):
                z = 1
                localReduction = float(2.07)
                reduction += localReduction
            else:
                z = 0
                localReduction = float(0)

            eeg_umlage = float(6.81)

            cost = round((float(30) - reduction - eeg_umlage),5)

            #order of reductions is lokalerZusammenhang, netzentgeltdifferenzen, konzessionsabgaben = [x,y,z]
            # create nested dictionary
            nested_cost_dictionary[firstKey][secondKey] = {}
            nested_cost_dictionary[firstKey][secondKey] = cost

            pairs_and_usedReduction[(firstKey,secondKey)] = [x, y, z]

    #--------------dumping file -----------------------------------
    with open('150_no_locals_community_costs.json', 'w') as file:
        json.dump(nested_cost_dictionary, file)


    with open(('150_no_locals_community_reductions.json'), 'w') as f:
        json.dump(str(pairs_and_usedReduction), f)

    return 0


def main():

    print(calculate_costs_and_reductions())

if __name__ == '__main__':
    main()


