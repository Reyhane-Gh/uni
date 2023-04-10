import random as rd
import sys


def select_algorithm():
    try:
        algorithm = int(input("Select algorithm:\n1-elevator    2-fcfs    3-both\n-> "))

        if algorithm == 1:
            Elevator()
        elif algorithm == 2:
            Fcfs()
        else:
            elevator = Elevator()
            fcfs = Fcfs(elevator.requests, elevator.tracks_per_ms, elevator.head_loc, elevator.base_delay)
            print(f'\nelevator finish time: {round(elevator.time, 2)}\nfcfs finish time: {round(fcfs.time, 2)}')

    except Exception as e:
        print('wrong input: ', e)
        sys.exit(-1)


class DiskScheduling:
    def __init__(self, *args):
        try:
            self.requests = []
            self.times = []
            self.time = 0

            if len(args) == 0:
                rl = float(input("Rotational Latency: "))
                tt = float(input("Transport Time: "))
                self.tracks_per_ms = int(input("Number of Tracks per ms: "))
                self.head_loc = int(input("Current Location of Header: "))
                self.base_delay = rl + tt
                self.current_loc = self.head_loc
                self.set_requests()
            else:
                self.requests = args[0]
                self.tracks_per_ms = args[1]
                self.head_loc = args[2]
                self.base_delay = args[3]

            self.current_loc = self.head_loc
        except Exception as e:
            print('wrong input: ', e)
            sys.exit(-1)

    def set_requests(self):
        try:
            request = int(input("\nSelect requests:\n1-random requests   2-set requests\n-> "))
            if request == 1:
                requests_num = int(input("\nPlease enter number of requests: "))
                self.create_requests(requests_num)
            else:
                requests_num = int(input("\nPlease enter number of requests: "))
                print('Enter requests:(Ex: 24000 2)')
                for i in range(requests_num):
                    request = input("-> ").split(' ')
                    self.requests.append([int(request[0]), int(request[1])])
        except Exception as e:
            print('wrong input: ', e)
            sys.exit(-1)

    def create_requests(self, requests_num):
        try:
            self.requests = [[self.head_loc, 0], ]
            time_range = int(input("Please enter range of time: "))

            for i in range(requests_num - 1):
                request = rd.randrange(0, 65536, self.tracks_per_ms)
                time = rd.randrange(0, time_range, 10)
                self.requests.append([request, time])
            self.requests.sort(key=lambda x: x[1])

            self.print_request()
        except Exception as e:
            print('wrong input: ', e)
            sys.exit(-1)

    def print_request(self):
        print('requests:')
        for request in self.requests:
            print(f"{request[0]}{' ' * (10 - len(str(request[0])))}{request[1]}")
        print('*' * 50)

    def output(self, name):
        print(f'\n{name} algorithm')
        for i in range(len(self.times)):
            print("Cylinder of Request: ", self.times[i][0], " Time Completed: ", round(self.times[i][1], 2))
        print('*' * 50)


class Elevator(DiskScheduling):
    def __init__(self):
        super().__init__()
        self.direction = None
        self.received_requests = []
        self.remain_requests = self.requests.copy()
        self.remain_requests.sort(key=lambda x: x[1])

        self.elevator()

    def elevator(self):
        self.receive_request()
        while True:
            min_dis, min_i = self.find_min_dis()

            if min_dis == sys.maxsize:
                self.time = self.remain_requests[0][1]
                self.receive_request()
                continue

            track = self.received_requests[min_i][0]
            if self.direction is None:
                if track - self.current_loc > 0:
                    self.direction = 1
                elif track - self.current_loc < 0:
                    self.direction = -1

            distance = abs(track - self.current_loc)
            self.current_loc = track
            if distance == 0:
                self.time += self.base_delay + (distance / self.tracks_per_ms)
            else:
                self.time += self.base_delay + (distance / self.tracks_per_ms) + 1
            self.times.append([track, self.time])
            self.received_requests.pop(min_i)

            if len(self.remain_requests) == 0 and len(self.received_requests) == 0:
                break
            self.receive_request()
        self.output('Elevator')

    def find_min_dis(self):
        min_dis = sys.maxsize
        min_i = 0
        i = 0
        while i < len(self.received_requests):
            track = self.received_requests[i][0]
            distance = abs(track - self.current_loc)
            if distance < min_dis:
                if (track - self.current_loc > 0 and self.direction == -1) or (
                        track - self.current_loc < 0 and self.direction == 1):
                    if i == len(self.received_requests) - 1 and min_dis == sys.maxsize:
                        self.direction *= -1
                        i = 0
                        continue
                    else:
                        i += 1
                        continue
                min_dis = distance
                min_i = i
            i += 1
        return min_dis, min_i

    def receive_request(self):
        i = 0
        while i < len(self.remain_requests):
            if self.remain_requests[i][1] <= self.time:
                self.received_requests.append(self.remain_requests[i])
                self.remain_requests.remove(self.remain_requests[i])
                i = -1
            i += 1


class Fcfs(DiskScheduling):
    def __init__(self, *args):
        super().__init__(*args)
        self.fcfs()

    def fcfs(self):
        for i in range(len(self.requests)):
            track = self.requests[i][0]
            distance = abs(track - self.current_loc)
            self.current_loc = track
            if distance == 0:
                self.time += self.base_delay + (distance / self.tracks_per_ms)
            else:
                self.time += self.base_delay + (distance / self.tracks_per_ms) + 1
            self.times.append([track, self.time])
        self.output('Fcfs')


select_algorithm()
