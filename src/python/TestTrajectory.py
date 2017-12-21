import unittest
from unittest.mock import MagicMock
from shapely.geometry import Polygon, LineString
import numpy as np
import datetime as dt

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

    def test_axioms_before(self):

        time = "2000-01-01 00:01:00"
        assert (self.traj.before(self.traj.begins()) == None)
        assert(self.traj.after(time).before(time) == None)
    pass


    def test_axioms_after(self):

        time = "2000-04-01 00:01:00"
        assert (self.traj.after(self.traj.ends()) == None)
        assert(self.traj.before(time).after(time) == None)
    pass


    def test_axioms_during(self):

        assert(self.traj.after("2000-01-01 00:01:00").during("2000-04-01 00:01:00", "2000-01-01 00:01:00") == None)
        assert (self.traj.before("2000-04-01 00:01:00").during( "2000-04-01 00:01:00","2000-01-01 00:01:00") == None)
    pass


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



    def test_intersection_verificar_se_interpolou_e_nao_pegou_o_mais_proximo(self):

        polygon = Polygon([(1, 1), (1, 2), (1, 3), (4, 3), (4, 1), (1, 1)])
        line = LineString([(0, 0, 1), (2, 2, 2), (0, 2, 3)])

        inter = line.intersection(polygon)
        time = np.array(inter)[:,2]

        assert (time[0] != time[1])
        assert (time[1] != time[2])

    pass

    def test_intersection_verificar_se_interpolacao_retorna_o_valor_correto(self):

        line = LineString([(0, 0, 1), (2, 2, 2), (0, 2, 3)])
        polygon = Polygon([(1, 1), (1, 2), (1, 3), (4, 3), (4, 1), (1, 1)])

        result = LineString([(1, 1, 1.5), (2, 2, 2), (1, 2, 2.5)])
        inter = line.intersection(polygon)

        resultTime = np.array(result)[:, 2]
        time = np.array(inter)[:, 2]

        assert (time[0] == resultTime[0])
        assert (time[1] == resultTime[1])
        assert (time[2] == resultTime[2])
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



    def test_startTime(self):
        dateTest = dt.datetime(year=2000, month=1, day=1, minute=1)
        dateTestNumPy = np.array(dateTest, dtype='datetime64[{}]'.format('s'))
        dateFalse = dt.datetime(year=2000, month=1, day=2, hour=1)

        self.assertTrue(np.array_equal(self.traj.begins(), dateTestNumPy))
        self.assertNotIsInstance(self.traj.begins(), dt.datetime)
        self.assertNotEqual(self.traj.begins(), dateFalse)
        self.assertEqual(self.traj.begins(), dateTestNumPy)

    pass



    def test_endTime(self):
        dateTest = dt.datetime(year=2000, month=4, day=1, minute=1)
        dateTestNumPy = np.array(dateTest, dtype='datetime64[{}]'.format('s'))
        dateFalse = dt.datetime(year=2000, month=3, day=2, hour=1)

        self.assertTrue(self.traj.ends(), dateTest)
        self.assertNotIsInstance(self.traj.ends(), dt.datetime)
        self.assertNotEqual(self.traj.ends(), dateFalse)
        self.assertEqual(self.traj.ends(), dateTestNumPy)

    pass



    def test_getX(self):

        x = [1, 2, 3, 5]
        falseX = [4, 7, 1, 6]

        self.assertTrue(np.array_equal(self.traj.getX(), x))
        self.assertFalse(np.array_equal(self.traj.getX(), falseX), False)
        falseX.append(1)
        self.assertFalse(np.array_equal(self.traj.getX(),falseX), False)
        self.assertTrue(self.traj.getX().__len__() == 4)

    pass



    def test_getY(self):
        y = [0, 2, 2, 4]
        falseY = [5, 3, 0, 7]

        self.assertTrue(np.array_equal(self.traj.getY(), y))
        self.assertFalse(np.array_equal(self.traj.getY(), falseY), False)
        falseY.append(1)
        self.assertFalse(np.array_equal(self.traj.getY(), falseY), False)
        self.assertTrue(self.traj.getY().__len__() == 4)

    pass



    def test_tamanho_de_x_e_y_sao_diferentes_de_t(self):
        try:
            Trajectory([5, 5],[4, 5],['2000-04-01', '2000-05-01',
                    '2000-05-01', '2000-05-01'])
            assert(False)
        except:
            assert(True)
    pass



    def test_tamanho_de_y_e_diferente_de_t_e_x(self):
        try:
            Trajectory([5, 5, 4, 5], [4, 5], ['2000-04-01', '2000-05-01',
                                        '2000-05-01', '2000-05-01'])
            assert (False)
        except:
            assert (True)
    pass



    def test_tamanho_dos_tres_atributos_sao_diferentes(self):
        try:
            Trajectory([5, 5, 4, 5], [4, 5], ['2000-05-01',
                                        '2000-05-01', '2000-05-01'])
            assert (False)
        except:
            assert (True)
    pass



    def test_criar_objeto_de_dois_pontos(self):
        try:
            Trajectory([1, 2],[0, 2],
                    ['2000-01-01', '2000-02-01'])

            assert(True)
        except:
            assert(False)
        pass



    def test_criar_obj_de_tres_pontos(self):
        try:
            Trajectory([1, 2, 3],[0, 2, 3],
                    ['2000-01-01', '2000-02-01', '2000-03-01'])

            assert(True)
        except:
            assert(False)
        pass



    def test_criar_obj_de_dez_pontos(self):

        try:
            Trajectory([1, 2, 2, 3, 3, 4, 5, 5, 3, 3],
                       [0, 2, 4, 4, 2, 2, 2, 1, 1, 2],
                       ["2000-01-01 00:01:00", "2000-02-01 00:01:00", "2000-03-01 00:01:00", "2000-04-01 00:01:00"
                           , "2000-05-01 00:01:00", "2000-06-01 00:01:00", "2000-07-01 00:01:00",
                        "2000-08-01 00:01:00"
                           , "2000-09-01 00:01:00", "2000-10-01 00:01:00"])
            assert (True)
        except:
            assert (False)
        pass



##
## Fim dos testes
##

if __name__ == '__main__':
    unittest.main()

