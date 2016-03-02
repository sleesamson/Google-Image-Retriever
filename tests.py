from imageretriever import ImageRetriever
import unittest

class ImageRetrieverTestCase(unittest.TestCase):
    def setUp(self):
        #Key and CSE to use for tests
        self.api_key = 'AIzaSyA2wQlys8wp1D5FYDE1MyFj6wyDBepX3y4'
        self.cse = '016803272596937244315:fouq07cojeg'

        self.ir = ImageRetriever(self.api_key, self.cse)

    def test_cse_notspecified(self):
        with self.assertRaises(ValueError):
            ImageRetriever(self.api_key)

    def test_badfile_type(self):
        with self.assertRaises(TypeError):
            self.ir.query('Blackberry 9800', fileType='txt')

    def test_badsize(self):
        with self.assertRaises(TypeError):
            self.ir.query('Blackberry 9800', size='jsadfa')

    def test_baddominant_color(self):
        with self.assertRaises(TypeError):
            self.ir.query('Blackberry 9800', dom_color='lkajsd')


    def test_result(self):
        self.ir.query('Blackberry 9800', fileType='jpg', dom_color='white')
        results = self.ir.filter_by_resolution(width=300, height=300)

        self.assertEquals(type(results), list)


if __name__ == '__main__':
    unittest.main()


