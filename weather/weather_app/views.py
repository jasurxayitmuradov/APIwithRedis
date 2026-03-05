import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

@api_view(['GET'])
def get_weather(request, city):
    # 1. Avval keshdan qidiramiz
    cache_key = f"weather_{city.lower()}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response({"source": "cache", "data": cached_data})

    # 2. Agar keshda bo'lmasa, API'dan olamiz
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={api_key}&contentType=json"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            # Ma'lumotni 12 soatga keshga saqlaymiz
            cache.set(cache_key, weather_data, timeout=43200) 
            return Response({"source": "api", "data": weather_data})
        
        return Response({"error": "Shahar topilmadi"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)