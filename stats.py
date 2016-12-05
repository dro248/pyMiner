import json
import time

class Stats():
    """ Stores statistics for the miner program """
    def __init__(self, store=False):
        # add in total time of run
        self.store = store
        self.rounds = 0
        self.sleep_total = 0
        self.drops = []
        self.data = {}
        self.initial_points = 0
        self.start_time = 0
        self.title = ""
        self.points = 0

    def start(self, points):
        self.initial_points = points
        self.start_time = time.time()

    def set_title(self, title):
        self.title = title

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
        """ Generate the stats and json object """
        self.end_time = time.time()
        self.data["title"] = self.title
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
        return json.dumps(self.data)

    def get_json(self):
        return json.dumps(self.data)

