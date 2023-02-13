import requests
from flask import Flask, request, jsonify

FORCE = 100000  # F(N)
UNCHARGED_MASS = 35000  # M(KG)
SPEED = 140  # V (M/S)
MAX_DEPARTURE_TIME = 60  # t (sec)
MIN_CARGO_MASS = 0
MAX_TEMPERATURE = 30
MIN_TEMPERATURE = 15
HOURS_IN_DAY = 24
WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast'
LATITUDE = '30'
LONGITUDE = '35'
TEMPERATURE = 'temperature_2m'
app = Flask("GoldenPath", template_folder=r'C:/Users/cgc/PycharmProjects/GoldenPath')


def find_acceleration(cargo_mass):
    """
    function that find the plane acceleration
    :return: the plane acceleration
    """
    total_mass = find_total_mass(cargo_mass)
    acceleration = FORCE / total_mass  # a = F / M
    return acceleration


def find_total_mass(cargo_mass):
    """
    function that find the mass of the plane include the cargo mass
    :return: the mass of the plane
    """
    total_mass = UNCHARGED_MASS + cargo_mass
    return total_mass


def find_departure_time(acceleration):
    """
    function that find the departure time
    :param acceleration: the plane acceleration
    :return: the departure time
    """
    time = SPEED / acceleration  # t = v / a
    return time


def fix_over_weight(time):
    """
    function that finds what is the excess weight that needs to be destroyed
    :param time: current departure time
    :return: Nothing, print the excess weight that needs to be destroyed to stand the task
    """
    acceleration = SPEED / time  # a = v * t
    mass = FORCE / acceleration  # m = F / a
    max_mass = find_max_mass()
    unnecessary_weight = mass - max_mass
    return unnecessary_weight


def find_max_mass():
    """
    A function that finds the maximum mass that stands the task
    :return: the maximum mass
    """
    max_acceleration = SPEED / MAX_DEPARTURE_TIME  # a = v * t
    max_mass = FORCE / max_acceleration  # m = F / a
    return max_mass


def time_checker(time):
    """
    function that checks if the departure time is over the max time
    :param time: the departure time
    :return: nothing, if the time is over the max time send to fix_over_weight function
    """
    if time > MAX_DEPARTURE_TIME:
        return fix_over_weight(time)
    else:
        return ''


def find_departure_distance(acceleration, time):
    """
    function that finds the departure distance
    :param acceleration: the plane acceleration
    :param time: the departure time
    :return: the departure distance
    """
    # x = 0.5 * a * t^2 + V0t + x0
    distance = 0.5 * acceleration * time ** 2  # the initial speed and distance are 0, so there is no need to write them
    # in the equation
    return distance


def get_api_response(date):
    """
    function that send get request to open-metto.com api and get the temperature of each hour in that day
    :param date: the input date from the client
    :return: the temperature of each hour in the day
    """
    params = {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'start_date': date,
        'end_date': date,
        'hourly': TEMPERATURE,
    }
    response = requests.get(WEATHER_API_URL, params=params).json()
    return response


def weather_checker(date):
    """
    A function that checks in which hours it is possible to fly and in which hours it is not.
    param date: the inputdate from the client
    :return: if the plane can fly at least one hour a day it will return a message that includes
    the time. If the plane cannot fly at any time of the day, it will return a message that includes the temperature
    at any time of the day

    """
    api_response = get_api_response(date)
    times = api_response['hourly']['time']
    hours = [hour.replace(f'{date}T', '') for hour in times]
    hourly_temperature = api_response['hourly']['temperature_2m']
    can_fly = f''
    cant_fly_message = f''

    for i in range(HOURS_IN_DAY):
        if MIN_TEMPERATURE <= hourly_temperature[i] <= MAX_TEMPERATURE:
            can_fly += f' {str(hours[i])}, '
        else:
            cant_fly_message += f' {hours[i]} : {hourly_temperature[i]}C°, '
    if can_fly == '':
        return f'The weather on your selected date ({date}) does not permit to fly. The hours are: ' + cant_fly_message[0:-2]
    return f'The weather on your selected date ({date}) permit you to fly at :' + can_fly[0:-2]


@app.route("/", methods=["GET", "POST"])
def calculate():
    if request.method == 'POST':
        try:
            data = request.get_json()
            date = data.get('start_date', None).split('T')[0] # get only the date without the hour






            cargo_mass = int(data["cargo_mass"])
        except ValueError:
            return jsonify({'error': 'The cargo mass must be a number '})
        if cargo_mass < MIN_CARGO_MASS:
            return jsonify({'error': 'the cargo mass must be bigger then 0'})
        acceleration = find_acceleration(cargo_mass)
        time = find_departure_time(acceleration)
        distance = find_departure_distance(acceleration, time)
        excess_weight = time_checker(time)
        weather_message = weather_checker(date)
        return jsonify({
            'time': time,
            'distance': distance,
            'excess weight': excess_weight,
            'weather_message': weather_message

        })


if __name__ == '__main__':
    app.run(debug=True)
