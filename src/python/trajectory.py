import datetime
import numpy as np
from shapely.geometry import Polygon, asLineString, MultiPoint


class Trajectory:

    def __init__(self, x, y, t, unit='D'):
        self.unit = unit
        self.x = np.array(x, dtype='f8')
        self.y = np.array(y, dtype='f8')
        self.t = np.array(t, dtype='datetime64[{}]'.format(unit))

        # dt = np.dtype([('x','f8'),('y','f8'),('t','datetime64[{}]'.format(unit))])
        # #,('t','datetime64[{}]'.format(unit))
        # self.all = np.array(list(zip(self.x,self.y,self.t)), dtype=dt)

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

    def begins(self):
        return self.t[0]

    def ends(self):
        return self.t[-1]

    def after(self, t):
        t = np.datetime64(t, unit=self.unit)
        mask = self.t > t
        result = traj_py(self.x[mask], self.y[mask], self.t[mask])
        return result

    def before(self, t):
        t = np.datetime64(t, unit=self.unit)
        mask = self.t < t
        result = traj_py(self.x[mask], self.y[mask], self.t[mask])
        return result

    def during(self, t1, t2):
        t1 = np.datetime64(t1, unit=self.unit)
        t2 = np.datetime64(t2, unit=self.unit)
        mask = ((self.t > t1) & (self.t < t2))
        result = traj_py(self.x[mask], self.y[mask], self.t[mask])
        return result

    def intersection(self, geom, startTime, endTime):

        time = np.array([startTime, endTime], dtype='datetime64[{}]'.format('D'))

        traj = MultiPoint(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])))
        cont = 0

        trajF = []

        for point in traj:
            ref = geom.intersection(point)
            if ref.is_empty == False and time[0] <= self.t[cont] <= time[1]:
                trajF.append(ref)

        return MultiPoint(trajF)

    def difference(self, geom):
        traj = asLineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])))
        return traj.difference(geom)

    def boundary(self):
        traj = asLineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])))
        return traj.bounds


traj = traj_py([1, 2, 3, 5],
               [0, 2, 2, 4],
               ["2000-01-01", "2000-02-01", "2000-03-01", "2000-04-01", "2000-05-01"])

traj["2000-02-01"]
# (2.0, 2.0)
#
# #
polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])

timeS = datetime.datetime(2000, 1, 1, 15, 14, 12)
timeE = datetime.datetime(2000, 4, 1, 15, 14, 12)

print(traj.intersection(polygon, timeS, timeE))

