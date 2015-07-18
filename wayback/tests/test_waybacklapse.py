import os
import unittest

import wayback.waybacklapse as wbl


class TestWaybacklapse(unittest.TestCase):

    def test_create_output_fn(self):
        """
        Non-Alphanumeric characters are stripped while creating output filename
        """

        expected = os.path.join(wbl.GIF_OUTPUT_DIR, 'foo.gif')
        actual = wbl.create_output_fn('foo!@#$%^&()[]')
        self.assertEqual(expected, actual)
