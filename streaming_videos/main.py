class Endpoint:
    def __init__(self, dc_latency, latencies):
        self.dc_latency = dc_latency
        self.latencies = {} # map cache id to latency

class Request:
    def __init__(self, video_id, endpoint_id, count):
        self.video_id = video_id
        self.endpoint_id = endpoint_id
        self.count = count

class Cache:
    def __init__(self, id, videos):
        self.id = id
        self.videos = videos

class Data:
    videos = [] # list of sizes
    endpoints = []
    requests = []
    caches = []
    cache_size = 0
    cache_count = 0

def parser(filename):
    d = Data()
    with open(filename) as f:
        _, endp, reqs, d.cache_count, d.cache_size = map(int, f.readline().split())
        d.videos = map(int, f.readline().split())

        for c_id in range(d.cache_count):
            d.caches.append(Cache(c_id, []))
        
        for _ in range(endp):
            dcl, cnt = map(int, f.readline().split())
            latencies = {}
            for _ in range(cnt):
                cache_id, latency = map(int, f.readline().split())
                latencies[cache_id] = latency
            d.endpoints.append(Endpoint(dcl, latencies))

        for _ in range(reqs):
            video_id, endpoint_id, count = map(int, f.readline().split())
            d.requests.append(Request(video_id, endpoint_id, count))
    return d

def print_results (caches):
    out_file = open ("result.out", "w")
    out_file.write(str(len(caches)))
    out_file.write("\n")

    for c in caches:
        out_file.write(str(c.id))
        for v in c.videos:
            out_file.write(" " + str (v))
        out_file.write("\n")
    out_file.close()

def get_latency_gain(data, video_id, cache_id):
    gain = 0
    vid_requests = [r for r in data.requests if r.video_id == video_id]
    for r in vid_requests:
        ep = data.endpoints[r.endpoint_id]
        if cache_id in ep.latencies:
            latency = ep.latencies[cache_id]
            gain += r.count * (ep.dc_latency - latency)
    return gain

data = parser('me_at_the_zoo.in')

#print get_latency_gain(data, 0, 0)

print_results(data.caches)

        
