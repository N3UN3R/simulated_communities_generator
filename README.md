# simulated_communities_generator

based on https://launix.de/launix/launix-gibt-plz-datenbank-frei/ distances of all zipcodes in Germany have
been calcultated and saved to cleaned_local_distances.csv


dataGenerator_withLocals.py
 - this script rebuilds producer and consumer data
- based on the distances in cleaned_local_distances.csv this script generates
  simulated households with unique meter-Ids and random supply/demand values

  function local_distance_households(localDistance)
   makes it possible to decide how many of those generated households do have local distance
 
  function create_random_consumers and create_random_producers could be used to generate random households
  which are not in local distance


calculateCostDict.py
- this script creates a cost-dictionary for all generated households based
- it also creates a file with all used reductions to generate the cost dictionary




