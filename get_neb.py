from ray_casting import *

class NebChecker:
    def __init__(self,rows):
        self.polys = []
        edges = []

        prev_neigh = None
        prev_coord = None
        poly_name  = None

        for row in rows:
            if prev_neigh == None:
                prev_neigh = row[0]
                prev_coord = (row[-2],row[-1])
                poly_name  = row[4]
            elif (row[0] <> prev_neigh):
                self.polys.append(Poly(name=poly_name,edges=edges))
                prev_neigh = row[0]
                prev_coord = (row[-2],row[-1])
                poly_name  = row[4]
                edges = []
            else:
                edges.append(Edge(a=Pt(x=prev_coord[0],y=prev_coord[1]),b=Pt(x=row[-2],y=row[-1])))
                prev_coord = (row[-2],row[-1])

    def get_neb(self,lon,lat):
        for poly in self.polys:
            if ispointinside(Pt(x=float(lon),y=float(lat)),poly):
                return poly[0]
        return "other"