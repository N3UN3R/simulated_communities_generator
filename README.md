# simulated_communities_generator


# needed data

zipcodes_to_specificData.json
- contains zipcodes matched to necessary data like the coordinates, net costs and konzession costs

PLZ_orte.csv
- contains zipcodes in Germany matched to coordinates.
  available on https://launix.de/launix/launix-gibt-plz-datenbank-frei/

cleaned_kein_lokaler_Zusammenhang.csv
- contains zipcodes that have a distance over 4.5 km

cleaned_lokaler_Zusammenhang.csv
- contains zipcodes that have a distance under 4.5 km

# programs

calculatedCostDict.py
-	Program that calculates cost dictionarys for simulated communities as well as the used reductions
  of each possible trading pair


costDictIntegers.py
-	Program that transforms the float values of cost dictionaries into integer values which are needed for
  the network simplex algorithm


generate_local_communities.py
-	program that generates a community containing just households with local distance 


generate_micro_clusters.py
-	Program that generates a community which contains household clusters with local distance
  for specific zipcode areas in Germany


generate_scaled_commmunities.py
-	Program that generates random communities of optional size


No_locals_community.py
- Program that generates communties with households without local distance

