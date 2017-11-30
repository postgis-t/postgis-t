import unittest
from unittest.mock import MagicMock
from shapely.geometry import Polygon, LineString
import numpy as np

from postgistT.trajectory.trajectory import Trajectory


class TestTrajectory(unittest.TestCase):

    def setUp(self):
        self.traj = Trajectory([1, 2, 3, 5], [0, 2, 2, 4],
                               ["2000-01-01 00:01:00", "2000-02-01 00:01:00",
                                "2000-03-01 00:01:00", "2000-04-01 00:01:00"])

        self.traj2 = Trajectory([0, 2, 0],
                                [0, 2, 4],
                                ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00"])

    pass

    ##
    ## Inicio dos testes
    ##

    def test_intersection_beirada(self):
        polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
        line = LineString([(1, 0, 1), (2, 2, 2), (3, 2, 3), (5, 4, 4)])

        inter = line.intersection(polygon)
        resultRight = LineString([(1.5, 1, 1.5), (2, 2, 2), (3, 2, 3), (4, 3, 3.5)])

        assert (resultRight == inter)

    pass

    def test_intersection_sem_beirada(self):
        polygon = Polygon([(1.1, 1), (1, 3), (4.1, 3), (4.1, 1), (1.1, 1)])
        line = LineString([(1, 0, 1), (2, 2, 2), (3, 2, 3), (5, 4, 4)])

        result = LineString([(1.5, 1, 1.5), (2, 2, 2), (3, 2, 3), (4, 3, 3.5)])

        inter = line.intersection(polygon)

        assert (result == inter)

    pass

    def test_intersection_com_beirada_superior_e_inferior_esquerdo(self):
        polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
        line = LineString([(0, 0, 1), (2, 2, 2), (0, 4, 3)])

        result = LineString([(1, 1, 1.5), (2, 2, 2), (1, 3, 2.5)])
        inter = line.intersection(polygon)

        assert (result == inter)

    pass

    def test_intersection_sem_beirada_superior_e_inferior_esquerdo(self):
        polygon = Polygon([(0.9, 1), (0.9, 2), (0.9, 3), (4, 3), (4, 1), (0.9, 1)])
        line = LineString([(0, 0, 1), (2, 2, 2), (0, 4, 3)])

        result = LineString([(1, 1, 1.5), (2, 2, 2), (1, 3, 2.5)])
        inter = line.intersection(polygon)

        assert (result == inter)

    pass

    def test_intersection_quando_se_encontra_em_um_ponto_qualquer(self):
        polygon = Polygon([(1, 1), (1, 2), (1, 3), (4, 3), (4, 1), (1, 1)])
        line = LineString([(0, 0, 1), (2, 2, 2), (0, 2, 3)])

        result = LineString([(1, 1, 1.5), (2, 2, 2), (1, 2, 2.5)])
        inter = line.intersection(polygon)

        assert (result == inter)
    pass


    ###Só para fins de verificação, esse teste deve da erro
    def test_intersection_verificar_se_interpolou_e_nao_pegou_o_mais_proximo(self):
        polygon = Polygon([(1, 1), (1, 2), (1, 3), (4, 3), (4, 1), (1, 1)])
        line = LineString([(0, 0, 1), (2, 2, 2), (0, 2, 3)])

        result = LineString([(1, 1, 1.5), (2, 2, 2), (1, 2, 2.5)])
        inter = line.intersection(polygon)

        time = np.array(inter)[:,2]

        assert (time[0] != time[1])
        assert (time[1] != time[2])

    pass


    def test_intersection_com_mock(self):
        ls = LineString([(1.5, 1, 9.48024060e+08), (2, 2, 9.49363260e+08),
                         (3, 2, 9.51868860e+08), (4, 3, 9.53208060e+08)])

        poly = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])

        self.traj.intersection_shapely = MagicMock(return_value=ls)
        response = self.traj.intersection_shapely(poly)

        ls = np.array(ls)
        trajMock = self.traj.to_Trajectory(response)
        traj = Trajectory(ls[:, 0], ls[:, 1], ls[:, 2])

        assert (np.array_equal(trajMock.getX(), traj.getX()))
        assert (np.array_equal(trajMock.getY(), traj.getY()))
        assert (np.array_equal(trajMock.getTime(), traj.getTime()))

    pass

    def test_intersection_com_mock_2(self):
        ls = LineString([(1, 1, 9.48024060e+08), (2, 2, 9.49363260e+08),
                         (3, 1, 9.51868860e+08)])

        poly = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])

        self.traj2.intersection_shapely = MagicMock(return_value=ls)
        response = self.traj2.intersection_shapely(poly)

        ls = np.array(ls)

        trajMock = self.traj2.to_Trajectory(response)
        traj = Trajectory(ls[:, 0], ls[:, 1], ls[:, 2])

        assert (np.array_equal(trajMock.getX(), traj.getX()))
        assert (np.array_equal(trajMock.getY(), traj.getY()))
        assert (np.array_equal(trajMock.getTime(), traj.getTime()))

    pass

    ###Só para fins de verificação
    def test_intersection_sem_mock_do_test_2(self):
        poly = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
        response = self.traj2.intersection_shapely(poly)

        traj = self.traj2.to_Trajectory(response)

        time = np.datetime64('2000-02-01T00:01:00')
        seconds = (time - np.datetime64("1970-01-01 00:00:00")) / np.timedelta64(1, 's')

        assert (np.array_equal(traj.getTime()[0], seconds))
        assert (np.array_equal(traj.getTime()[1], seconds))
        assert (np.array_equal(traj.getTime()[2], seconds))

    pass

    ##
    ## Fim dos testes
    ##


    # ##
    # ## Inicio dos testes
    # ##
    #
    # ##Irá da erro pois a intersection irá enconstar na beirada
    # ##ou seja o ultimo Z retornado será diferente de 3.5
    # def test_intersection_beirada(self):
    #     polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
    #     line = LineString([(1, 0, 1), (2, 2, 2), (3, 2, 3), (5, 4, 4)])
    #
    #     result = LineString([(1.5, 1, 1.5), (2, 2, 2), (3, 2, 3), (4, 3, 3.5)])
    #     linestring = LineString([(1.5, 1, 1.5), (2, 2, 2), (3, 2, 3), (4, 3, 3)])
    #
    #     inter = line.intersection(polygon)
    #
    #     assert (result != inter)
    #     assert(linestring == inter)
    #
    #     pass
    #
    # def test_intersection_sem_beirada(self):
    #
    #     polygon = Polygon([(1.1, 1), (1, 3), (4.1, 3), (4.1, 1), (1.1, 1)])
    #     line = LineString([(1, 0, 1), (2, 2, 2), (3, 2, 3), (5, 4, 4)])
    #
    #     result = LineString([(1.5, 1, 1.5), (2, 2, 2), (3, 2, 3), (4, 3, 3.5)])
    #
    #     inter = line.intersection(polygon)
    #
    #     assert (result == inter)
    #
    #     pass
    #
    # def test_intersection_com_beirada_superior_esquerdo(self):
    #
    #     polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
    #     line = LineString([(0, 0, 1), (2, 2, 2), (0, 4, 3)])
    #
    #     result = LineString([(1, 1, 2), (2, 2, 2), (1, 3, 2)])
    #     inter = line.intersection(polygon)
    #
    #     assert (result == inter)
    #
    #     pass
    #
    # def test_intersection_com_ponto(self):
    #
    #     polygon = Polygon([(1, 1),(1,2), (1, 3), (4, 3), (4, 1), (1, 1)])
    #     line = LineString([(0, 0, 1), (2, 2, 2), (0, 2, 3)])
    #
    #     result = LineString([(1, 1, 2), (2, 2, 2), (1, 2, 2)])
    #     inter = line.intersection(polygon)
    #
    #     assert (result == inter)
    #
    #     pass
    #
    # def test_intersection_com_ponto_flutuante(self):
    #     polygon = Polygon([(1, 1), (1.1, 2.1), (1, 3), (4, 3), (4, 1), (1, 1)])
    #     line = LineString([(0, 0, 1), (2.1, 2.1, 2), (0.1, 2.1, 3)])
    #
    #     result = LineString([(1, 1, 2), (2.1, 2.1, 2), (1.1, 2.1, 2)])
    #     inter = line.intersection(polygon)
    #
    #     assert (result == inter)
    #
    #     pass
    # #
    # def test_startTime(self):
    #     dateTest = dt.datetime(year=2000, month=1, day=1)
    #     dateTestNumPy = np.array(dateTest, dtype='datetime64[{}]'.format('D'))
    #     dateFalse = dt.datetime(year=2000, month=1, day=2, hour=1)
    #
    #     self.assertTrue(np.array_equal(self.trajetoria.begins(), dateTestNumPy))
    #     self.assertNotIsInstance(self.trajetoria.begins(), dt.datetime)
    #     self.assertNotEqual(self.trajetoria.begins(), dateFalse)
    #     self.assertEqual(self.trajetoria.begins(), dateTestNumPy)
    #
    # pass
    #
    # def test_endTime(self):
    #     dateTest = dt.datetime(year=2000, month=5, day=1)
    #     dateTestNumPy = np.array(dateTest, dtype='datetime64[{}]'.format('D'))
    #     dateFalse = dt.datetime(year=2000, month=3, day=2, hour=1)
    #
    #     self.assertTrue(self.trajetoria.ends(), dateTest)
    #     self.assertNotIsInstance(self.trajetoria.ends(), dt.datetime)
    #     self.assertNotEqual(self.trajetoria.ends(), dateFalse)
    #     self.assertEqual(self.trajetoria.ends(), dateTestNumPy)
    #
    # pass
    #
    # def test_getX(self):
    #     x = [1, 2, 3, 5, 5]
    #     falseX = [4, 2, 1, 6]
    #
    #     self.assertTrue(np.array_equal(self.trajetoria.getX(), x))
    #     self.assertFalse(np.array_equal(self.trajetoria.getX(), falseX), False)
    #     self.assertFalse(np.array_equal(self.trajetoria.getX(), falseX.append(1)), False)
    #     self.assertTrue(self.trajetoria.getX().__len__() == 5)
    #
    # pass
    #
    # def test_getY(self):
    #     y = [0, 2, 2, 4, 5]
    #     falseY = [5, 3, 0, 7]
    #
    #     self.assertTrue(np.array_equal(self.trajetoria.getY(), y))
    #     self.assertFalse(np.array_equal(self.trajetoria.getY(), falseY), False)
    #     self.assertFalse(np.array_equal(self.trajetoria.getY(), falseY.append(1)), False)
    #     self.assertTrue(self.trajetoria.getY().__len__() == 5)
    #
    # pass
    #
    # # erro
    # def test_after(self):
    #     traj = Trajectory([5, 5],
    #                       [4, 5],
    #                       ['2000-04-01', '2000-05-01', '2000-05-01', '2000-05-01'])
    #
    #     dateMidTest = dt.datetime(year=2000, month=3, day=1)
    #
    #     trajTest = self.trajetoria.after(dateMidTest)
    #
    #     self.assertTrue(np.array_equal(traj.getX(), trajTest.getX()))
    #     self.assertFalse(np.array_equal(traj.getX(), trajTest.getX().T) == False)
    #     self.assertTrue(np.array_equal(traj.getY(), trajTest.getY()))
    #     self.assertTrue(np.array_equal(traj.begins(), trajTest.begins()))
    #     self.assertTrue(np.array_equal(traj.ends(), trajTest.ends()))
    #
    # pass
    #
    # # erro
    # def test_create_obj_two_points(self):
    #     traj = Trajectory([1, 2],
    #                       [0, 2],
    #                       ['2000-01-01', '2000-02-01'])
    #
    #     pass
    #
    # def test_create_obj_three_points(self):
    #     traj = Trajectory([1, 2, 3],
    #                       [0, 2, 3],
    #                       ['2000-01-01', '2000-02-01', '2000-03-01'])
    #     pass
    #
    # # erro
    # def test_create_obj_three_points(self):
    #     traj = Trajectory([1, 2, 2, 3, 3, 4, 5, 5, 3, 3],
    #                       [0, 2, 4, 4, 2, 2, 2, 1, 1, 2],
    #                       ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00", "2000-04-01 00:01:00"
    #                           , "2000-05-01 00:01:00", "2000-06-01 00:01:00", "2000-07-01 00:01:00",
    #                        "2000-08-01 00:01:00"
    #                           , "2000-09-01 00:01:00", "2000-10-01 00:01:00"])
    #     pass
    #
    # # erro
    # def test_intersection_multiline(self):
    #     traj = Trajectory([1, 2, 2, 3, 3, 4, 5, 5, 3, 3],
    #                       [0, 2, 4, 4, 2, 2, 2, 1, 1, 2],
    #                       ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00", "2000-04-01 00:01:00"
    #                           , "2000-05-01 00:01:00", "2000-06-01 00:01:00", "2000-07-01 00:01:00",
    #                        "2000-08-01 00:01:00"
    #                           , "2000-09-01 00:01:00", "2000-10-01 00:01:00"])
    #
    #     polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
    #     traj.intersection(polygon)
    #     pass
    #
    # def test_intersection_normal_line(self):
    #     traj = Trajectory([1, 2, 3, 5],
    #                       [0, 2, 2, 4],
    #                       ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00", "2000-04-01 00:01:00"])
    #
    #     polygon = Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
    #     traj.intersection(polygon)
    #     pass
    #
    # def test_before(self):
    #     traj = Trajectory([1, 2, 3],
    #                       [0, 2, 2],
    #                       ['2000-01-01', '2000-02-01', '2000-03-01'])
    #     dateMidTest = dt.datetime(year=2000, month=4, day=1)
    #
    #     trajTest = self.trajetoria.before(dateMidTest)
    #
    #     self.assertTrue(np.array_equal(traj.getX(), trajTest.getX()))
    #     self.assertFalse(np.array_equal(traj.getX(), trajTest.getX().T) == False)
    #     self.assertTrue(np.array_equal(traj.getY(), trajTest.getY()))
    #     self.assertTrue(np.array_equal(traj.begins(), trajTest.begins()))
    #     self.assertTrue(np.array_equal(traj.ends(), trajTest.ends()))
    #
    # pass
    #
    # def test_during(self):
    #     traj = Trajectory([2, 3, 5],
    #                       [2, 2, 4],
    #                       ['2000-02-01', '2000-03-01', '2000-04-01'])
    #
    #     startDateTest = dt.datetime(year=2000, month=1, day=1)
    #     endDateTest = dt.datetime(year=2000, month=5, day=1)
    #
    #     trajTest = self.trajetoria.during(startDateTest, endDateTest)
    #
    #     self.assertTrue(np.array_equal(traj.getX(), trajTest.getX()))
    #     self.assertFalse(np.array_equal(traj.getX(), trajTest.getX().T) == False)
    #     self.assertTrue(np.array_equal(traj.getY(), trajTest.getY()))
    #     self.assertTrue(np.array_equal(traj.begins(), trajTest.begins()))
    #     self.assertTrue(np.array_equal(traj.ends(), trajTest.ends()))
    #
    # pass


##
## Fim dos testes
##

if __name__ == '__main__':
    unittest.main()

