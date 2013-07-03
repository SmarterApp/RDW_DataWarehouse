import unittest
import py1


class Test(unittest.TestCase):

    def test_avg_empty(self):
        seq = []
        generated_avg = py1.avg(seq)
        self.assertIsNone(generated_avg)

    def test_avg(self):
        seq = [3, 5, 9]
        generated_avg = py1.avg(seq)
        self.assertEqual(generated_avg, 5.666666666666667)

    def test_std_empty(self):
        seq = []
        generated_stg = py1.std(seq)
        self.assertIsNone(generated_stg)

    def test_std(self):
        seq = [5, 1, 9]
        generated_stg = py1.std(seq)
        self.assertEqual(generated_stg, 3.265986323710904)
