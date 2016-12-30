import json
import time

class Stats():
    """ Stores statistics for the miner program """
    def __init__(self):
        """ The overall data """
        self.users = {}
        self.overall_start_time = time.time()
        self.init()

    def init(self):
        """ The data for each run """
        self.currentuser = None
        self.rounds = 0
        self.sleep_total = 0
        self.drops = []
        self.data = {}
        self.initial_points = 0
        self.start_time = 0
        self.points = 0

    def start(self, points, username):
        if self.users.get(username) == None and self.users.get(username) == None:
            self.currentuser = username
            self.users[username] = {}
            self.initial_points = points
            self.start_time = time.time()
        else:
            raise Exception("%s is already registered or running." % str(self.currentuser))

    def sleep(self, seconds):
        """ uses invocations of this sleep method as the count of rounds
            sleep_total used to generate average sleep time
        """
        self.sleep_total += seconds

    def round(self, points):
        self.rounds += 1
        self.points = points

    def increase(self, points):
        """ When the points go up """
        self.points = points

    def decrease(self, points):
        """ When the points go down """
        if points >= self.points:
            return
        self.drops.push(self.points - points)
        self.points = points

    def done(self):
        """ Generate the stats and json object
            Clears out old data
        """
        self.end_time = time.time()
        self.data["user"] = self.currentuser
        self.data["total time"] = self.end_time - self.start_time
        self.data["initial points"] = self.initial_points
        self.data["total points"] = self.points
        self.data["points gained"] = self.points - self.initial_points
        self.data["rounds"] = self.rounds
        self.data["avg sleep time"] = self.sleep_total / (float(self.rounds) or 1)
        self.data["drops"] = len(self.drops)
        if len(self.drops) > 0:
            self.data["drop avg"] = sum(self.drops) / (float(len(self.drops)) or 1)
            self.data["drop total"] = sum(self.drops)
        self.users[self.currentuser] = self.data
        self.init()

    def get_json(self):
        overall = {}
        overall["total time"] = time.time() - self.overall_start_time
        overall["accounts"] = self.users
        return json.dumps(overall)
