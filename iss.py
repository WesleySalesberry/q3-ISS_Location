#!/usr/bin/env python

__author__ = 'Wesley Salesberry'

import turtle
from datetime import datetime
import requests
import json


# Cleans up the json so that it is readable
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


# gets the number and name of each astronaught
def get_astronauts_information(URL):

    people = []

    res = requests.get(URL + "/astros.json")
    person = res.json()["people"]
    amount = res.json()["number"]
    # craft = res.json()["craft"]
    for p in person:
        # person = p["name"]
        people.append(p)

    # print(amount)
    jprint(people)


# Get the ISS current geographic coordinates and a timestamp
def get_ISS_information(URL):
    res = requests.get(URL)
    time_stamp = datetime.fromtimestamp(res.json()["timestamp"])
    location = res.json()["iss_position"]
    latitude = location["latitude"]
    longitude = location["longitude"]

    return [time_stamp, latitude, longitude]


def create_world(shape, lat, long):
    screen = turtle.Screen()
    screen.title("ISS Location")
    screen.setup(720, 360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic("map.gif")

    screen.register_shape(shape)
    create_ISS(shape, lat, long)
    pass_over_Indy()
    turtle.mainloop()


def create_ISS(shape, lat, long):
    iss = turtle.Turtle()
    iss.shape(shape)
    iss.setheading(90)

    iss.penup()
    iss.goto(long, lat)


def pass_over_Indy():
    indy_lat = 39.7684
    indy_long = -86.1581

    location = turtle.Turtle()
    location.penup()
    location.color("yellow")
    location.goto(indy_long, indy_lat)
    location.dot(5)
    time = pass_over_info("http://api.open-notify.org/iss-pass.json",
                          indy_lat, indy_long)
    style = ('Arial', 10, "bold")
    location.write(time, font=style)
    location.hideturtle()


def pass_over_info(URL, lat, long):
    URL = URL + '?lat=' + str(lat) + '&lon=' + str(long)
    res = requests.get(URL)
    passover_time = datetime.fromtimestamp(
        res.json()["response"][1]["risetime"])
    return passover_time


def main():
    get_astronauts_information("http://api.open-notify.org/")
    iss = "iss.gif"
    # get_astronauts("http://api.open-notify.org/astros.json")
    time_stamp = get_ISS_information(
        "http://api.open-notify.org/iss-now.json")[0]
    latitude = float(get_ISS_information(
        "http://api.open-notify.org/iss-now.json")[1])
    longitude = float(get_ISS_information(
        "http://api.open-notify.org/iss-now.json")[2])

    create_world(iss, latitude, longitude)

    print(f"Latitude: {latitude}\nLongitude: {longitude}\nTime :{time_stamp}")


if __name__ == '__main__':
    main()
