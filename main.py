import customtkinter
import requests
from PIL import Image
from io import BytesIO

BASE_URL = "http://dataservice.accuweather.com/locations/v1/cities/search"
POSTAL_URL = "http://dataservice.accuweather.com/locations/v1/postalcodes/search"
WEATHER_URL = "http://dataservice.accuweather.com/currentconditions/v1/"
TOMORROW_URL = "http://dataservice.accuweather.com/forecasts/v1/daily/1day/"
NEIGBOURS_URL = "http://dataservice.accuweather.com/locations/v1/cities/neighbors/"
API_KEY = "DnR9ZZrPguPY9udOQpnrq64uUk7bJiff"
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

komunikat_pogodowy = "Aktualna pogoda: \n"
locationkey = "264369" #domyślnie koluszki

root = customtkinter.CTk()
root.geometry("500x700")
#[{'Version': 1, 'Key': '264369', 'Type': 'City', 'Rank': 65, 'LocalizedName': 'Koluszki', 'EnglishName': 'Koluszki', 'PrimaryPostalCode': '', 'Region': {'ID': 'EUR', 'LocalizedName': 'Europa', 'EnglishName': 'Europe'}, 'Country': {'ID': 'PL', 'LocalizedName': 'Polska', 'EnglishName': 'Poland'}, 'AdministrativeArea': {'ID': '10', 'LocalizedName': 'Łódzkie', 'EnglishName': 'Łódź', 'Level': 1, 'LocalizedType': 'Województwo', 'EnglishType': 'Voivodship', 'CountryID': 'PL'}, 'TimeZone': {'Code': 'CEST', 'Name': 'Europe/Warsaw', 'GmtOffset': 2.0, 'IsDaylightSaving': True, 'NextOffsetChange': '2023-10-29T01:00:00Z'}, 'GeoPosition': {'Latitude': 51.746, 'Longitude': 19.818, 'Elevation': {'Metric': {'Value': 209.0, 'Unit': 'm', 'UnitType': 5}, 'Imperial': {'Value': 685.0, 'Unit': 'ft', 'UnitType': 0}}}, 'IsAlias': False, 'SupplementalAdminAreas': [{'Level': 2, 'LocalizedName': 'Łódź East', 'EnglishName': 'Łódź East'}, {'Level': 3, 'LocalizedName': 'Koluszki', 'EnglishName': 'Koluszki'}], 'DataSets': ['AirQualityCurrentConditions', 'AirQualityForecasts', 'Alerts', 'DailyPollenForecast', 'ForecastConfidence', 'FutureRadar', 'MinuteCast', 'Radar']}]
#[{'LocalObservationDateTime': '2023-10-20T12:27:00+02:00', 'EpochTime': 1697797620, 'WeatherText': 'Pochmurno', 'WeatherIcon': 7, 'HasPrecipitation': False, 'PrecipitationType': None, 'IsDayTime': True, 'Temperature': {'Metric': {'Value': 9.0, 'Unit': 'C', 'UnitType': 17}, 'Imperial': {'Value': 48.0, 'Unit': 'F', 'UnitType': 18}}, 'MobileLink': 'http://www.accuweather.com/pl/pl/koluszki/264369/current-weather/264369', 'Link': 'http://www.accuweather.com/pl/pl/koluszki/264369/current-weather/264369'}]

def get_tomorrow(locationkey):
    query_params = {
        "apikey": API_KEY,
        "language": "pl-pl",
    }
    response = requests.get(TOMORROW_URL + locationkey, params=query_params)
    data = response.json()
    print(data)
    label_tom.configure(text="Pogoda jutro: \n" + data["DailyForecasts"][0]["Day"]["IconPhrase"] + "\n" + data["DailyForecasts"][0]["Night"]["IconPhrase"] + "\n" + str(data["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"]) + " stopni F minimum" + "\n" + str(data["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"]) + " stopni F maksimum")
def get_location(city):
    query_params = {
        "apikey": API_KEY,
        "q": city,
        "language": "pl-pl",
    }
    response = requests.get(BASE_URL, params=query_params)
    data = response.json()
    print(data)
    cityname = data[0]["LocalizedName"]
    global locationkey
    locationkey = data[0]["Key"]
    further_action(cityname)

def get_neighbours(locationkey, day):
    query_params = {
        "apikey": API_KEY,
        "language": "pl-pl",
    }
    response = requests.get(NEIGBOURS_URL + locationkey, params=query_params)
    data = response.json()
    print(data)


    iterator = 0
    for miejsce in data:
        if iterator <= int(day):
            iterator += 1
            print(miejsce["LocalizedName"])
            label_10.configure(text=label_10.cget("text") + "\n" + miejsce["LocalizedName"])

def get_postal(postal):
    query_params = {
        "apikey": API_KEY,
        "q": postal,
        "language": "pl-pl",
    }
    response = requests.get(POSTAL_URL, params=query_params)
    data = response.json()
    print(data)

    cityname = data[0]["LocalizedName"]
    global locationkey
    locationkey = data[0]["Key"]
    further_action(cityname)


def truly_get_weather(locationkey):
    query_params = {
        "apikey": API_KEY,
        "language": "pl-pl",
    }
    response = requests.get(WEATHER_URL + locationkey, params=query_params)
    data = response.json()
    print(data)
    label2.configure(text=komunikat_pogodowy + data[0]["WeatherText"] + "\n" + str(data[0]["Temperature"]["Metric"]["Value"]) + " stopni Celsjusza")


def further_action(cityname):
    label.configure(text=cityname)
    print("hihi")

def get_picture():
    query_params = {
        "apikey": API_KEY,
        "language": "pl-pl",
    }

    image_url = "https://scontent-waw1-1.xx.fbcdn.net/v/t39.30808-6/387773743_719915213511812_2899296914246115864_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=5f2048&_nc_ohc=YRUTDuyggL8AX9OlAWA&_nc_ht=scontent-waw1-1.xx&oh=00_AfChRTCByAXBBqXdvxb748y5_gP1X3ZNhEFFJB4YLDoXaw&oe=6538F8DE"
    response = requests.get(image_url)

    if response.status_code == 200:
        # Przekształć odpowiedź do obiektu Image
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        photo = customtkinter.CTkImage(image)


        # Utwórz okno aplikacji CTK
        root = customtkinter.CTk()
        root.title("CustomTkinter - Wyświetlanie obrazu")

        # Utwórz etykietę i przypisz obraz
        labelph.configure(image=photo)

        # Rozpocznij pętlę główną aplikacji



frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

header_frame = customtkinter.CTkFrame(frame)
header_frame.pack()

button_frame = customtkinter.CTkFrame(frame)
button_frame.pack()
combo_frame = customtkinter.CTkFrame(frame)
combo_frame.pack()

label = customtkinter.CTkLabel(header_frame, text="Pogodowe API")
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(header_frame, placeholder_text="Miasto")
entry1.pack(pady=12, padx=10)



button_general = customtkinter.CTkButton(master=button_frame, text="Znajdź Miasto", command=lambda: get_location(entry1.get()))
button_general.pack(side="left")

button_pos = customtkinter.CTkButton(master=button_frame, text="Znajdz kod pocztowy", command=lambda: get_postal(entry1.get()))
button_pos.pack(side="left")

button_sec = customtkinter.CTkButton(master=frame, text="aktualna pogoda", command=lambda: truly_get_weather(locationkey))
button_sec.pack(pady=12, padx=10)

button_tom = customtkinter.CTkButton(master=frame, text="pogoda jutro", command=lambda: get_tomorrow(locationkey))
button_tom.pack(pady=12, padx=10)

button_10 = customtkinter.CTkButton(master=combo_frame, text="wyświetl okolicę", command=lambda: get_neighbours(locationkey, dropdown.get()))
button_10.pack(pady=12, padx=10)


# Utwórz listę rozwijaną i przekaż dostępne opcje
dropdown = customtkinter.CTkComboBox(master=combo_frame, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
dropdown.pack()

checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
checkbox.pack(pady=12, padx=10)

label2 = customtkinter.CTkLabel(master=frame, text="")
label2.pack(pady=12, padx=10)

label_tom = customtkinter.CTkLabel(master=frame, text="")
label_tom.pack(pady=12, padx=10)

label_10 = customtkinter.CTkLabel(master=frame, text="")
label_10.pack(pady=12, padx=10)


root.mainloop()
