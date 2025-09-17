def get_weather_forecast(location):
    """Get mock weather forecast data"""
    # In a real application, this would fetch data from a weather API
    return {
        'location': location,
        'temperature': 25,
        'humidity': 60,
        'rainfall': 800,
        'forecast': 'Partly cloudy with a chance of rain'
    }