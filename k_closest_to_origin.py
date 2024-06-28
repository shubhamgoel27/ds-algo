import heapq 
class Solution:

    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []
        for i,(x,y) in enumerate(points):
            dist = x**2 + y**2 
            heapq.heappush(heap, (dist,i))
        res = []
        for i in range(k):
                dist, i = heapq.heappop(heap)
                res.append(points[i])
        return res
