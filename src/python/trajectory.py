import datetime as dt

import numpy as np
from shapely.geometry import Polygon, LineString, MultiLineString
from scipy import interpolate



class Trajectory:

    def __init__(self, x, y, t):
        self.unit = 's'
        self.x = np.array(x, dtype='f8')
        self.y = np.array(y, dtype='f8')
        self.t = np.array(t, dtype='datetime64[{}]'.format(self.unit))
        seconds = []

        for time in self.t:
            timedelta =  time.item() - dt.datetime.min
            seconds.append(timedelta.total_seconds())

        self.seconds = np.array(seconds, dtype='f8')
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

    def intersection(self, geom):

        traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis],self.seconds[:, np.newaxis])))
        inter = traj.intersection(geom)

        xy = inter.coords.xy
        timestamp = []
                                #[1:-1]
        for coord in inter.coords:
            d = dt.timedelta(seconds=coord[2])
            rt = d + dt.datetime.min
            timestamp.append(rt)

        interpolator = interpolate.CloughTocher2DInterpolator(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])), self.seconds)

        timestamp[0] =  dt.timedelta(seconds=float(interpolator(xy[0][0],xy[1][0]))) + dt.datetime.min
        timestamp[timestamp.__len__()-1] = dt.timedelta(seconds=float(interpolator(xy[0][xy[0].__len__()-1], xy[1][xy[1].__len__() - 1]))) + dt.datetime.min

        return Trajectory(xy[0],xy[1],timestamp)


    def difference(self, geom):
        traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])))
        return traj.difference(geom)
    #
    # def boundary(self):
    #     traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])))
    #     return traj.bounds



