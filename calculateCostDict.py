import json
from random import *
from geopy.distance import geodesic

with open('5050consumer50_producer50.json') as file:
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
        if float(konz_difference) > float(0):
            x = 1
        else:
            x = 0

        netz_difference = producer_netz - consumer_netz
        if float(netz_difference) > float(0):
            y = 1
        else:
            y = 0


        distance = float(geodesic(producer_coordinates,consumer_coordinates).km)
        if distance < float(4.5):
            z = 1
            localReduction = float(2.07)
        else:
            z = 0

        eeg_umlage = float(6.81)

        cost = round((float(30) - konz_difference - netz_difference - localReduction - eeg_umlage),5)

        #hier bedingung reinmachen, dass wenn gesetzliche rahmenbedinungen zur Reduzierung eingesetzt werden eine 1, oder eine 0
        #reihenfolge ist lokalerZusammenhang, netzentgeltdifferenzen, konzessionsabgaben = [x,y,z]
        # create nested dictionary
        nested_cost_dictionary[firstKey][secondKey] = {}
        nested_cost_dictionary[firstKey][secondKey] = cost

        pairs_and_usedReduction[(firstKey,secondKey)] = [x, y, z]




#--------------dumping file -----------------------------------
with open('5050consumer50_producer50_costs.json', 'w') as file:
    json.dump(nested_cost_dictionary, file)


with open(('5050consumer50_producer50_reductions.json'), 'w') as f:
    json.dump(str(pairs_and_usedReduction), f)

"""
for k,v in pairs_and_usedReduction.items():
    if v[1] == 1:
        print("hello")
        
    if v[2] == 1:
        print("lokal")
    
    if v[0] == 1:
        print("netz")"""