#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the VMDK image path specification implementation."""

import unittest

from dfvfs.path import test_lib
from dfvfs.path import vmdk_path_spec


class VmdkPathSpecTest(test_lib.PathSpecTestCase):
  """Tests for the VMDK image path specification implementation."""

  def testInitialize(self):
    """Tests the path specification initialization."""
    path_spec = vmdk_path_spec.VmdkPathSpec(parent=self._path_spec)

    self.assertNotEquals(path_spec, None)

    with self.assertRaises(ValueError):
      _ = vmdk_path_spec.VmdkPathSpec(parent=None)

    with self.assertRaises(ValueError):
      _ = vmdk_path_spec.VmdkPathSpec(parent=self._path_spec, bogus=u'BOGUS')

  def testComparable(self):
    """Tests the path specification comparable property."""
    path_spec = vmdk_path_spec.VmdkPathSpec(parent=self._path_spec)

    self.assertNotEquals(path_spec, None)

    expected_comparable = u'\n'.join([
        u'type: TEST',
        u'type: VMDK',
        u''])

    self.assertEquals(path_spec.comparable, expected_comparable)


if __name__ == '__main__':
  unittest.main()
