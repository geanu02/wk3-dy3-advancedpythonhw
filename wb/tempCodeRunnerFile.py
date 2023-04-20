    def test_join_string(self):
        result = pigLatin(["Pig latin is cool"])
        ex_output = "igPay atinlay siay oolcay"
        self.assertEqual(result, ex_output)