import json
import random


def create_integer_cost_dict():
    """ this function receives a cost dictionary for a simulated
        community and converts the values into integer values.
        Integer values are needed for the network simplex algorithm"""

    with open('100150consumer100_producer150_costs.json') as file:
        household_data = json.load(file)

    nested_cost_dictionary = {}
    for producer in household_data['producers']:
        firstKey = producer['meterId']

        nested_cost_dictionary[firstKey] = {}

        for consumer in household_data['consumers']:
            secondKey = consumer['meterId']

            cost = random.randint(18,24)
            nested_cost_dictionary[firstKey][secondKey] = {}
            nested_cost_dictionary[firstKey][secondKey] = cost



    #--------------dumping file -----------------------------------
    with open('integer_consumer180_producer180_costs.json', 'w') as file:
       json.dump(nested_cost_dictionary, file)

    return 0


def main():

    print(create_integer_cost_dict())

if __name__ == '__main__':
    main()

