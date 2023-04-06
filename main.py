import random as rd


def get_input():
    # rl = float(input("Rotational Latency: "))
    # tt = float(input("Transport Time: "))
    # tracks_per_ms = int(input("Number of Tracks per ms: "))
    # head_loc = int(input("Current Location of Header: "))
    algorithm = int(input("\nSelect algorithm:\n1-elevator    2-fcfs\n-> "))
    request = int(input("\nSelect requests:\n1-random requests   2-set requests\n-> "))

    rl = 4.17
    tt = 0.13
    tracks_per_ms = 4000
    head_loc = 8000
    if request == 1:
        requests = create_requests(tracks_per_ms, head_loc)
    else:
        requests = []
        requests_num = int(input("\nPlease enter number of requests: "))
        for i in range(requests_num):
            request = input("-> ").split(' ')
            requests.append([int(request[0]),int(request[1])])
    # requests = [[8000, 0], [24000, 0], [56000, 0], [16000, 10], [64000, 20], [40000, 30]]
    if algorithm == 1:
        elevator(rl, tt, tracks_per_ms, head_loc, requests)
    else:
        fcfs(rl, tt, tracks_per_ms, head_loc, requests)


def create_requests(tracks_per_ms, head_loc):
    requests = [[head_loc, 0], ]

    for i in range(10):
        request = rd.randrange(head_loc, 65536, tracks_per_ms)
        time = rd.randrange(0, 60, 5)
        requests.append([request, time])
    requests.sort(key=lambda x: x[1])

    print(requests)
    return requests


def elevator(rl, tt, tracks_per_ms, head_loc, requests):
    direction = None
    time = 0
    times = []
    base_delay = rl + tt
    current_loc = head_loc
    received_requests = []
    remain_requests = requests.copy()
    remain_requests.sort(key=lambda x: x[1])

    i = 0
    while i < len(remain_requests):
        if remain_requests[i][1] <= time:
            received_requests.append(remain_requests[i])
            remain_requests.remove(remain_requests[i])
            i = -1
        i += 1

    i = 0
    while i < len(received_requests):
        if direction is None:
            track = received_requests[i][0]
            if track - current_loc >= 0:
                direction = 1
            else:
                direction = -1
        else:
            track = received_requests[i][0]
            if (track - current_loc > 0 and direction == -1) or (track - current_loc < 0 and direction == 1):
                if i == len(received_requests) - 1:
                    direction *= -1
                    i = 0
                else:
                    i += 1
                continue

        distance = abs(track - current_loc)
        current_loc = track
        if distance == 0:
            time += base_delay + (distance / tracks_per_ms)
        else:
            time += base_delay + (distance / tracks_per_ms) + 1
        times.append([track, time])
        received_requests.pop(i)

        if len(remain_requests) == 0 and len(received_requests) == 0:
            break

        j = 0
        while j < len(remain_requests):
            if remain_requests[j][1] <= time:
                received_requests.append(remain_requests[j])
                remain_requests.remove(remain_requests[j])
                j = -1
            j += 1

    output(times)


def fcfs(rl, tt, tracks_per_ms, head_loc, requests):
    times = []
    time = 0
    base_delay = rl + tt
    current_loc = head_loc

    for i in range(len(requests)):
        track = requests[i][0]
        distance = abs(track - current_loc)
        current_loc = track
        if distance == 0:
            time += base_delay + (distance / tracks_per_ms)
        else:
            time += base_delay + (distance / tracks_per_ms) + 1
        times.append([track, time])
    output(times)


def output(times):
    for i in range(len(times)):
        print("Cylinder of Request: ", times[i][0], " Time Completed: ", round(times[i][1], 2))


get_input()
