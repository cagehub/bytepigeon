import time

class Endpoint:
    def __init__(self, dc_latency, latencies):
        self.dc_latency = dc_latency
        self.latencies = latencies # map cache id to latency

class Request:
    def __init__(self, video_id, endpoint_id, count):
        self.video_id = video_id
        self.endpoint_id = endpoint_id
        self.count = count

class Cache:
    def __init__(self, cache_id, size):
        self.id = cache_id
        self.videos = {}
        self.remaining_size = size

    def add(self, video_id, video_size):
        if video_id not in self.videos:
            if self.remaining_size - video_size >= 0:
                self.videos[video_id] = True
                self.remaining_size -= video_size
                return True
            else:
                return False
        return True

    def is_empty(self):
        return not self.videos

class Data:
    videos = [] # list of sizes
    endpoints = []
    requests = {} # from video to request list
    cache_size = 0
    cache_count = 0

def parser(filename):
    d = Data()
    caches = {}
    with open(filename) as f:
        _, endp, reqs, d.cache_count, d.cache_size = map(int, f.readline().split())
        d.videos = map(int, f.readline().split())
        
        for _ in range(endp):
            dcl, cnt = map(int, f.readline().split())
            latencies = {}
            for _ in range(cnt):
                cache_id, latency = map(int, f.readline().split())
                latencies[cache_id] = latency
                if cache_id not in caches:
                    caches[cache_id] = 1
                else:
                    caches[cache_id] += 1
            d.endpoints.append(Endpoint(dcl, latencies))

        for _ in range(reqs):
            video_id, endpoint_id, count = map(int, f.readline().split())
            if video_id in d.requests:
                d.requests[video_id].append(Request(video_id, endpoint_id, count))
            else:
                d.requests[video_id] = [Request(video_id, endpoint_id, count)]
    return d, caches

def print_results (caches, filename):
    out_file = open (filename, "w")
    out_file.write(str(len(caches)))
    out_file.write("\n")

    for c in caches:
        out_file.write(str(c.id))
        for v in c.videos:
            out_file.write(" " + str (v))
        out_file.write("\n")
    out_file.close()

def get_latency_gain(data, video_id, cache_id, count):
    gain = 0
    if video_id not in data.requests:
        return 0

    reqs = data.requests[video_id]
    for r in reqs:
        ep = data.endpoints[r.endpoint_id]
        if cache_id in ep.latencies:
            latency = ep.latencies[cache_id]
            gain += r.count * (ep.dc_latency - latency) * count
    return gain

# me_at_the_zoo
# kittens
# trending_today
# videos_worth_spreading
data, caches = parser('trending_today.in')

gain = []
for v_id in range(len(data.videos)):
    t0 = time.time()
    print "{} of {}".format(v_id, len(data.videos))
    vid_gain = []
    for c_id in range(data.cache_count):
        vid_gain.append((c_id, get_latency_gain(data, v_id, c_id, caches[c_id])))
    vid_gain.sort(key=lambda x: x[1], reverse=True)
    gain.append(vid_gain)
    print "took {} seconds".format(time.time() - t0)


gain.sort(key=lambda x: x[0][1], reverse=True)

caches = [Cache(i, data.cache_size) for i in range(data.cache_size)]

CACHES_MAX = 1

for vid_id in range(len(gain)):
    caches_used = 0
    for i in range(data.cache_count):
        if len(gain[vid_id]) > 0:
            cache_id = gain[vid_id][i][0]
            if caches[cache_id].add(vid_id, data.videos[vid_id]):
                caches_used += 1
        if caches_used >= CACHES_MAX:
            break

output_caches = [c for c in caches if not c.is_empty()]
print_results(output_caches, "trending_today.out")

        
