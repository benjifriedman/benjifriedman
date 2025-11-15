from datetime import datetime

from pytz import timezone
from jinja2 import Environment, FileSystemLoader

from infrastructure import weather

def main():
    """Compile variables and pass into README"""
    (
        weather_dict,
        city_temperature,
        sunrise_time_unix,
        sunset_time_unix,
    ) = weather.get_openweather_info()

    timestamp = weather.convert_timestamp_to_PST(sunrise_time_unix)
    formatted_time = timestamp.strftime("%H:%M %p")
    sunrise_time = str(formatted_time)

    # Convert from 24 hour to 12 hour clock
    sunset_time = weather.convert_timestamp_to_PST(sunset_time_unix).strftime("%H:%M")
    sunset_time = datetime.strptime(sunset_time, "%H:%M").strftime("%I:%M %p")

    current_time_PST = datetime.now(timezone("US/Pacific")).strftime("%H:%M")
    current_time_PST = datetime.strptime(current_time_PST, "%H:%M").strftime("%I:%M %p")
    current_date = datetime.now(timezone("US/Pacific")).strftime("%Y-%m-%d")

    template_variables = {
        "current_datetime_PST": f"{current_date} {current_time_PST}",
        "current_time_PST": datetime.now(timezone("US/Pacific")).strftime("%I:%M %p"),
        "sun_rise": sunrise_time,
        "sun_set": sunset_time,
        "temperature": city_temperature,
        "weather_emoji": weather.weather_icon(city_temperature),
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
