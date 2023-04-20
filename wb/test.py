import unittest

from wb import pigLatin

class Test_pigLatin(unittest.TestCase):

    def test_simple_string(self):
        result = pigLatin("Pig latin is cool")
        ex_output = "igPay atinlay siay oolcay"
        self.assertEqual(result, ex_output)

    def test_join_string(self):
        result = pigLatin(["Pig latin is cool"])
        ex_output = "igPay atinlay siay oolcay"
        self.assertEqual(result, ex_output)

if __name__ == '__main__':
    unittest.main()