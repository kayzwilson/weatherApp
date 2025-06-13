import requests
import pytz

def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params ={
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
          temp = data['main']['temp']
          humidity = data['main']['humidity']
          description = data['weather'][0]['description']
          print(f"Weather for {city.title()} city")
          print(f"Description: {description.capitalize()}")
          print(f"Temperature: {temp}")
          print(f"Humidity: {humidity}\n")
        else:
          print(f"City {city} not available. Please check the Name")
    except requests.exceptions.ConnectionError:
        print("\n❌ No internet connection. Please check your connection and try again.")
    except requests.exceptions.Timeout:
        print("\n⏱️ The request timed out. Try again later.")
    except requests.exceptions.HTTPError as err:
        print(f"\n⚠️ HTTP Error: {err}")
    except Exception as e:
        print(f"\n🚨 An unexpected error occurred: {e}")

def find_timezone(city_name):
    city = city_name.lower().replace(" ", "").replace("_", "").replace("-", "")
    possible_matches = []

    for tz in pytz.all_timezones:
        cleaned_tz = tz.lower().replace("_", "").replace("-", "")
        if city in cleaned_tz:
            return tz
        if city[:3] in cleaned_tz:
            possible_matches.append(tz)

    if possible_matches:
        print("\nDid you mean one of these timezones?")
        for m in possible_matches[:5]:
            print(" -", m)

    return None


def get_time(city):
    timezone = find_timezone(city)
    if timezone:
        url = f"https://timeapi.io/api/Time/current/zone?timeZone={timezone}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
               data = response.json()
               print(f"\nCurrent time in {city.title()} ({timezone}): {data['dateTime']}")
            else:
                print("❌ Error fetching time data.")
        except requests.exceptions.ConnectionError:
          print("\n❌ No internet connection. Please try again later.")
        except requests.exceptions.Timeout:
           print("\n⏱️ The request timed out. Try again later.")
        except requests.exceptions.HTTPError as err:
          print(f"\n⚠️ HTTP Error: {err}")
        except Exception as e:
           print(f"\n🚨 An unexpected error occurred: {e}")
    else:
        print(f"❌ Could not find timezone for city '{city}'.")


if __name__ == "__main__":
    print("====WeatherApp====")
    print("Enter Name of City for weather and \'close\' to Exit")
    while(True):
      city = input("Enter Name of city: ").lower()
      api_key = "55f25917642981a966fe7d08fd82ab19" 
      if city == 'close':
          print("Closing Program....")
          break
      else:
        get_time(city)
        get_weather(city, api_key)
        