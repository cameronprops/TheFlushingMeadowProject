#!/usr/bin/env python3
"""WF0028 interpretive route planner. Never equate 2D AABB clearance to full navigation.
Input JSON: {"bounds":[xmin,ymin,xmax,ymax],
 "obstacles":[{"id":"wall", "bounds":[xmin,ymin,xmax,ymax]}],
 "routes":[{"id":"R1","start":[x,y],"goal":[x,y]}]}
Run: python3 plan_wf0028_alternate_routes.py input.json output.json
All dimensions in local metres. Obstacles must be chosen from collidable geometry
intersecting the pedestrian vertical range; maintain that selection upstream.
"""
import heapq
import json
import math
import sys

RADIUS = 0.45
CELL = 0.25
NEIGHBORS = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

def plan_route(bounds, obstacles, start, goal, radius=RADIUS, cell=CELL):
    xmin,ymin,xmax,ymax = map(float, bounds)
    assert xmax>xmin and ymax>ymin and cell>0 and radius>=0
    nx=int(math.ceil((xmax-xmin)/cell))+1
    ny=int(math.ceil((ymax-ymin)/cell))+1
    if nx*ny>800000:
        raise ValueError("grid too large")
    def coord(p):
        return (round((p[0]-xmin)/cell),round((p[1]-ymin)/cell))
    def world(k):
        return (xmin+k[0]*cell,ymin+k[1]*cell)
    boxes=[(o["id"],tuple(map(float,o["bounds"]))) for o in obstacles]
    def clear(k):
        if not (0<=k[0]<nx and 0<=k[1]<ny):
            return False
        x,y=world(k)
        if x>xmax or y>ymax:
            return False
        return all(not (b[0]-radius<=x<=b[2]+radius and
                        b[1]-radius<=y<=b[3]+radius) for _,b in boxes)
    a,b=coord(start),coord(goal)
    if not clear(a) or not clear(b):
        return {"status":"ENDPOINT_BLOCKED","points":[]}
    dist={a:0.}
    parent={}
    heap=[(math.dist(a,b),0,a)]
    count=0
    while heap:
        _,g,k=heapq.heappop(heap)
        if g>dist.get(k,math.inf)+1e-9:
            continue
        count+=1
        if k==b:
            nodes=[b]
            while nodes[-1]!=a:
                nodes.append(parent[nodes[-1]])
            nodes.reverse()
            pts=[list(world(v)) for v in nodes]
            pts[0]=list(start)
            pts[-1]=list(goal)
            return {"status":"CANDIDATE_ONLY","points":pts,
                    "length_m":sum(math.dist(u,v) for u,v in zip(pts,pts[1:])),
                    "explored_nodes":count}
        for dx,dy in NEIGHBORS:
            t=(k[0]+dx,k[1]+dy)
            if not clear(t):
                continue
            # A diagonal cannot pass between touching corners.
            if dx and dy and (not clear((k[0]+dx,k[1])) or
                              not clear((k[0],k[1]+dy))):
                continue
            ng=g+math.hypot(dx,dy)*cell
            if ng+1e-9<dist.get(t,math.inf):
                parent[t]=k
                dist[t]=ng
                heapq.heappush(heap,(ng+math.dist(t,b)*cell,ng,t))
    return {"status":"NO_ROUTE_AT_RESOLUTION","points":[],"explored_nodes":count}

def main(inp,out):
    data=json.load(open(inp,encoding="utf-8"))
    routes=[]
    for r in data["routes"]:
        ans=plan_route(data["bounds"],data["obstacles"],r["start"],r["goal"],
                       radius=data.get("radius_m",RADIUS),
                       cell=data.get("cell_m",CELL))
        routes.append({"id":r["id"],"start":r["start"],"goal":r["goal"],**ans})
    result={"schema":"fmp.wf0028.interpretive_alternate_routes.v001",
            "building_id":"WF0028","historical_accuracy":"UNVERIFIED",
            "navigation_certified":False,"unreal_tested":False,
            "input_obstacles":len(data["obstacles"]),"routes":routes,
            "limitations":["2D footprint screen only","Requires vertical 1.8m obstacle filter",
              "Source floor support and step elevations unverified",
              "Requires continuous swept-capsule and Unreal NavMesh checks",
              "Never deletes original architectural components"]}
    with open(out,"w",encoding="utf-8") as f:
        json.dump(result,f,indent=2)

if __name__=="__main__":
    if len(sys.argv)!=3:
        raise SystemExit("usage: plan_wf0028_alternate_routes.py input.json output.json")
    main(sys.argv[1],sys.argv[2])
