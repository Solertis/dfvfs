# -*- coding: utf-8 -*-
"""The CPIO extracted file-like object implementation."""

import os

from dfvfs.file_io import file_io
from dfvfs.resolver import resolver


class CPIOFile(file_io.FileIO):
  """Class that implements a file-like object using CPIOArchiveFile."""

  def __init__(self, resolver_context):
    """Initializes the file-like object.

    Args:
      resolver_context: the resolver context (instance of resolver.Context).
    """
    super(CPIOFile, self).__init__(resolver_context)
    self._cpio_archive_file = None
    self._cpio_archive_file_entry = None
    self._current_offset = 0
    self._file_system = None
    self._size = 0

  def _Close(self):
    """Closes the file-like object."""
    self._cpio_archive_file_entry = None
    self._cpio_archive_file = None

    self._file_system.Close()
    self._file_system = None

  def _Open(self, path_spec=None, mode='rb'):
    """Opens the file-like object defined by path specification.

    Args:
      path_spec: optional the path specification (instance of PathSpec).
      mode: optional file access mode. The default is 'rb' read-only binary.

    Raises:
      AccessError: if the access to open the file was denied.
      IOError: if the file-like object could not be opened.
      PathSpecError: if the path specification is incorrect.
      ValueError: if the path specification is invalid.
    """
    if not path_spec:
      raise ValueError(u'Missing path specification.')

    file_system = resolver.Resolver.OpenFileSystem(
        path_spec, resolver_context=self._resolver_context)

    file_entry = file_system.GetFileEntryByPathSpec(path_spec)
    if not file_entry:
      file_system.Close()
      raise IOError(u'Unable to retrieve file entry.')

    self._file_system = file_system
    self._cpio_archive_file = self._file_system.GetCPIOArchiveFile()
    self._cpio_archive_file_entry = file_entry.GetCPIOArchiveFileEntry()

    self._current_offset = 0

  # Note: that the following functions do not follow the style guide
  # because they are part of the file-like object interface.

  def read(self, size=None):
    """Reads a byte string from the file-like object at the current offset.

    The function will read a byte string of the specified size or
    all of the remaining data if no size was specified.

    Args:
      size: optional integer value containing the number of bytes to read.
            Default is all remaining data (None).

    Returns:
      A byte string containing the data read.

    Raises:
      IOError: if the read failed.
    """
    if not self._is_open:
      raise IOError(u'Not opened.')

    if self._current_offset >= self._cpio_archive_file_entry.data_size:
      return b''

    file_offset = (
        self._cpio_archive_file_entry.data_offset + self._current_offset)

    read_size = self._cpio_archive_file_entry.data_size - self._current_offset
    if read_size > size:
      read_size = size

    data = self._cpio_archive_file.ReadDataAtOffset(file_offset, read_size)

    # It is possible the that returned data size is not the same as the
    # requested data size. At this layer we don't care and this discrepancy
    # should be dealt with on a higher layer if necessary.
    self._current_offset += len(data)

    return data

  def seek(self, offset, whence=os.SEEK_SET):
    """Seeks an offset within the file-like object.

    Args:
      offset: the offset to seek.
      whence: optional value that indicates whether offset is an absolute
              or relative position within the file. Default is SEEK_SET.

    Raises:
      IOError: if the seek failed.
    """
    if not self._is_open:
      raise IOError(u'Not opened.')

    if whence == os.SEEK_CUR:
      offset += self._current_offset
    elif whence == os.SEEK_END:
      offset += self._cpio_archive_file_entry.data_size
    elif whence != os.SEEK_SET:
      raise IOError(u'Unsupported whence.')

    if offset < 0:
      raise IOError(u'Invalid offset value less than zero.')

    self._current_offset = offset

  def get_offset(self):
    """Returns the current offset into the file-like object.

    Raises:
      IOError: if the file-like object has not been opened.
    """
    if not self._is_open:
      raise IOError(u'Not opened.')

    return self._current_offset

  def get_size(self):
    """Returns the size of the file-like object.

    Raises:
      IOError: if the file-like object has not been opened.
    """
    if not self._is_open:
      raise IOError(u'Not opened.')

    return self._cpio_archive_file_entry.data_size
