try:
    from nullege.test.test import *
except ImportError:
    from test import *

from nullege.sample import Sample

class MockUrlRequest(object):
    def __init__(self, url, source, charset):
        self._url = url
        self._source = source
        self._charset = charset

    def info(self):
        return self

    def get_charset(self):
        return self._charset

    def read(self):
        return self._source

    def __call__(self, url):
        assert self._url == url, 'expected {} == {}'.format(self._url, url)
        return self

    @property
    def status(self):
        return 200

class SampleTest(unittest.TestCase):

    Sample = Sample

    @property
    def sample1(self):
        return self.Sample('os', sample1)

    @property
    def sample2(self):
        def get_url(url):
            self.assertEqual(url, sample1['nullege_file'])
            return '#sample_source'
        sample = self.sample1
        sample._get_url = get_url
        return sample

    @property
    def sample3(self):
        sample = self.sample1
        sample._urlopen = MockUrlRequest(sample1['nullege_file'], b'abcd', None)
        return sample

    @property
    def sample4(self):
        sample = self.sample1
        sample._urlopen = MockUrlRequest(sample1['nullege_file'], b'\xe1\x88\xb4', 'utf8')
        return sample

    @property
    def sample5(self):
        sample = self.sample1
        sample._urlopen = MockUrlRequest(sample1['nullege_file'], '\n'.join(map(str, range(1, 100))), None)
        return sample

    def test_file(self):
        self.assertEqual(self.sample1.file, sample1['file'])

    def test_lines(self):
        self.assertEqual(self.sample1.line_numbers, [32, 45])

    def test_nullege_file_url(self):
        self.assertEqual(self.sample1.nullege_file_url, sample1['nullege_file'])

    def test_project(self):
        self.assertEqual(self.sample1.project, 'topographica')

    def test_repository(self):
        self.assertEqual(self.sample1.repository, sample1['repository'])

    def test_source2(self):
        self.assertEqual(self.sample2.source, '#sample_source')

    def test_raw(self):
        self.assertEqual(self.sample1.raw, sample1)

    @unittest.skip('not supported yet')
    def test_source3(self):
        self.assertEqual(self.sample3.source, b'abcd')

    def test_source4(self):
        self.assertEqual(self.sample4.source, b'\xe1\x88\xb4'.decode('utf8'))

    def test_lines_around(self):
        self.assertEqual(self.sample5.lines_around(4, 5), ['2', '3', '4', '5', '6'])

    def test_sample_lines(self):
        self.assertEqual(self.sample5.line_numbers, [32, 45])
        self.assertEqual(self.sample5.sample_lines(), [['30', '31', '32', '33', '34'], ['43', '44', '45', '46', '47']])

    def test_sample_lines_join(self):
        self.assertEqual(self.sample5.sample_lines(14), [list(map(str, range(26, 53)))])

if __name__ == '__main__':
    unittest.main(exit = False)




