from checksum import app

import unittest

class ChecksumTestCase(unittest.TestCase):

    def test_create_checksum(self):
        response = self.tester.get('/create-checksum?url=http://www.google.com')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'http://www.google.com&checksum=738ddf35b3a85a7a6ba7b232bd3d5f1e4d284ad1')

    def test_check_checksum(self):
        response = self.tester.get('/check-checksum?url=http://www.google.com&checksum=738ddf35b3a85a7a6ba7b232bd3d5f1e4d284ad1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'verified')

    def test_check_checksum_with_checksum_in_front(self):
        response = self.tester.get('/check-checksum?checksum=738ddf35b3a85a7a6ba7b232bd3d5f1e4d284ad1&url=http://www.google.com')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'verified')

    def test_create_checksum_with_nested_querystring(self):
        response = self.tester.get('/create-checksum?url=http://www.google.com?q=foo&fb=x&g=y')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'http://www.google.com?q=foo&fb=x&g=y&checksum=59f9d86879dfb1020418149d30a7285e0233ba8b')

    def test_check_checksum_with_nested_querystring(self):
        response = self.tester.get('/check-checksum?url=http://www.google.com?q=foo&fb=x&g=y&checksum=59f9d86879dfb1020418149d30a7285e0233ba8b')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'verified')

    def test_create_checksum_with_nested_checksum(self):
        response = self.tester.get('/create-checksum?url=http://www.google.com?q=foo&fb=x&g=y&checksum=59f9d86879dfb1020418149d30a7285e0233ba8b')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'http://www.google.com?q=foo&fb=x&g=y&checksum=59f9d86879dfb1020418149d30a7285e0233ba8b&checksum=1955556fcbdf0687fdc96a2e45119c7c218064b5')

    def test_check_checksum_with_nested_checksum(self):
        response = self.tester.get('/check-checksum?url=http://www.google.com?q=foo&fb=x&g=y&checksum=59f9d86879dfb1020418149d30a7285e0233ba8b&checksum=1955556fcbdf0687fdc96a2e45119c7c218064b5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'verified')

    def test_create_checksum_with_no_url(self):
        response = self.tester.get('/create-checksum')
        self.assertEqual(response.status_code, 400)

    def test_check_checksum_with_bad_checksum(self):
        response = self.tester.get('/check-checksum?url=http://www.google.com&checksum=BAD_CHECKSUM')
        self.assertEqual(response.status_code, 400)

    def test_check_checksum_with_no_checksum(self):
        response = self.tester.get('/check-checksum?url=http://www.google.com')
        self.assertEqual(response.status_code, 400)

    def setUp(self):
        self.tester = app.test_client(self)

if __name__ == '__main__':
    unittest.main()
