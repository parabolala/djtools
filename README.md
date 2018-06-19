# DJ Tools

The project contains a set of libraries for reading, writing and converting
media library information between different DJ Software applications.

# Features

  * Algoriddim djay Pro 2: read and parse library. Limited writing.
  * Rekordbox: read explorted XML library.

  * Conversion:
    * Convert cue points from Rekordbox XML format to matching tracks in djay Pro 2 library.

# Installing

```
# --process-dependency-links required for pulling an updated version of bpylist.
$ pip install Djtools --process-dependency-links

# Tests
$ pip install Djtools[test] --process-dependency-links && nosetests
```

# Usage

```
>>> # Explore djay Pro 2 database.
>>> from djtools.djay import Explorer
>>> e = Explorer()
>>> track = e.get_all_tracks()[0]
>>> print('{} - {}'.format(track.title.artist, track.title.title))

>>> # Parse rekordbox XML library.
>>> from djtools import rekordbox, matching, convert
>>> rbts = rekordbox.parse_xml_file()
>>> print(rbt.Artist, rbt.Name)

>>> # Transfer cue points from rekordbox XML library to matching tracks in djay Pro 2.
>>> for dj_t in e.get_all_tracks():
>>>     print(dj_t.title.artist + ' - ' + dj_t.title.title)
>>>     match = matching.find_matching_track(dj_t, rbts)
>>>     if match is not None:
>>>         e.save_track(convert.transfer_cue_points(match, dj_t))
>>>     print('===')
```

# Disclaimer

This is not an officially supported Google product.
