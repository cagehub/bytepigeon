class Endpoint:
    def __init__(self, dc_latency, latencies):
        self.dc_latency = dc_latency
        self.latencies = latencies # list of tuples of id and latency e.g. (1, 500)

class Request:
    def __init__(self, count, video_id, endpoint_id):
        self.count = count
        self.video_id = video_id
        self.endpoint_id = endpoint_id

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


def getCacheLossCost_CacheArray(video):
    
    endPointsWithVideo =
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
