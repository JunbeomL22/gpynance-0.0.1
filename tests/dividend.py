from unittest import TestCase
#from gpynance 

class MyTests(TestCase):
    def test_one_plus_two(self):
        self.assertEqual(1 + 2, 3)

"""
tm = [1.0, 2.0, 3.0]
data = Data([0.01, 0.02, 0.03])
div = Dividend(tm, data)
print(div(2.0))
data.data[1] += 0.01
data.notify()
print(div(2.0))
data.data[1] -= 0.01
data.notify()
print(div(2.0))

"""
