#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the gzip file path specification implementation."""

import unittest

from dfvfs.path import gzip_path_spec

from tests.path import test_lib


class GzipPathSpecTest(test_lib.PathSpecTestCase):
  """Tests for the gzip file path specification implementation."""

  def testInitialize(self):
    """Tests the path specification initialization."""
    path_spec = gzip_path_spec.GzipPathSpec(parent=self._path_spec)

    self.assertIsNotNone(path_spec)

    with self.assertRaises(ValueError):
      _ = gzip_path_spec.GzipPathSpec(parent=None)

    with self.assertRaises(ValueError):
      _ = gzip_path_spec.GzipPathSpec(parent=self._path_spec, bogus=u'BOGUS')

  def testComparable(self):
    """Tests the path specification comparable property."""
    path_spec = gzip_path_spec.GzipPathSpec(parent=self._path_spec)

    self.assertIsNotNone(path_spec)

    expected_comparable = u'\n'.join([
        u'type: TEST',
        u'type: GZIP',
        u''])

    self.assertEqual(path_spec.comparable, expected_comparable)


if __name__ == '__main__':
  unittest.main()
