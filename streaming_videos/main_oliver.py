from operator import attrgetter
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
    maxLossCosts = []
    Xmul = 1
    Ymul = 3
    Zmul = 5


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

class LossCost:
    def __init__(self, cost, cacheId):
        self.cost = cost
        self.cacheId = cacheId
        self.videoId = -1

def getLossFromNotInsertingVideoToCache(data,cacheId, endpoint_id, request_count):
    loss = 0
    ep = data.endpoints[endpoint_id]
    if cacheId in ep.latencies:
        latency = ep.latencies[cacheId]
        loss += request_count * (ep.dc_latency - latency)
    return loss

def getCacheLossCost_CacheArray(data, video_id):
    lossCostArray = [LossCost(0, -1) for _ in range(data.cache_count)]
    print("processing requests for video: " + str(video_id))
    for request in data.requests:
        if(request.video_id == video_id):
            loopcacheId = 0
            while loopcacheId < data.cache_count:
                if(lossCostArray[loopcacheId].cacheId != loopcacheId):
                    lossCostArray[loopcacheId].cacheId = loopcacheId
                lossCostArray[loopcacheId].cost += getLossFromNotInsertingVideoToCache(data,loopcacheId, request.endpoint_id, request.count)
                loopcacheId += 1
    #print(' , '.join(str(e.cost) for e in lossCostArray))
    return getBiggestCacheLoss(lossCostArray)

def getSorter(item):
    return item.cost

def getBiggestCacheLoss(lossCostArray):
    return max(lossCostArray, key=attrgetter('cost'))


def getSaved(data, count, endpoint_id, video_id):
    best_saved = 0
    ep = data.endpoints[endpoint_id]
    for cacheId in ep.latencies:
        if(video_id in data.caches[cacheId].videos):
            latency = ep.latencies[cacheId]
            saved = count * (ep.dc_latency - latency)
            if saved > best_saved:
                 best_saved = saved
    return best_saved

def calculateScore(data):
    score = 0
    req_count = 0
    for request in data.requests:
        req_count += request.count
        score += getSaved(data, request.count, request.endpoint_id, request.video_id)
    return score*1000/req_count






def main():
    data = parser('streaming_videos/me_at_the_zoo.in')
    for video_id in range(0,data.videos.__len__()):
        temp = getCacheLossCost_CacheArray(data, video_id)
        temp.videoId = video_id
        data.maxLossCosts.append(temp)
    data.maxLossCosts.sort(key=lambda x: x.cost, reverse=True)
    print(' x '.join(str(e.cost) for e in data.maxLossCosts))

    caches = []
    cachesMem = [data.cache_size]* data.cache_count
    totalMem = data.cache_count * data.cache_size
    res_i = 0

    skiplist = []
    while res_i < data.maxLossCosts.__len__():
        vidSize = data.videos[data.maxLossCosts[res_i].videoId]
        if data.maxLossCosts[res_i].cost == 0 or totalMem < vidSize:
            print("cost 0, exiting")
            break

        if cachesMem[data.maxLossCosts[res_i].cacheId] >= vidSize:
            #print("insert")
            cachesMem[data.maxLossCosts[res_i].cacheId] -= vidSize
            totalMem -= vidSize
            data.caches[data.maxLossCosts[res_i].cacheId].videos.append(data.maxLossCosts[res_i].videoId)
            skiplist.append(res_i)

        res_i +=1

    print("out")

    res_i = 0
    while res_i < data.maxLossCosts.__len__():
        vidSize = data.videos[data.maxLossCosts[res_i].videoId]
        if data.maxLossCosts[res_i].cost == 0 or totalMem < vidSize:
            print("out of mems")
            break

        for i in range(0,data.cache_count):
            if cachesMem[i] >= vidSize:
                cachesMem[i] -= vidSize
                totalMem -= vidSize
                if(data.maxLossCosts[res_i].videoId in data.caches[i].videos):
                    continue
                data.caches[i].videos.append(data.maxLossCosts[res_i].videoId)

        res_i += 1

    print("done")
    print_results(data.caches)
    print(calculateScore(data))
main()

#class Cache:
#    def __init__(self, id, videos):
 #       self.id = id
 #       self.videos = videos