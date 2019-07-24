import urllib, json, dateutil.parser as dp, datetime

url = "https://api-v3.mbta.com/predictions?filter%5Bstop%5D=5296&sort=-route_id"
response = urllib.urlopen(url)
data = json.loads(response.read())

class Bus:

	def __init__(self, route_id, prediction):
		self.route_id = route_id
		self.prediction = prediction

routes = []
buses = []

def now_in_seconds():

	now = datetime.datetime.now().isoformat()
	parsed_now = dp.parse(now)
	now_in_seconds = parsed_now.strftime('%s')
	now = int(now_in_seconds)
	return now

now = now_in_seconds()

def get_routes():
	for bus in buses:
		if int(bus.route_id) not in routes:
			routes.append(int(bus.route_id))
	routes.sort()

def get_times():

	for bus in data['data']:

		route_id = bus['relationships']['route']['data']['id']
		arrival_time = bus['attributes']['arrival_time']
		parsed_arrival = dp.parse(arrival_time)
		arrival_in_seconds = int(parsed_arrival.strftime('%s')) / 60
		prediction_in_seconds = arrival_in_seconds - now / 60
		prediction = str(prediction_in_seconds)
		bus = Bus(route_id, prediction)
		buses.append(bus)

get_times()
get_routes()

print "Routes servicing your area: " + str(routes)
print "There are " + str(len(buses)) + " buses on the way to your stop."
for bus in buses:
	print "A " + bus.route_id + " bus is coming to your stop in " + bus.prediction + " minutes."