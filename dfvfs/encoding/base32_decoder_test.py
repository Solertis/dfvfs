#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the base32 decoder object."""

import unittest

from dfvfs.encoding import base32_decoder
from dfvfs.encoding import test_lib
from dfvfs.lib import errors


class Base32DecoderTestCase(test_lib.DecoderTestCase):
  """Tests for the base32 decoder object."""

  def testDecode(self):
    """Tests the Decode method."""
    decoder = base32_decoder.Base32Decoder()

    decoded_data, _ = decoder.Decode(b'AEBAGBAFAYDQQ===')
    expected_decoded_data = b'\x01\x02\x03\x04\x05\x06\x07\x08'
    self.assertEquals(decoded_data, expected_decoded_data)

    with self.assertRaises(errors.BackEndError):
      _, _ = decoder.Decode(b'\x01\x02\x03\x04\x05\x06\x07\x08')


if __name__ == '__main__':
  unittest.main()