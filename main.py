import json
import simplekml
import argparse
from typing import Dict, List
import subprocess
import os
import platform

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

    def get_altitude_by_lower_limit(self, lower_limit: int) -> int:
        if lower_limit == 60:
            return 102
        elif lower_limit == 45:
            return 101
        elif lower_limit == 25:
            return 100
        else:  # lower_limit == 0 or any other value
            return 103

    def add_feature_to_kml(self, feature: Dict):
        name = feature.get('name', 'Unnamed Zone')
        identifier = feature.get('identifier', 'No ID')
        
        for geometry in feature.get('geometry', []):
            # Get altitude based on lowerLimit
            lower_limit = geometry.get('lowerLimit', 0)
            altitude = self.get_altitude_by_lower_limit(lower_limit)
            
            # Update description to include max altitude as the first attribute
            description = f"Max altitude: {lower_limit}m\nID: {identifier}\nType: {feature.get('type', 'N/A')}\nRestriction: {feature.get('restriction', 'N/A')}"

            polygon = self.kml.newpolygon(name=name, description=description)
            coords = geometry['horizontalProjection']['coordinates'][0]
            
            polygon.outerboundaryis = [(coord[0], coord[1], altitude) for coord in coords]
            
            # Use relativetoground instead of clamptoground
            polygon.altitudemode = simplekml.AltitudeMode.relativetoground
            polygon.extrude = 1

            # Get color based on lowerLimit
            color = self.get_color_by_lower_limit(lower_limit)

            # Set style
            polygon.style.linestyle.color = color
            polygon.style.linestyle.width = 2
            polygon.style.polystyle.color = simplekml.Color.changealphaint(128, color)  # 50% transparency

    def convert(self):
        data = self.read_input_file()
        self.process_features(data.get('features', []))
        self.kml.save(self.output_file)

def open_in_google_earth(kml_file: str, project_name: str):
    # Ensure the file path is absolute
    kml_file_abs = os.path.abspath(kml_file)
    
    system = platform.system()
    
    if system == "Windows":
        try:
            # Try common installation paths on Windows
            paths = [
                r"C:\Program Files\Google\Google Earth Pro\client\googleearth.exe",
                r"C:\Program Files (x86)\Google\Google Earth Pro\client\googleearth.exe"
            ]
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path, kml_file_abs])
                    print(f"Opening {kml_file} in Google Earth Pro")
                    return
            raise FileNotFoundError("Google Earth Pro executable not found")
        except Exception as e:
            print(f"Failed to open Google Earth Pro: {e}")
    
    elif system == "Darwin":  # macOS
        try:
            subprocess.Popen(["open", "-a", "Google Earth Pro", kml_file_abs])
            print(f"Opening {kml_file} in Google Earth Pro")
        except Exception as e:
            print(f"Failed to open Google Earth Pro: {e}")
    
    elif system == "Linux":
        try:
            subprocess.Popen(["google-earth-pro", kml_file_abs])
            print(f"Opening {kml_file} in Google Earth Pro")
        except Exception as e:
            print(f"Failed to open Google Earth Pro: {e}")
    
    else:
        print(f"Unsupported operating system: {system}")
    
    print(f"If Google Earth Pro didn't open, please open {kml_file} manually in Google Earth")

def main():
    parser = argparse.ArgumentParser(description="Convert D-Flight geozones to KML for Google Maps")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to the output KML file")
    parser.add_argument("--project", help="Google Earth Web project name (optional)")
    args = parser.parse_args()

    converter = DroneZoneConverter(args.input_file, args.output_file)
    converter.convert()
    print(f"Conversion complete. KML file saved as {args.output_file}")

    if args.project:
        open_in_google_earth(args.output_file, args.project)
        print(f"Attempting to open in Google Earth Pro with project: {args.project}")

if __name__ == "__main__":
    main()