import numpy as np
from geojson.geometry import MultiPolygon
from shapely.geometry import Polygon, LineString, MultiLineString
from scipy import interpolate


class Trajectory:
    def __init__(self, x, y, t):

        self.unit = 's'
        self.x = np.array(x, dtype='f8')
        self.y = np.array(y, dtype='f8')
        self.t = np.array(t, dtype='M8[s]'.format(self.unit))
        self.seconds = (self.t - np.datetime64("1970-01-01 00:00:00")) / np.timedelta64(1, 's')

        self._t = {str(v): i for i, v in enumerate(t)}

    def __getitem__(self, t):
        t = np.datetime64(t, unit=self.unit)
        try:
            i = self._t[str(t)]
            return self.x[i], self.y[i]
        except KeyError:
            # interpolate?
            pass

    def __str__(self):
        i = 10
        result = ""
        for v in zip(self.x, self.y, self.t):
            result += str(v) + "\n"
            i -= 1
            if i == 0:
                result += "..."
                break
        return result

    def __repr__(self):
        return self.__str__()

    def __setitem__(self, t, point):
        t = np.datetime64(t, unit=self.unit)
        try:
            i = self._t[str(t)]
            self.x[i] = point[0]
            self.y[i] = point[1]
        except KeyError:
            # interpolate?
            pass

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getTime(self):
        return self.seconds

    def begins(self):
        return self.t[0]

    def ends(self):
        return self.t[-1]

    def after(self, t):
        t = np.datetime64(t, unit=self.unit)
        mask = self.t > t
        result = Trajectory(self.x[mask], self.y[mask], self.t[mask])
        return result

    def before(self, t):
        t = np.datetime64(t, unit=self.unit)
        mask = self.t < t
        result = Trajectory(self.x[mask], self.y[mask], self.t[mask])
        return result

    def during(self, t1, t2):
        t1 = np.datetime64(t1, unit=self.unit)
        t2 = np.datetime64(t2, unit=self.unit)
        mask = ((self.t > t1) & (self.t < t2))
        result = Trajectory(self.x[mask], self.y[mask], self.t[mask])
        return result

    def intersection_shapely(self,geom):
        traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis], self.seconds[:, np.newaxis])))
        return traj.intersection(geom)

    def to_Trajectory(self, inter):

        if isinstance(inter, MultiLineString) or isinstance(inter, MultiPolygon):
            array_traj = []
            for multi in inter:
                array_traj.append(self.__set_data__(multi))

            return array_traj

        return self.__set_data__(inter)

    def interpolate_middle_xyt(self,xyt):

        x = (xyt[0][0] + xyt[1][0]) / 2
        y = (xyt[0][1] + xyt[1][1]) / 2
        t = (xyt[0][2] + xyt[1][2]) / 2
        traj_inter = np.array([x, y, t], dtype='f8')

        return  np.insert(xyt, 1, traj_inter, axis=0)


    def __set_data__(self, inter):

        xy = np.array(inter)

        # xy[0][2] = self.interpolator(xy[0][0], xy[0][1])
        #
        # xy[-1][2] = self.interpolator(xy[-1][0], xy[-1][1])

        # if (xy.size <= 6):
        #     xy = self.interpolate_middle_xyt(xy)

        timestamp = xy[:, 2] * np.timedelta64(1, 's') + np.datetime64("1970-01-01 00:00:00")

        return Trajectory(xy[:,0], xy[:,1], timestamp)


    def difference(self, geom):
        traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])))
        return traj.difference(geom)

        # def boundary(self):
        #     traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])))
        #     return traj.bounds

#
# traj = Trajectory([0,2,3,5],
#                   [0,2,2,4],
#                ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00","2000-04-01 00:01:00"])#
#
#
# traj = Trajectory([1, 2, 3, 5],
#                   [0, 2, 2, 4],
#                ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00","2000-04-01 00:01:00"])
#
# polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
# # # # polygon = Polygon([(1, 1), (1, 3), (2.5, 3), (2.5, 1), (1, 1)])
#
# polygon = Polygon([(1,1), (1, 3), (4, 3), (4, 1), (1,1)])
# #
# print(traj.intersection(polygon))
# #


# traj = Trajectory([1, 2, 2, 3, 3, 4, 5, 5, 3, 3],
#                   [0, 2, 4, 4, 2, 2, 2, 1, 1, 2],
#                   ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00", "2000-04-01 00:01:00"
#                       , "2000-05-01 00:01:00", "2000-06-01 00:01:00", "2000-07-01 00:01:00", "2000-08-01 00:01:00"
#                       , "2000-09-01 00:01:00", "2000-10-01 00:01:00"])
#
# polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
#
# print(traj.intersection(polygon))

