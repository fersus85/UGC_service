import unittest


class TestFake(unittest.TestCase):
    def test_fake(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
