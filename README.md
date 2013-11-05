Elevation Mapping
=================
Searches available alternate routes from Google Maps and provides information on
the corresponding changes in elevation, as well as XY distance travelled and
number of steps (proxying for number of turns, though this is fuzzy).

The **primary shortcoming** is the reliance upon Google to provide alternative
routes; ideally, the script would provide alternative routes on its own.

Required Python libraries:
* **json** (read data from Google)
* **numpy** (array manipulation)
* **pandas** (data manipulation)
* **urllib2** (download from http)
