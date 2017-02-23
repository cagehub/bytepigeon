import random

class Latency:
    def __init__(self, ep_id, latency):
        self.endpoint_id = ep_id
        self.latency = latency


class Endpoint:
    def __init__(self, dc_latency, latencies):
        self.dc_latency = dc_latency
        self.latencies = latencies  # map cache id to latency


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
    maxLossCosts = []
    Xmul = 1
    Ymul = 3
    Zmul = 5


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


data = parser('streaming_videos/me_at_the_zoo.in')

class LossCost:
    def __init__(self, cost, cacheId):
        self.cost = cost

def getLossFromNotInsertingVideoToCache(data,cacheId, endpoint_id, request_count):
    loss = 0
    ep = data.endpoints[endpoint_id]
    if cacheId in ep.latencies:
        latency = ep.latencies[cacheId]
        loss += request_count * (ep.dc_latency - latency)
    return loss

def getCacheLossCost_CacheArray(data, video_id):
    lossCostArray = [0]*data.cache_count
    for request in data.requests:
        if(request.video_id == video_id):
            cacheId = 0
            while cacheId < data.cache_count:
                lossCostArray[cacheId] += getLossFromNotInsertingVideoToCache(data,cacheId, request.endpoint_id, request.count)
    return getBiggestCacheLoss(lossCostArray)

# getSorter(item):
 #   return item.cost

def getBiggestCacheLoss(lossCostArray):
    return sorted(lossCostArray, reverse=True)[0]

def main(data):
    for video_id in range(0,data.videos.__len__()):
        data.maxLossCosts.append(getCacheLossCost_CacheArray(data, video_id))
    print(''.join(str(e) for e in data.maxLossCosts))

main(data)
