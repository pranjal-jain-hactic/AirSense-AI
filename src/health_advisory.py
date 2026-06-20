def get_health_advisory(aqi):

    if aqi <= 50:
        return "Good", "Air quality is satisfactory. Enjoy outdoor activities."

    elif aqi <= 100:
        return "Moderate", "Sensitive people should reduce prolonged outdoor activity."

    elif aqi <= 200:
        return "Poor", "Wear a mask outdoors and limit outdoor exercise."

    elif aqi <= 300:
        return "Unhealthy", "Avoid strenuous outdoor activities. Use air purifiers indoors."

    elif aqi <= 400:
        return "Very Unhealthy", "Stay indoors as much as possible."

    else:
        return "Hazardous", "Avoid outdoor exposure. Follow health advisories."