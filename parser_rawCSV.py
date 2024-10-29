import csv
#https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat

def load_airports(file_path):
    airports = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            iata = row[4]  # IATA code
            if "\\" in iata:
                continue
            name = row[1]  # Airport name
            latitude = float(row[6])  # Latitude
            longitude = float(row[7])  # Longitude
            country = row[3]  # Country
            city = row[2]  # City

            airports.append((iata, name, latitude, longitude, country, city))
    return airports

def save_airports_to_csv(airports, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Writing the header
        writer.writerow(["IATA", "Name", "LATITUDE", "LONGITUDE", "Country", "City"])
        # Writing airport data
        writer.writerows(airports)

# Usage
airports = load_airports('airport.csv')
# Saving to 'airports_sample.csv'
file_path = "processed_airports.csv"
save_airports_to_csv(airports, file_path)


