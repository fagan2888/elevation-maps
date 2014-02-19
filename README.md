Elevation-based Direction Mapping
=================================
Searches available alternate routes from Google Maps and provides information on
the corresponding changes in elevation, as well as XY distance travelled and
number of steps (proxying for number of turns, though this is fuzzy).

The **primary shortcoming** is the reliance upon Google to provide alternative
routes; ideally, the script would provide alternative routes on its own.

Using
-----
Just run `elevation-maps.py`. Depending on the input address, the elevation API
request may be too long--this needs to be changed. Will provide a dictionary
named `statistics` containing, by mode of transport, all alternate routes with
corresponding total decrease and increase in elevation, numsteps, and distance
in meters.

Dependencies
------------
Python:
* **json** (read data from Google)
* **numpy** (array manipulation)
* **pandas** (data manipulation)
* **requests** (download from http)
