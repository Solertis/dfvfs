# -*- coding: utf-8 -*-
"""A text file interface for file-like objects."""

import os

# Since this class implements the readlines file-like object interface
# the names of the interface functions are in lower case as an exception
# to the normal naming convention.

# TODO: add encoding and codepage support.


class TextFile(object):
  """Class that implements a text file interface for file-like objects."""

  # The size of the lines buffer.
  _LINES_BUFFER_SIZE = 1024 * 1024

  # The maximum allowed size of the read buffer.
  _MAXIMUM_READ_BUFFER_SIZE = 16 * 1024 * 1024

  def __init__(self, file_object, end_of_line=b'\n'):
    """Initializes the text file.

    Args:
      file_object: the file-like object (instance of file_io.FileIO) to read
                   from.
      end_of_line: optional string containing the end of line indicator.
    """
    super(TextFile, self).__init__()
    self._file_object = file_object
    self._file_object_size = file_object.get_size()
    self._end_of_line = end_of_line
    self._lines_buffer = b''
    self._lines_buffer_offset = 0
    self._lines_buffer_size = 0
    self._current_offset = 0

  def __enter__(self):
    """Enters a with statement."""
    return self

  def __exit__(self, unused_type, unused_value, unused_traceback):
    """Exits a with statement."""
    # TODO: do we want to close the file_object here e.g. i.c.w. a flag value
    # to have TextFile manage the file_object?
    return

  def __iter__(self):
    """Returns a line of text.

    Yields:
      A byte string containing a line of text.
    """
    line = self.readline()
    while line:
      yield line
      line = self.readline()

  def _ReadLinesData(self, maximum_size=None):
    """Reads the lines data.

    The number of reads are minimized by using a lines buffer.

    Args:
      maximum_size: optional integer value that contains the maximum number of
                    bytes to read from the file-like object. The default is None
                    indicating all remaining data.

    Raises:
      ValueError: if the maximum size is smaller than zero or exceeds the
                  maximum (as defined by _MAXIMUM_READ_BUFFER_SIZE).
    """
    if maximum_size is not None and maximum_size < 0:
      raise ValueError(u'Invalid maximum size value smaller than zero.')

    if (maximum_size is not None and
        maximum_size > self._MAXIMUM_READ_BUFFER_SIZE):
      raise ValueError(u'Invalid maximum size value exceeds maximum.')

    if self._lines_buffer_offset >= self._file_object_size:
      return b''

    if maximum_size is None:
      read_size = self._MAXIMUM_READ_BUFFER_SIZE
    else:
      read_size = maximum_size

    if self._lines_buffer_offset + read_size > self._file_object_size:
      read_size = self._file_object_size - self._lines_buffer_offset

    if read_size > self._lines_buffer_size:
      data = self._lines_buffer
      self._lines_buffer = b''

      # Read the remaining requested data and a full lines buffer at once.
      read_size -= self._lines_buffer_size
      remaining_size = read_size
      read_size += self._LINES_BUFFER_SIZE

      if self._lines_buffer_offset + read_size > self._file_object_size:
        read_size = self._file_object_size - self._lines_buffer_offset

      self._file_object.seek(self._lines_buffer_offset, os.SEEK_SET)
      read_buffer = self._file_object.read(read_size)

      read_count = len(read_buffer)

      if remaining_size > read_count:
        remaining_size = read_count

      data += read_buffer[:remaining_size]

      if remaining_size < read_count:
        self._lines_buffer = read_buffer[remaining_size:]
        self._lines_buffer_size = read_count - remaining_size

      self._lines_buffer_offset += read_count

    else:
      data = self._lines_buffer[:read_size]

      self._lines_buffer = self._lines_buffer[read_size:]
      self._lines_buffer_size -= read_size

    return data

  # Note: that the following functions do not follow the style guide
  # because they are part of the readline file-like object interface.

  def readline(self, size=None):
    """Reads a single line of text.

    The functions reads one entire line from the file-like object.
    A trailing end-of-line indicator (newline by default) is kept in the
    string (but may be absent when a file ends with an incomplete line).
    If the size argument is present and non-negative, it is a maximum byte
    count (including the trailing end-of-line) and an incomplete line may
    be returned. An empty string is returned only when end-of-file is
    encountered immediately.

    Args:
      size: Optional integer value that contains the maximum string size
            to read. Default is None.

    Returns:
      A byte string containing a line of text.
    """
    if size is None or size <= 0:
      size = None

    next_offset = self._current_offset + self._lines_buffer_size

    if (self._end_of_line not in self._lines_buffer and
        next_offset == self._file_object_size):
      line = self._lines_buffer
      self._lines_buffer_size = 0
      self._lines_buffer = b''

      return line
    elif (self._end_of_line not in self._lines_buffer and
          (size is None or self._lines_buffer_size < size)):
      lines_data = self._ReadLinesData(size)

      result, separator, lines_data = lines_data.partition(self._end_of_line)

      if lines_data:
        self._lines_buffer = b''.join([lines_data, self._lines_buffer])
        self._lines_buffer_size = len(self._lines_buffer)

    else:
      result, separator, self._lines_buffer = self._lines_buffer.partition(
          self._end_of_line)
      self._lines_buffer_size -= len(result + separator)

    line = b''.join([result, separator])
    self._current_offset += len(line)

    return line

  def readlines(self, sizehint=None):
    """Reads lines of text.

    The function reads until EOF using readline() and return a list
    containing the lines read. If the optional sizehint argument is
    present, instead of reading up to EOF, whole lines totalling
    approximately sizehint bytes (possibly after rounding up to
    an internal buffer size) are read.

    Args:
      sizehint: optional integer value that contains the maximum byte size
                to read. Default is None.

    Returns:
      A list of byte strings containing a lines of text.
    """
    if sizehint is None or sizehint <= 0:
      sizehint = None

    lines = []
    lines_byte_size = 0
    line = self.readline()

    while line:
      lines.append(line)

      if sizehint is not None:
        lines_byte_size += len(line)

        if lines_byte_size >= sizehint:
          break

      line = self.readline()

    return lines

  # get_offset() is preferred above tell() by the libbfio layer used in libyal.
  def get_offset(self):
    """Returns the current offset into the file-like object."""
    return self._current_offset

  # Pythonesque alias for get_offet().
  def tell(self):
    """Returns the current offset into the file-like object."""
    return self._current_offset
