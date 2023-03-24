import random as rd


def get_input():
    rl = float(input("Rotational Latency: "))
    tt = float(input("Transport Time: "))
    tracks_per_ms = int(input("Number of Tracks per ms: "))
    head_loc = int(input("Current Location of Header: "))
    requests = create_requests(tracks_per_ms, head_loc)
    # requests = {8000: 0, 24000: 0, 56000: 0, 16000: 10, 64000: 20, 40000: 30}
    # elevator(rl, tt, tracks_per_ms, head_loc, requests)
    fcfs(rl, tt, tracks_per_ms, head_loc, requests)


def create_requests(tracks_per_ms, head_loc):
    requests = {head_loc: 0, }
    keys = []
    values = []

    i = 0
    while i < 10:
        key = rd.randrange(head_loc, 65536, tracks_per_ms)
        value = rd.randrange(0, 60, 5)
        if key not in keys and value not in values:
            keys.append(key)
            values.append(value)
            i += 1

    values.sort()
    for j in range(10):
        requests.update({keys[j]: values[j]})

    print(requests)

    return requests


def elevator(rl, tt, tracks_per_ms, head_loc, requests):
    direction = "left"


def fcfs(rl, tt, tracks_per_ms, head_loc, requests):
    times = []
    time = 0
    base_delay = rl + tt
    current_loc = head_loc

    for i in range(10):
        track = list(requests.keys())[i]
        distance = abs(track - current_loc)
        current_loc = track
        if i == 0:
            time += base_delay + (distance / tracks_per_ms)
        else:
            time += base_delay + (distance / tracks_per_ms) + 1
        times.append(time)

    output(requests, times)


def output(requests, times):
    for i in range(10):
        print("Cylinder of Request: ", list(requests.keys())[i], " Time Completed: ", times[i])


get_input()
