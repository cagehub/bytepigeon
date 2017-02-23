class Endpoint:
    def __init__(self, dc_latency, latencies):
        self.dc_latency = dc_latency
        self.latencies = latencies # list of tuples of id and latency e.g. (1, 500)

class Request:
    def __init__(self, count, video_id, endpoint_id):
        self.count = count
        self.video_id = video_id
        self.endpoint_id = endpoint_id

class Cache:
    def __init__(self, size, videos):
        self.videos = videos


videos = [] # list of sizes
endpoints = []
requests = []

cache_size = 0
cache_count = 0
caches = []

