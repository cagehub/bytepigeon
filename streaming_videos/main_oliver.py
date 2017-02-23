class Latency:
    def __init__(self, ep_id, latency):
        self.endpoint_id = ep_id
        self.latency = latency


class Endpoint:
    def __init__(self, dc_latency, latencies):
        self.dc_latency = dc_latency
        self.latencies = latencies  # list of Latency


class Request:
    def __init__(self, video_id, endpoint_id, count):
        self.video_id = video_id
        self.endpoint_id = endpoint_id
        self.count = count


class Cache:
    def __init__(self, size, videos):
        self.videos = videos


class Data:
    videos = []  # list of sizes
    endpoints = []
    requests = []
    cache_size = 0
    cache_count = 0


def parser(filename):
    d = Data()
    with open(filename) as f:
        _, endp, reqs, d.cache_count, d.cache_size = map(int, f.readline().split())
        d.videos = map(int, f.readline().split())

        for _ in range(endp):
            dcl, cnt = map(int, f.readline().split())
            latencies = []
            for _ in range(cnt):
                ep_id, latency = map(int, f.readline().split())
                latencies.append(Latency(ep_id, latency))
            d.endpoints.append(Endpoint(dcl, latencies))

        for _ in range(reqs):
            video_id, endpoint_id, count = map(int, f.readline().split())
            d.requests.append(Request(video_id, endpoint_id, count))
    return d


data = parser('me_at_the_zoo.in')

class LossCost:
    def __init__(self, cost, cacheId):
        self.cost = cost
        self.cacheId = cacheId


videos = [] # list of sizes
endpoints = []
requests = []

cache_size = 0
cache_count = 0

Xmul = 1
Ymul = 3
Zmul = 5

maxLossCosts = []
lossCostArray = []

def getCacheLossCost_CacheArray(video):
    for request in requests:
        cacheId = 0
        while cacheId < cache_count:
            lossCostArray[]

    lossCostArray[]
    return (LossCost(10,2), LossCost(5,3), LossCost(232,30))

def getSorter(item):
    return item.cost

def getMaxLossCost(lossCost_CacheArray):
    return sorted(lossCost_CacheArray, key=getSorter, reverse=True)[0]

def main():
    for video in videos:

        maxLossCosts.append(getMaxLossCost(getCacheLossCost_CacheArray(video)))
    print(maxLossCosts[0].cost)
main()
