# Simple utility to convert d-flight UAS Geo Zone to KML

# Usage

```
python main.py input.json output.kml --project "My Project"
```

# Notes
- The input file should be a valid GeoJSON file from d-flight UAS Geo Zone. Probably works with other GeoJSON files, but that's not tested.
- The output file will be a KML file.
- If you want to open the KML file in Google Earth Pro desktop, you can use the `--project` flag to specify the project name.