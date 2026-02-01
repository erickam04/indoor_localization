import numpy as np

class Wall:
    def __init__(self, x1, y1, x2, y2, attenuation=10.0):
        
        # define wall as line segment
        self.p1 = np.array([x1, y1])    # wall coordinate
        self.p2 = np.array([x2, y2])    # wall coordinate
        self.attenuation = attenuation

    def _ccw(self, p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    def is_intersect(self, beacon_pos, user_pos):
        p1, p2 = self.p1, self.p2       # wall points
        p3, p4 = beacon_pos, user_pos   # beacon and user los

        # check ccw of los on wall's point of view
        ccw1 = self._ccw(p1, p2, p3)
        ccw2 = self._ccw(p1, p2, p4)
        cond1 = (ccw1 * ccw2 < 0)

        # check ccw of wall on los's point of view
        ccw3 = self._ccw(p3, p4, p1)
        ccw4 = self._ccw(p3, p4, p2)
        cond2 = (ccw3 * ccw4 < 0)

        return cond1 and cond2


       