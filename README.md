# Simple utility to convert d-flight UAS Geo Zone to KML

# Installation

1. Ensure you have Python 3.6 or newer installed.
2. Clone this repository or download the source code.
3. Install the required packages:

```
pip install -r requirements.txt
```

# Usage

```
python main.py input.json output.kml --open
```

# Notes
- The input file should be a valid GeoJSON file from d-flight UAS Geo Zone. Probably works with other GeoJSON files, but that's not tested.
- The output file will be a KML file.
- If you want to open the KML file in Google Earth Pro desktop, you can use the `--open` flag.
