from collections import defaultdict

class Endpoint:
    def __init__(self, dc_latency, latencies):
        self.dc_latency = dc_latency
        self.latencies = latencies # map cache id to latency
        self.min_latencies = latencies.items()
        self.min_latencies.sort(key=lambda x: x[1])


class Request:
    def __init__(self, video_id, endpoint_id, count):
        self.video_id = video_id
        self.endpoint_id = endpoint_id
        self.count = count


class Data:
    videos = [] # list of sizes
    endpoints = []
    requests = defaultdict(list) # from video id to request list
    cache_size = 0
    cache_count = 0


class CacheManager:
    def __init__(self, data):
        self.data = data
        self.cached = defaultdict(set) # video id to cache id-s were it is being cached
        self.init_caches()
        self.allocate_primary_caches()
        self.allocate_caches()

    def init_caches(self):
        self.caches = [Cache(i) for i in xrange(data.cache_count)]        
        
        print "init_caches: started"        
        
        for video_id in xrange(len(self.data.videos)):
            print "{} out of {}".format(video_id, len(self.data.videos))          
            
            requests = self.data.requests[video_id]

            for r in requests:
                min_latencies = self.data.endpoints[r.endpoint_id].min_latencies
                if len(min_latencies) > 0:
                    self.caches[min_latencies[0][0]].add_primary_video(video_id)
                
                for i in range(1, len(min_latencies)):
                    self.caches[min_latencies[i][0]].add_video(video_id)
        
        print "init_caches: done"

    def allocate_primary_caches(self):
        print "allocate_primary_caches: started"  

        for c in self.caches:
            print "================ {} out of {} ================".format(c.id, len(self.caches))
            
            items = [] # list of (video id, video size, gain)
            for video_id in c.primary_videos:
                video_size = self.data.videos[video_id]
                gain = self.get_latency_gain(video_id, c.id)
                items.append((video_id, video_size, gain))
            
            c.allocate(data, items, self.data.cache_size)
                
            for video_id in c.allocation:
                self.add_cached(video_id, c.id)
        
        print "allocate_primary_caches: done"

    def allocate_caches(self):
        print "allocate_caches: started"  

        for c in self.caches:
            print "================ {} out of {} ================".format(c.id, len(self.caches))
            
            items = [] # list of (video id, video size, gain)
            for video_id in c.videos:
                video_size = self.data.videos[video_id]
                gain = self.get_latency_gain(video_id, c.id)
                items.append((video_id, video_size, gain))
            
            c.allocate(data, items, self.data.cache_size)
                
            for video_id in c.allocation:
                self.add_cached(video_id, c.id)
        
        print "allocate_caches: done"  

    def add_cached(self, video_id, cache_id):
        self.cached[video_id].add(cache_id)

    def get_current_latency(self, video_id, endpoint_id):
        ep = self.data.endpoints[endpoint_id]
        current_latency = ep.dc_latency
        for c in self.cached[video_id]:
            if c in ep.latencies:
                current_latency = min(current_latency, ep.latencies[c])
                #print "getting adjusted latency {} instead of {}".format(current_latency, ep.dc_latency)
        return current_latency

    def get_latency_gain(self, video_id, cache_id):
        if video_id not in self.data.requests:
            return 0
    
        gain = 0
        for r in self.data.requests[video_id]:
            ep = self.data.endpoints[r.endpoint_id]
            if cache_id in ep.latencies:
                new_latency = ep.latencies[cache_id]
                current_latency = self.get_current_latency(video_id, r.endpoint_id)
                if new_latency < current_latency:
                    gain += r.count * (current_latency - new_latency)
        return gain # / self.videos[video_id]
        
    def get_output_caches(self):
        return [c for c in self.caches if len(c.allocation) > 0]


def get_videos_size(data, videos):
    return sum([data.videos[v] for v in videos])
            

class Cache:
    def __init__(self, id):
        self.id = id

        self.primary_videos = set()        
        self.videos = set()

        self.allocation = set()

    def add_primary_video(self, video_id):
        self.primary_videos.add(video_id)

    def add_video(self, video_id):
        self.videos.add(video_id)

    def allocate(self, data, items, cache_size):
        if len(items) == 0:
            print "nothing to allocate"
            return
        
        allocation_size = cache_size - get_videos_size(data, self.allocation)
        
        (gain, new_allocation) = self.find_allocation(items, allocation_size)
        
        print "cache id={} new allocation (gain={}, used {} out of {}): {}".format(
                self.id, gain, get_videos_size(data, new_allocation), allocation_size, new_allocation)

        self.allocation = self.allocation.union(new_allocation)
        
        print "cache id={} current allocation size={}".format(self.id, get_videos_size(data, self.allocation))

    @staticmethod
    def find_allocation(items, cache_size):
        solution = [(0, set()) for _ in xrange(cache_size+1)]
        
        for cur_size in xrange(1, cache_size+1):
            for video_id, video_size, gain in items:
                prev_size = cur_size - video_size
                if (prev_size >= 0) and (video_id not in solution[prev_size][1]):
                    new_gain = gain + solution[prev_size][0]
                    if new_gain > solution[cur_size][0]:
                        new_set = set(solution[prev_size][1])
                        new_set.add(video_id)
                        solution[cur_size] = (new_gain, new_set)

        # in case exact solution was not possible
        for i in xrange(cache_size, 0, -1):
            s = solution[i]
            if s[0] > 0:
                return s

        # no solution was found
        return (0, set())


def parser(filename):
    d = Data()
    with open(filename) as f:
        _, endp, req_count, d.cache_count, d.cache_size = map(int, f.readline().split())

        # videos (sizes): [s1, s2, s3]        
        d.videos = map(int, f.readline().split())

        # endpoints: data center latency, count of caches and each cache on separate line
        for epid in xrange(endp):
            dcl, cnt = map(int, f.readline().split())
            latencies = {}
            
            for _ in xrange(cnt):
                cache_id, latency = map(int, f.readline().split())
                latencies[cache_id] = latency
            d.endpoints.append(Endpoint(dcl, latencies))

        # for each request (video id, endpoint id, count)
        for _ in xrange(req_count):
            video_id, endpoint_id, count = map(int, f.readline().split())
            d.requests[video_id].append(Request(video_id, endpoint_id, count))

    return d


def print_results (caches, filename):
    with open(filename, 'w') as f:
        f.write("{}\n".format(len(caches)))
        for c in caches:
            f.write("{} ".format(c.id))
            f.write(" ".join(map(str, sorted(c.allocation))))
            f.write("\n")


# me_at_the_zoo
# kittens
# trending_today
# videos_worth_spreading
data = parser('trending_today.in')

cm = CacheManager(data)

print_results(cm.get_output_caches(), 'trending_today.out')
#print_videos(caches)