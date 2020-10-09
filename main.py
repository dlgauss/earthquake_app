import geocoder
import requests
from prettytable import PrettyTable
from folium.plugins import MarkerCluster
import folium





# Obtain initial data
starttime = input('Please enter start time (format year-month-day): ')
endtime = input('Please enter end time (format year-month-day):  ')
location_api = geocoder.osm(input('Enter name of city or country: '))
latitude = location_api.lat
longitude = location_api.lng
max_radius_km = input('Enter Max Radius KM: ')
minmagnitude = input('Min magnitude: ')


#Get data frrom API https://earthquake.usgs.gov
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
response = requests.get(url, headers = {'Acces':'applcation/json'}, params={
    'format':'geojson',
    'starttime':starttime,
    'endtime':endtime,
    'latitude':latitude,
    'longitude':longitude,
    'maxradiuskm': max_radius_km,
    'minmagnitude':minmagnitude

})

data = response.json()

#Create aditional a table
table = PrettyTable(['No.','Location','Magnitude','Longitude','Latitude'])
#Create a list for inital data for map
map_list = []

#Filter json file, obtain s[0] = Place , s[1] = Longitude , s[2] = Latitude , s[3] = Magnitude
number = 0
for json_data in data['features']:
    number+=1
    place = json_data ['properties']['place']
    magnitude = json_data ['properties']['mag']
    coord_long = json_data ['geometry']['coordinates'][0]
    coord_lat =json_data ['geometry']['coordinates'][1]
    table.add_row([number,place,magnitude,coord_long,coord_lat])
    new_list = [place]+[coord_long]+[coord_lat]+[magnitude]
    map_list.append(new_list)


### Creating map

map_hooray = folium.Map(location=[latitude, longitude],zoom_start = 7)

marker_cluster = MarkerCluster().add_to(map_hooray)

# Colorizle popup def
def color_change(priora):
    if (json_data_list[3] <= 4):
        return ('beige')
    elif (json_data_list[3] <=5):
        return ('orange')
    elif (json_data_list[3] <= 6):
        return ('red')
    elif (json_data_list[3] <= 10):
        return ('darkred')



#Adding poppups to map
for json_data_list in map_list:
    name_country, long_number, lat_number, magnit = json_data_list[0], json_data_list[1], json_data_list[2], json_data_list[3]
#json_data_list[0] = Place , json_data_list[1] = latitudine , json_data_list[2] = longitudine

    tt_popup_html = f'''<b>Place:</b> {json_data_list[0]} <br> <b>Magnitude:</b> {magnit} '''

    iframe = folium.IFrame(html=tt_popup_html, width=300, height=150)
    popup = folium.Popup(iframe, max_width=2000)

    folium.Marker(location=[lat_number, long_number], popup=popup,icon=folium.Icon(color=color_change(magnit)),  fill_opacity=1).add_to(map_hooray)

map_hooray.save('/home/gaus/MyProjects/earthquake_app/earthquake.html')
print(table)

