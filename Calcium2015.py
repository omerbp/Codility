__author__ = 'Omer Ben - Porat'
from collections import deque

def count_cameras(edges, depth_tree, root, allowed_diameter):
    """
    recursive function:
    stoping condition: if 'root' if a leaf
    in case it is not a leaf:
    step1: calculate the number of needed cameras in order to keep his tree with diameter at most allowed_diameter,
           and the depth of each son
    step2: for each of sons (ordered by depth): if the path the nodes creates between the sons (d1+d2+2) is greater
           than the diameter - break the edge to d1. count the number of breaks
    step3: for his last son (or the only one) - in case the path from root to his leaf is greater allowed_diameter,
           break the edge from root to son. count this break
    step4: set the depth of root as the maximum depth of his (remaining) sons, plus 1.
    step5: return the number of broken edges
    """
    if len(edges[root]) == 0:
        depth_tree[root] = 0
        return 0
    sons = edges[root].copy()
    counter = sum([count_cameras(edges, depth_tree, son, allowed_diameter) for son in sons])
    sons_depths = sorted([(son,depth_tree[son]) for son in sons], key=lambda x:x[1],reverse=True)

    for i in xrange(len(sons_depths)-1):
        if sons_depths[i][1] + sons_depths[i+1][1] + 2 > allowed_diameter:
            sons.remove(sons_depths[i][0])
            counter += 1

    if sons_depths[-1][1] + 1 > allowed_diameter:
            sons.remove(sons_depths[-1][0])
            counter += 1

    if len(sons)== 0 :
        depth_tree[root] = 0
    else:
        depth_tree[root] = max([depth_tree[son] for son in sons])+1
    return counter


def solution(A, B, K):
    """
    The solution is as follows:
    step 0: represent the graph as a directional tree
    step 1: iterate over on the possible diameter of the graph (using binary search)
        step1.1: calculate what should be the minimal number of cameras to get this diameter
                 (see count_cameras for more information)
        step1.2: in case a diameter can be achieved using less cameras than we are given, it should be considered
                 as an alternative
    step 2: out of all alternative, pick the longest diameter"""
    N = len(A)
    edges = [set() for _ in xrange(N+1)]
    for i in xrange(N):
        edges[A[i]].add(B[i])
        edges[B[i]].add(A[i])
    q = deque([0])
    while len(q) > 0: #after this loop we end up with edges as a rooted tree
        node = q.popleft()
        for son in edges[node]:
            edges[son].remove(node)
            q.append(son)

    depth_tree = [0] * (N+1)
    first = 0
    last = min(900, N)
    res = []
    while first<=last :
        midpoint = (first + last)//2
        cameras = count_cameras(edges, depth_tree,0, midpoint)
        if cameras > K:
            first = midpoint+1
        else:
            res.append(midpoint)
            last = midpoint-1

    return min(res)

#some simple tests you can use
test = ([5, 1, 0, 2, 7, 0, 6, 6, 1], [1, 0, 7, 4, 2, 6, 8, 3, 9], 2) #2
sroch = ([0,1,2,3,4],[1,2,3,4,5],1) # 2
simple = ([0,0,0,3],[1,2,3,4],2) # 1
simple2 = ([0,0,1,2,2,5],[1,2,3,4,5,6],2) #2
simple3 = ([0,0,1,1,2,2],[1,2,3,4,5,6],2) #2
print solution(*simple3)

