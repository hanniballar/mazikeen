import unittest

from mazikeen.ScriptDataProcessor import Version

class VersionTest(unittest.TestCase):
    def test_simple(self):
        v = Version("1.0.0")
        self.assertTupleEqual((1,0,0), (v.major, v.minor, v.patch))

    def test_smallVersion(self):
        v = Version("1")
        self.assertEqual((1,"",""), (v.major, v.minor, v.patch))

    def test_LongVersion(self):
        with self.assertRaises(Exception, msg = "Invalid version. Version is too long") as e:
            Version("1.0.0.0")
        
    def test_StrInVersion(self):
        with self.assertRaises(ValueError, msg = "Invalid version. Version may only contain numbers") as e:
            Version("1.a.0")

    def test_NoneNEmpty(self):
        v = Version("")
        self.assertTupleEqual(("","",""), (v.major, v.minor, v.patch))
        v = Version(None)
        self.assertTupleEqual(("","",""), (v.major, v.minor, v.patch))

    def test_Compare(self):
        self.assertGreater(Version("1.0.1"), Version("1.0.0"))
        self.assertGreater(Version("1.1.0"), Version("1.0.0"))
        self.assertGreater(Version("2.0.0"), Version("1.0.0"))
        self.assertTrue(Version("1.0.0") == Version("1.0.0"))
        self.assertLess(Version("1.0.0"), Version("1.0.1"))
        self.assertLess(Version("1.0.0"), Version("1.1.0"))
        self.assertLess(Version("1.0.0"), Version("2.0.0"))

if __name__ == '__main__':
    unittest.main()