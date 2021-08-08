# simulated_communities_generator

based on https://launix.de/launix/launix-gibt-plz-datenbank-frei/ distances of all zipcodes in Germany have
been calcultated and saved to cleaned_local_


dataGenerator.py
- this script rebuilds producer and consumer data
- it could generate different numbers of producer and consumer households
- it generates unique Ids for all households
- it generates demands for consumer households and supplys for producer households


# what is needed
- a script that builds a cost matrix similiar to the BloGPV-Communitys
- it should contain:
- Die Möglichkeit die Zahlen zu beeinflussen, wie viele Haushalte sich in räumlichen Zusammenhang befinden, oder wie viele Haushalte sich in verschiedenen Netzentgeltzonen befinden.
- Es ist nicht notwendig Koordinaten für jeden Haushalt zu erschaffen, da alle Zusammenhänge über die Strompreisdifferenzen dargestellt werden können.

# Haushalt random Koordinaten zurodnen
https://launix.de/launix/launix-gibt-plz-datenbank-frei/

-> würde konkrete Aussagen über lokalen Zusammenhang und Verteilung von Haushalten auf ländlichere Regionen oder Stadtregionen erlauben
-> Nutzen der Funktionen, die ene't daten analysieren
-> Innerhalb einer PLZ werden bestimmte Anzahl an Haushalten als miteinander in räumlichen Zusammenhang befindend angenommen
