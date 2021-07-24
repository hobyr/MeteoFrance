import sys
import meteofrance_api

def request_api_data(query):
    """
    Request location's weather from Meteo France's API.
    """
    # Perform location search according to query
    city = meteofrance_api.client.MeteoFranceClient().search_places(search_query=query)
    # Initialize choice variable for later WHILE loop
    choice = ''
    # Ask user to choose city for forecast
    if len(city) == 0:
        sys.exit("Cities not found... Quitting...")
    if len(city) > 1:
        print("\nWhich location do you want the forecast of?")
        for ind, place in enumerate(city):
            print(f"{ind}. {place.name}, {place.postal_code}, {place.country}")
        while True:
            choice = input("Choice [q to quit]: ")
            if choice == 'q':
                sys.exit('Bye')
            if not choice.isdigit():
                continue
            if int(choice) >= len(city):
                continue
            else:
                choice = int(choice)
                break
    # Choose only location if no choice to be made
    else:
        choice = 0
        print(f"Weather forecast for {city[choice].name}, {city[choice].postal_code}")
    loc = city[choice]
    # Retrieve forecast for chosen location
    forecast = meteofrance_api.client.MeteoFranceClient().get_forecast_for_place(loc, language='en')
    return loc, forecast


def print_today_forecast(location, forecast):
    """
    Print today's forecast at selected location.

    location: chosen location
    forecast: forecast info (contains current, today, daily forecast for 15 days)
    """
    # Retrieve today's forecast at chosen location
    today_fc = forecast.today_forecast
    sunrise_time = forecast.timestamp_to_locale_time(today_fc['sun']['rise'])
    sunset_time = forecast.timestamp_to_locale_time(today_fc['sun']['set'])
    # Pretty print today's forecast information
    print('')
    print(' Today\'s forecast '.center(50, '*'))
    print(f"Location: {location.name}, {location.postal_code}, {location.country} ({location.latitude},{location.longitude})",
          f"\nLast update: {forecast.timestamp_to_locale_time(today_fc['dt'])}",
          f"\nMinimal temperature: {today_fc['T']['min']}°C | Maximal temperature: {today_fc['T']['max']}°C",
          f"\nMinimal humidity: {today_fc['humidity']['min']} % | Maximal humidity: {today_fc['humidity']['max']} %",
          f"\nUV Index: {today_fc['uv']}",
          f"\nSunrise: {sunrise_time} | Sunset: {sunset_time}")


def print_current_forecast(location, forecast):
    """
    Print current forecast at selected location.

    location: chosen location
    forecast: forecast info (contains current, today, daily forecast for 15 days)
    """
    # Retrieve current forecast at chosen location
    current_fc = forecast.current_forecast
    # Pretty print current forecast information
    print('')
    print(' Current forecast '.center(50, '*'))
    print(f"Location: {location.name}, {location.postal_code}, {location.country} ({location.latitude},{location.longitude})",
          f"\nLast update: {forecast.timestamp_to_locale_time(current_fc['dt'])}",
          f"\nCurrent temperature: {current_fc['T']['value']}°C",
          f"\nWindchill: {current_fc['T']['windchill']}°C",
          f"\nHumidity: {current_fc['humidity']} %",
          f"\nWind: {current_fc['wind']['speed']} km/h, Direction {current_fc['wind']['icon']}",
          f"\nCloud coverage: {current_fc['clouds']} %, {current_fc['weather']['desc']}")


if __name__ == "__main__":
    query = sys.argv[1]
    location, forecast = request_api_data(query)
    print("\nType of forecast:\n0. Current forecast\n1. Today's forecast")
    # Ask user to choose type of forecast
    choice = ''
    while True:
        choice = input("Choice [q to quit]: ")
        if choice == 'q':
            sys.exit('Bye')
        if not choice.isdigit():
            continue
        if int(choice) > 1:
            continue
        else:
            choice = int(choice)
            break
    if choice == 0:
        print_current_forecast(location, forecast)
    else:
        print_today_forecast(location, forecast)
