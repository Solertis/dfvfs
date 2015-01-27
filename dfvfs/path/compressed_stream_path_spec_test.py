#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the compressed stream path specification implementation."""

import unittest

from dfvfs.path import compressed_stream_path_spec
from dfvfs.path import test_lib


class CompressedStreamPathSpecTest(test_lib.PathSpecTestCase):
  """Tests for the compressed stream path specification implementation."""

  def testInitialize(self):
    """Tests the path specification initialization."""
    path_spec = compressed_stream_path_spec.CompressedStreamPathSpec(
        compression_method=u'test', parent=self._path_spec)

    self.assertNotEquals(path_spec, None)

    with self.assertRaises(ValueError):
      _ = compressed_stream_path_spec.CompressedStreamPathSpec(
          compression_method=u'test', parent=None)

    with self.assertRaises(ValueError):
      _ = compressed_stream_path_spec.CompressedStreamPathSpec(
          compression_method=None, parent=self._path_spec)

    with self.assertRaises(ValueError):
      _ = compressed_stream_path_spec.CompressedStreamPathSpec(
          compression_method=u'test', parent=self._path_spec, bogus=u'BOGUS')

  def testComparable(self):
    """Tests the path specification comparable property."""
    path_spec = compressed_stream_path_spec.CompressedStreamPathSpec(
        compression_method=u'test', parent=self._path_spec)

    self.assertNotEquals(path_spec, None)

    expected_comparable = u'\n'.join([
        u'type: TEST',
        u'type: COMPRESSED_STREAM, compression_method: test',
        u''])

    self.assertEquals(path_spec.comparable, expected_comparable)


if __name__ == '__main__':
  unittest.main()
