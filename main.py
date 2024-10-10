import json
import simplekml
import argparse
from typing import Dict, List

class DroneZoneConverter:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.kml = simplekml.Kml()

    def read_input_file(self) -> Dict:
        with open(self.input_file, 'r') as f:
            return json.load(f)

    def process_features(self, features: List[Dict]):
        for feature in features:
            self.add_feature_to_kml(feature)

    def get_color_by_lower_limit(self, lower_limit: int) -> simplekml.Color:
        if lower_limit == 60:
            return simplekml.Color.cyan
        elif lower_limit == 45:
            return simplekml.Color.yellow
        elif lower_limit == 25:
            return simplekml.Color.orange
        else:  # lower_limit == 0 or any other value
            return simplekml.Color.red

    def add_feature_to_kml(self, feature: Dict):
        name = feature.get('name', 'Unnamed Zone')
        identifier = feature.get('identifier', 'No ID')
        description = f"ID: {identifier}\nType: {feature.get('type', 'N/A')}\nRestriction: {feature.get('restriction', 'N/A')}"

        for geometry in feature.get('geometry', []):
            polygon = self.kml.newpolygon(name=name, description=description)
            coords = geometry['horizontalProjection']['coordinates'][0]
            
            # Set a high altitude (e.g., 10000 meters) for better visibility
            polygon.outerboundaryis = [(coord[0], coord[1], 10000) for coord in coords]
            
            # Use clamptoground instead of relativetoground
            polygon.altitudemode = simplekml.AltitudeMode.clamptoground
            polygon.extrude = 1

            # Get color based on lowerLimit
            lower_limit = geometry.get('lowerLimit', 0)
            color = self.get_color_by_lower_limit(lower_limit)

            # Set style
            polygon.style.linestyle.color = color
            polygon.style.linestyle.width = 2
            polygon.style.polystyle.color = simplekml.Color.changealphaint(128, color)  # 50% transparency

    def convert(self):
        data = self.read_input_file()
        self.process_features(data.get('features', []))
        self.kml.save(self.output_file)

def main():
    parser = argparse.ArgumentParser(description="Convert D-Flight geozones to KML for Google Maps")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to the output KML file")
    args = parser.parse_args()

    converter = DroneZoneConverter(args.input_file, args.output_file)
    converter.convert()
    print(f"Conversion complete. KML file saved as {args.output_file}")

if __name__ == "__main__":
    main()