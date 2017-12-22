import numpy as np
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Polygon, Point


class Trajectory:
    def __init__(self, x, y, t):

        try:
            if (len(x) != len(y) or len(y) != len(t)):
                raise Exception('Os arrays x, y e t precisam ser do mesmo tamanho')

        except:
            raise Exception('Os atributos x, y e t precisam ser um arrays')

        self.unit = 's'
        self.x = np.array(x, dtype='f8')
        self.y = np.array(y, dtype='f8')
        self.t = np.array(t, dtype='datetime64[{}]'.format(self.unit))
        self.seconds = (self.t - np.datetime64("1970-01-01T00:00:00")) / np.timedelta64(1, 's')

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


    def __to_Timestamp__(self, time):
        return time * np.timedelta64(1, 's') + np.datetime64("1970-01-01 00:00:00")
    pass


    def getTime(self):
        return self.t


    def begins(self):
        return self.t[0]


    def ends(self):
        return self.t[-1]


    def after(self, t):
        t = np.datetime64(t, unit=self.unit)
        mask = self.t > t

        if(np.all(mask == False, axis = 0)):
            return None

        result = Trajectory(self.x[mask], self.y[mask], self.t[mask])
        return result


    def before(self, t):
        t = np.datetime64(t, unit=self.unit)
        mask = self.t < t

        if(np.all(mask == False, axis = 0)):
            return None

        result = Trajectory(self.x[mask], self.y[mask], self.t[mask])
        return result


    def during(self, t1, t2):

        t1 = np.datetime64(t1, unit=self.unit)
        t2 = np.datetime64(t2, unit=self.unit)

        mask = ((self.t > t1) & (self.t < t2))

        if(np.all(mask == False, axis = 0)):
            return None

        result = Trajectory(self.x[mask], self.y[mask], self.t[mask])
        return result

    def intersection_shapely(self,geom):
        traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis], self.seconds[:, np.newaxis])))
        return traj.intersection(geom)

    def boundary_shapely(self):
        traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis], self.seconds[:, np.newaxis])))
        return traj.boundary

    def to_Trajectory(self, inter):

        if (inter.has_z == False):
            raise Exception('O objeto precisa ser uma geometria com um atributo z')

        if isinstance(inter, MultiLineString) or isinstance(inter, MultiPolygon):
            array_traj = []
            for multi in inter:

                array_traj.append(self.__set_data__(multi))

            return array_traj

        return self.__set_data__(inter)


    def __calculate_inter__(self, cont, point, poly, field):

        xy = np.array([self.x[cont - 1], self.y[cont - 1]])

        timeBefore = self.seconds[cont - 1]
        timeCurrent = self.seconds[cont]

        pointBefore = Point(xy)

        line = LineString([pointBefore, point])
        result = line.intersection(poly)

        intersection = np.array(result)


        if (intersection.size == 2):
            inter = intersection
        else:
            inter = intersection[field]

        time = self.__interpolate_linear__(timeBefore, timeCurrent, np.array(pointBefore),
                                           inter, np.array(point))
        return np.insert(inter, 2, time)
        pass


    def intersecs(self, poly):

        beforeIntersection = None
        cont = 0

        trajectory = np.empty(shape=(0))

        for x, y in np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis])):

            point = Point(x, y)
            haveIntersection = poly.intersects(point)

            if (haveIntersection):

                if (haveIntersection !=  beforeIntersection):

                    result = self.__calculate_inter__(cont, point, poly, 0)
                    trajectory = np.append(trajectory, result)
                pass

                p = np.array(point)
                trajectory = np.append(trajectory, np.insert(p, 2, self.seconds[cont]))
                beforeIntersection = haveIntersection

            elif (haveIntersection !=  beforeIntersection and cont > 0):

                result = self.__calculate_inter__(cont, point, poly, 1)
                trajectory = np.append(trajectory, result)
                beforeIntersection = haveIntersection
            pass

            cont = cont + 1
            pass

        size = int(trajectory.size / 3)
        trajectory = trajectory.reshape(size, 3)

        return Trajectory(trajectory[:,0],trajectory[:,1],trajectory[:,2])


    def __get_h__(self, xy1, xy2):

        x = (xy2[0] - xy1[0])
        y = (xy2[1] - xy1[1])

        x = x * x
        y = y * y

        return np.sqrt((x+y))


    def __interpolate_linear__(self,t1, t2, first_xy, second_xy, third_xy):

        h1 = self.__get_h__(first_xy,third_xy)
        h2 = self.__get_h__(first_xy, second_xy)

        t = t2 - t1

        time = ((t * h2) / h1) + t1

        return time

        pass

    def __set_data__(self, inter):

        xy = np.array(inter)
        timestamp = self.__to_Timestamp__(xy[:, 2])

        return Trajectory(xy[:,0], xy[:,1], timestamp)


    def difference(self, geom):
        traj = LineString(np.column_stack((self.x[:, np.newaxis], self.y[:, np.newaxis], self.seconds[:, np.newaxis])))
        return traj.difference(geom)



# traj = Trajectory([1,2,3,5],
#                   [0,2,2,4],
#                ["2000-01-01 00:01:00", "2000-02-01 00:01:00",
#                 "2000-03-01 00:01:00","2000-04-01 00:01:00"])
#
# traj2 = Trajectory([0,2,0],
#                   [0,2,2],
#                ["2000-01-01 00:01:00", "2000-02-01 00:01:00",
#                 "2000-03-01 00:01:00"])

# traj3 = Trajectory([1, 2, 2, 3, 3, 4, 5, 5, 3, 3],
#                    [0, 2, 4, 4, 2, 2, 2, 1, 1, 2],
#            ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00", "2000-04-01 00:01:00"
#                , "2000-05-01 00:01:00", "2000-06-01 00:01:00", "2000-07-01 00:01:00",
#             "2000-08-01 00:01:00"
#                , "2000-09-01 00:01:00", "2000-10-01 00:01:00"])


# polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])


