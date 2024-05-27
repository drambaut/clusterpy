from Clusterpy.core.toolboxes.cluster.componentsAlg.areacl import AreaCl
from Clusterpy.core.toolboxes.cluster.componentsAlg.dist2Regions import distanceStatDispatcher

class AreaManagerNodes:
    """
    This class contains operations at areal level, including the generation of
    instances of areas, a wide range of area2area and area2region distance
    functions.
    """
    #AreaManagerNodes(w, y, Dij, Cio, distanceType)
    def __init__(self, w, y, distanceType="EuclideanSquared", variance="false", Dij={}, Cij={}):
        """
        @type w: dictionary
        @param w: With B{key} = area Id, and B{value} = list with Ids of neighbours of
        each area.

        @type y: dictionary
        @param y: With B{key} = area Id, and B{value} = list with attribute
        values.

        @type distanceType: string
        @keyword distanceType: Function to calculate the distance between areas. Default value I{distanceType = 'EuclideanSquared'}.

        @type variance: boolean
        @keyword variance: Boolean indicating if the data have variance matrix. Default value I{variance = 'false'}.
        """
        self.y = y
        self.areas = {}
        self.noNeighs = set([])
        self.variance = variance
        self.distanceType = distanceType
        self.createAreas(w, y, Dij)
        self.distanceStatDispatcher = distanceStatDispatcher


    def getDistance2Region(self, area, areaList, distanceStat="Centroid", weights=[], indexData=[], Dij = {}, Cio = {}, seeds = []):
        """
        Returns the distance from an area to a region (defined as a list of
        area IDs)
        """
        if isinstance(distanceStat, str):
            #print 'Index Data Stat', len(indexData)
            if len(indexData) == 0:
                indexData = range(len(area.data))
            #print self.distanceStatDispatcher[distanceStat](self, area, areaList, indexData, Dij, Cio)
            return self.distanceStatDispatcher[distanceStat](self, area, areaList, indexData, Dij, Cio, seeds)
        else:
            distance = 0.0
            i = 0
            for dS in distanceStat:
                if len(indexData) == 0:
                    indexDataDS = range(len(area.data))
                else:
                    indexDataDS = indexData[i]
                if len(weights) > 0:
                    distance += weights[i]
                    self.distanceStatDispatcher[dS](self, area, areaList, indexDataDS)
                else:
                    distance += self.distanceStatDispatcher[dS](self, area, areaList, indexDataDS)
                i += 1
            return distance