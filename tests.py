import unittest
import os
from makefile_generator import MakefileGenerator

class MakefileGeneratorTest(unittest.TestCase):
    def setUp(self):
        # make fake directory, populate with some files. (needs to be done for .cpp and .c)
        # make sure directory we are trying to create/test with does not exist.


        # setup is run before every test is run 


        print 'setup'

    def tearDown(self):
        # delete directory above.
        print 'teardown'

    def test_parser_creation(self):
        # test_obj = MakefileGenerator()
        self.assertTrue('a', 'a')
        

if __name__ == '__main__':
    unittest.main()