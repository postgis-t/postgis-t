import unittest
from postgistT.trajectory.trajectory import Trajectory
import datetime as dt
import numpy as np


class TestTrajectory(unittest.TestCase):

    def setUp(self):
        self.trajetoria = Trajectory([1, 2, 3, 5, 5],
                          [0, 2, 2, 4, 5],
                          ['2000-01-01', '2000-02-01', '2000-03-01', '2000-04-01', '2000-05-01'])

    pass

##
## Inicio dos testes
##
    
    def test_startTime(self):

        dateTest = dt.datetime(year=2000,month=1,day=1)
        dateTestNumPy = np.array(dateTest, dtype='datetime64[{}]'.format('D'))
        dateFalse = dt.datetime(year=2000, month=1, day=2, hour=1)

        self.assertTrue(np.array_equal(self.trajetoria.begins(), dateTestNumPy))
        self.assertNotIsInstance(self.trajetoria.begins(),dt.datetime)
        self.assertNotEqual(self.trajetoria.begins(),dateFalse)
        self.assertEqual(self.trajetoria.begins(),dateTestNumPy)

    pass


    def test_endTime(self):

        dateTest = dt.datetime(year=2000,month=5,day=1)
        dateTestNumPy = np.array(dateTest, dtype='datetime64[{}]'.format('D'))
        dateFalse = dt.datetime(year=2000, month=3, day=2, hour=1)

        self.assertTrue(self.trajetoria.ends(),dateTest)
        self.assertNotIsInstance(self.trajetoria.ends(),dt.datetime)
        self.assertNotEqual(self.trajetoria.ends(),dateFalse)
        self.assertEqual(self.trajetoria.ends(),dateTestNumPy)

    pass


    def test_getX(self):

        x = [1, 2, 3, 5, 5]
        falseX = [4, 2, 1, 6]

        self.assertTrue(np.array_equal(self.trajetoria.getX(), x))
        self.assertFalse(np.array_equal(self.trajetoria.getX(), falseX), False)
        self.assertFalse(np.array_equal(self.trajetoria.getX(), falseX.append(1)), False)
        self.assertTrue(self.trajetoria.getX().__len__() == 5)

    pass


    def test_getY(self):

        y = [0, 2, 2, 4, 5]
        falseY = [5, 3, 0, 7]

        self.assertTrue(np.array_equal(self.trajetoria.getY(), y))
        self.assertFalse(np.array_equal(self.trajetoria.getY(), falseY), False)
        self.assertFalse(np.array_equal(self.trajetoria.getY(), falseY.append(1)), False)
        self.assertTrue(self.trajetoria.getY().__len__() == 5)


    pass


    def test_after(self):

        traj = Trajectory([5, 5],
                          [4, 5],
                          ['2000-04-01', '2000-05-01'])

        dateMidTest = dt.datetime(year=2000, month=3, day=1)

        trajTest = self.trajetoria.after(dateMidTest)

        self.assertTrue(np.array_equal(traj.getX(), trajTest.getX()))
        self.assertFalse(np.array_equal(traj.getX(),  trajTest.getX().T) == False)
        self.assertTrue(np.array_equal(traj.getY(), trajTest.getY()))
        self.assertTrue(np.array_equal(traj.begins(), trajTest.begins()))
        self.assertTrue(np.array_equal(traj.ends(), trajTest.ends()))

    pass


    def test_before(self):

        traj = Trajectory([1,2,3],
                          [0,2,2],
                          ['2000-01-01', '2000-02-01', '2000-03-01'])
        dateMidTest = dt.datetime(year=2000, month=4, day=1)

        trajTest = self.trajetoria.before(dateMidTest)

        self.assertTrue(np.array_equal(traj.getX(), trajTest.getX()))
        self.assertFalse(np.array_equal(traj.getX(), trajTest.getX().T) == False)
        self.assertTrue(np.array_equal(traj.getY(), trajTest.getY()))
        self.assertTrue(np.array_equal(traj.begins(), trajTest.begins()))
        self.assertTrue(np.array_equal(traj.ends(), trajTest.ends()))

    pass


    def test_during(self):

        traj = Trajectory([2, 3, 5],
                          [2, 2, 4],
                          ['2000-02-01', '2000-03-01', '2000-04-01'])

        startDateTest = dt.datetime(year=2000, month=1, day=1)
        endDateTest = dt.datetime(year=2000, month=5, day=1)

        trajTest = self.trajetoria.during(startDateTest,endDateTest)

        self.assertTrue(np.array_equal(traj.getX(), trajTest.getX()))
        self.assertFalse(np.array_equal(traj.getX(), trajTest.getX().T) == False)
        self.assertTrue(np.array_equal(traj.getY(), trajTest.getY()))
        self.assertTrue(np.array_equal(traj.begins(), trajTest.begins()))
        self.assertTrue(np.array_equal(traj.ends(), trajTest.ends()))

    pass

##
## Fim dos testes
##

if __name__ == '__main__':
    unittest.main()
