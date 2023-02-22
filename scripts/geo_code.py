import googlemaps
import csv
#hide key
api_key = 'AIzaSyABteA2oGa6yJK1u92PAvbKhcpMiiE21w8'
gmaps = googlemaps.Client(key=api_key)
#Read from CSV or JSON
#address_directory = csv.DictReader("filename")
address_directory = {
    'Warming Centers' : ['1140 West 79th Street, Chicago, IL 60620',
                         '10 South Kedzie Avenue, Chicago, IL 60612',
                         '4314 South Cottage Grove, Chicago, IL 60653',
                         '845 West Wilson Avenue, Chicago, IL 60640',
                         '8650 South Commercial Avenue, Chicago, IL 60617',
                         '4312 West North Avenue, Chicago, IL 60639'
                         ]
}
def geocode(directory):
    coord_directory = {}
    for prov,locations in directory.items():
        coord_directory[prov]=[]
        for location in locations:
            geocode_result = gmaps.geocode(location)
            lat = geocode_result[0]['geometry']['location']['lat']
            long = geocode_result[0]['geometry']['location']['lng']
            coord_directory[prov].append((location,lat,long))
    return coord_directory
