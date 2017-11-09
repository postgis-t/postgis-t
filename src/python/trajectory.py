import datetime as dt

import numpy as np
from geojson.geometry import MultiPolygon
from scipy.spatial.qhull import ConvexHull
from shapely.geometry import Polygon, LineString, MultiLineString
from scipy import interpolate


class Trajectory:
    def __init__(self, x, y, t, interpolator=1):

        self.unit = 's'
        self.x = np.array(x, dtype='f8')
        self.y = np.array(y, dtype='f8')
        self.t = np.array(t, dtype='M8[s]'.format(self.unit))
        # self.size = self.t.argsort().argsort()

        self.seconds = (self.t - np.datetime64("1970-01-01 00:00:00")) / np.timedelta64(1, 's')


        if interpolator == 1:
            #print(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])))
            self.interpolator = interpolate.LinearNDInterpolator(
                np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])), self.seconds)

            # Trigonomial
        elif interpolator == 2:
            self.interpolator = interpolate.CloughTocher2DInterpolator(
                np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])), self.seconds)

        elif interpolator == 3:
            self.interpolator = interpolate.NearestNDInterpolator(
                np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])), self.seconds)

        elif interpolator == 4:
            self.interpolator = interpolate.interp2d(
                self.x, self.y, self.seconds)

        elif interpolator == 5:
            self.interpolator = interpolate.griddata(
                np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])), self.seconds, (self.x, self.y), method='linear')

        else:
            raise Exception('Valor para o interpolador é inválido')
            #
            # a = (self.t[0])
            # print(a)
            # # # #
            # print(a.total_seconds())
            # d = dt.timedelta(seconds=a.total_seconds())
            # print(d)
            #
            # rt = d + dt.datetime.min



            # print(dt.datetime.fromordinal(self.t[0].item().toordinal()))
            # self.t2 = np.array(self.t, dtype='timedelta64[s]')
            # print(self.t2.astype('timedelta64[h]'))

            # print(dt.datetime.strptime(t[0], '%Y-%M-%d') - dt.datetime.min)

            # t2 = dt.datetime(2000,1,1)
            # # #


        #        self.t.
        # print(dt.datetime.fromordinal(dt.datetime.today().toordinal()))
        # delta = dt.timedelta(days=736629, seconds=53.137078, minutes=31, hours=21)
        #
        # print(delta.total_seconds())
        #
        # delta2 = dt.timedelta(seconds=63644823113.13708)
        #
        # print(delta2)

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

        traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis], self.seconds[:, np.newaxis])))
        inter = traj.intersection(geom)

        if (isinstance(inter, MultiLineString) or isinstance(inter, MultiPolygon)):
            array_traj = []

            for multi in inter:
                array_traj.append(self.interpolate_time(multi))

            return array_traj

        return self.interpolate_time(inter)


    def interpolate_middle_xy(self, xy):

        x = (xy[0][0] + xy[0][1]) / 2
        y = (xy[1][0] + xy[1][1]) / 2

        return np.insert(xy, [1], [[x], [y]], axis=1)


    def interpolate_middle_time(self, timestamp):
        t = (timestamp[0] + timestamp[1]) / 2
        return np.insert(timestamp, [1], t)


    def interpolate_time(self, inter):

        xy = inter.coords.xy
        timestamp = np.array(inter.coords)[:, 2]


        if(np.shape(xy)[1] <= 2):
            print(xy)
            xy = self.interpolate_middle_xy(xy)
            print(xy)
            timestamp = self.interpolate_middle_time(timestamp)


        timestamp = timestamp * np.timedelta64(1, 's') + np.datetime64("1970-01-01 00:00:00")

        timestamp[0] = self.interpolator(xy[0][0], xy[1][0]) * np.timedelta64(1, 's') + np.datetime64(
            "1970-01-01 00:00")
        timestamp[-1] = self.interpolator(xy[0][-1], xy[1][-1]) * np.timedelta64(1, 's') + np.datetime64(
            "1970-01-01 00:00")

        #print(xy)
        #print(timestamp)

        return Trajectory(xy[0], xy[1], timestamp)

    def difference(self, geom):
        traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])))
        return traj.difference(geom)
        #
        # def boundary(self):
        #     traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])))
        #     return traj.bounds


# traj = Trajectory([0,2,3,5],
#                   [0,2,2,4],
#                ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00","2000-04-01 00:01:00"])#


# traj = Trajectory([1, 2, 3, 5],
#                   [0, 2, 2, 4],
#                ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00","2000-04-01 00:01:00"],1)
#
# # # # polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
# # # # polygon = Polygon([(1, 1), (1, 3), (2.5, 3), (2.5, 1), (1, 1)])
#
# polygon = Polygon([(1,1), (1, 3), (4, 3), (4, 1), (1,1)])
# #
# print(traj.intersection(polygon))
# #


traj = Trajectory([1, 2, 2, 3, 3, 4, 5, 5, 3, 3],
                  [0, 2, 4, 4, 2, 2, 2, 1, 1, 2],
                  ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00", "2000-04-01 00:01:00"
                      , "2000-05-01 00:01:00", "2000-06-01 00:01:00", "2000-07-01 00:01:00", "2000-08-01 00:01:00"
                      , "2000-09-01 00:01:00", "2000-10-01 00:01:00"], 1)

polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])

print(traj.intersection(polygon))

# x = np.array([4, 6], dtype='f8')
# y = np.array([4, 7], dtype='f8')
# t = np.array([ 9.55843260e+08 ,  9.57139260e+08,  9.57139260e+09], dtype='f8')
#
# xy = np.array((x.T,y.T))
#
# x1 = (xy[0][0] + xy[0][1]) / 2
# y2 = (xy[1][0] + xy[1][1]) / 2
# t3 = (t[0] + t[1]) / 2
#
# print(xy)
#
# xy = np.insert(xy, [1], [[x1],[y2]], axis=1)
# print(xy)
#
#
# #c = ConvexHull( np.column_stack((x[:, np.newaxis], y[:, np.newaxis], t[:, np.newaxis])))
#
# interpolator = interpolate.LinearNDInterpolator(
#                 np.column_stack((x[:, np.newaxis], y[:, np.newaxis])), t )
#
# print(interpolator(5,5))








#
# # vertices = np.column_stack((x[:, np.newaxis], y[:, np.newaxis]))
# #
# # model = PCA(n_components=2).fit(vertices)
# #
# # print(model)
# # proj_vertices = model.transform(vertices)
# # print(model.inverse_transform)
# # print(proj_vertices)
# # hull_kinda = ConvexHull(proj_vertices)
# # print(hull_kinda)
# # print(hull_kinda.simplices)
#
# interpolator = interpolate.LinearNDInterpolator(
#                 np.column_stack((x[:, np.newaxis], y[:, np.newaxis])), t)

#
# timedelta = dt.datetime(year=2000,month=2,day=1,hour=00,minute=1,second=00) - dt.datetime.min
# print(timedelta.total_seconds())
# d = dt.timedelta(seconds=957139260)
#
# rt = d + dt.datetime.min
# print(rt)

# , "2000-04-01 00:01:00"



#print(np.meshgrid(x,y,t))

