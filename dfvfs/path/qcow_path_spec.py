# -*- coding: utf-8 -*-
"""The QCOW image path specification implementation."""

from dfvfs.lib import definitions
from dfvfs.path import factory
from dfvfs.path import path_spec


class QCOWPathSpec(path_spec.PathSpec):
  """Class that implements the QCOW image path specification."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_QCOW

  def __init__(self, parent=None, **kwargs):
    """Initializes the path specification.

    Note that the QCOW path specification must have a parent.

    Args:
      parent (Optional[PathSpec]): parent path specification.

    Raises:
      ValueError: when parent is not set.
    """
    if not parent:
      raise ValueError(u'Missing parent value.')

    super(QCOWPathSpec, self).__init__(parent=parent, **kwargs)

  @property
  def comparable(self):
    """str: comparable representation of the path specification."""
    return self._GetComparable()


factory.Factory.RegisterPathSpec(QCOWPathSpec)
