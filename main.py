from datetime import datetime

from pytz import timezone
from jinja2 import Environment, FileSystemLoader

from infrastructure import weather, flickr

def main():
    """Compile variables and pass into README"""
    (
        weather_dict,
        city_temperature,
        sunrise_time_unix,
        sunset_time_unix,
        weather_description,
        weather_emoji_icon,
    ) = weather.get_openweather_info()
    
    # Get random Flickr photo
    flickr_photo = flickr.get_random_flickr_photo()

    pacific_tz = timezone("US/Pacific")
    current_timestamp_aware = datetime.now(pacific_tz)
    
    sunrise_timestamp = weather.convert_timestamp_to_pacific(sunrise_time_unix, pacific_tz)
    sunset_timestamp = weather.convert_timestamp_to_pacific(sunset_time_unix, pacific_tz)
    current_timestamp = current_timestamp_aware.replace(tzinfo=None)
    
    # Determine if we're in PST or PDT
    timezone_name = current_timestamp_aware.strftime("%Z")  # Returns "PST" or "PDT"
    
    sunrise_time = sunrise_timestamp.strftime("%-I:%M %p")
    sunset_time = sunset_timestamp.strftime("%-I:%M %p")

    current_time = current_timestamp_aware.strftime("%-I:%M %p")
    current_date = current_timestamp_aware.strftime("%Y-%m-%d")
    current_day = current_timestamp_aware.strftime("%A, %B %d, %Y")
    
    # Determine sunrise/sunset text based on current time
    if current_timestamp < sunrise_timestamp:
        # Before sunrise
        sunrise_text = "the sunrise will be at"
        sunset_text = "sunset is at"
        is_after_sunset = False
    elif current_timestamp < sunset_timestamp:
        # Between sunrise and sunset (daytime)
        sunrise_text = "sunrise today was at"
        sunset_text = "sunset will be at"
        is_after_sunset = False
    else:
        # After sunset
        sunrise_text = "the sunrise will be at"
        sunset_text = "sunset was at"
        is_after_sunset = True

    template_variables = {
        "current_datetime": f"{current_date} {current_time}",
        "current_time": current_time,
        "timezone_name": timezone_name,
        "current_day": current_day,
        "sun_rise": sunrise_time,
        "sun_set": sunset_time,
        "sunrise_text": sunrise_text,
        "sunset_text": sunset_text,
        "is_after_sunset": is_after_sunset,
        "temperature": city_temperature,
        "weather_description": weather_description,
        "weather_emoji": weather_emoji_icon,
        "flickr_photo": flickr_photo,
    }

    # Load template, pass in variables, write to README.md
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("main.html")
    output_from_parsed_template = template.render(template_variables)

    with open("README.md", "w+") as fh:
        fh.write(output_from_parsed_template)

    return

if __name__ == "__main__":
    main()
