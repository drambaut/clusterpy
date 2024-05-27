import numpy as np

class AreaCl:
    """
    Area Class for Regional Clustering.
    """
    def __init__(self, id, neighs, data, variance="false"):
        """
        @type id: integer
        @param id: Id of the polygon/area

        @type neighs: list
        @param neighs: Neighborhood ids

        @type data: list.
        @param data: Data releated to the area.

        @type variance: boolean
        @keyword variance: Boolean indicating if the data have variance matrix
        """
        self.id = id
        self.neighs = neighs
        if variance == "false":
            self.data = data
        else:
            n = (np.sqrt(9 + 8 * (len(data) - 1)) - 3) / 2
            #print n
            self.var = np.matrix(np.identity(n))
            index = n + 1
            for i in range(int(n)):
                for j in range(i + 1):
                    self.var[i, j] = data[int(index)]
                    self.var[j, i] = data[int(index)]
                    index += 1
            self.data = data[0: int(n + 1)]