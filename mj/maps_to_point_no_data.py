import folium
import math
import random

# Helper function to compute new lat/lon given a distance and bearing from an origin
# using a spherical Earth approximation.
def offset_coordinates(lat, lon, distance_km, bearing_deg):
    R = 6371.0  # approximate radius of Earth in km
    bearing_rad = math.radians(bearing_deg)
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    d = distance_km / R

    new_lat_rad = math.asin(
        math.sin(lat_rad) * math.cos(d) + math.cos(lat_rad) * math.sin(d) * math.cos(bearing_rad)
    )
    new_lon_rad = lon_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(d) * math.cos(lat_rad),
        math.cos(d) - math.sin(lat_rad) * math.sin(new_lat_rad)
    )

    new_lat = math.degrees(new_lat_rad)
    new_lon = math.degrees(new_lon_rad)
    return new_lat, new_lon

# Function to ask for a segment selection
def get_segment_choice():
    while True:
        try:
            choice = int(input("Enter the segment number (1-12) to select: "))
            if 1 <= choice <= 12:
                return choice
            else:
                print("Invalid choice. Please select a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to pick a random coordinate within a given segment
def pick_random_coordinate(segment, lat, lon, radius_km):
    angle_step = 360 / 12
    start_angle = (segment - 1) * angle_step
    end_angle = segment * angle_step

    random_angle = random.uniform(start_angle, end_angle)
    random_distance = random.uniform(0, radius_km)
    random_lat, random_lon = offset_coordinates(lat, lon, random_distance, random_angle)

    return random_lat, random_lon


def main():
    # Prompt user for lat/lon or use random if not provided
    lat_input = input("Enter latitude (or press Enter for random): ")
    if lat_input.strip() == "":
        lat = random.uniform(-90, 90)
    else:
        try:
            lat = float(lat_input)
        except ValueError:
            print("Invalid latitude. Using a random value.")
            lat = random.uniform(-90, 90)

    lon_input = input("Enter longitude (or press Enter for random): ")
    if lon_input.strip() == "":
        lon = random.uniform(-180, 180)
    else:
        try:
            lon = float(lon_input)
        except ValueError:
            print("Invalid longitude. Using a random value.")
            lon = random.uniform(-180, 180)

    # Prompt for radius
    radius_input = input("Enter radius in kilometers (default=10): ")
    try:
        radius_km = float(radius_input)
    except ValueError:
        radius_km = 10.0

    print(f"Using coordinates: lat={lat}, lon={lon} with radius={radius_km} km")

    # Set up a folium map similar to a typical street-level view
    # Google street view is usually around zoom level 14 or so.
    my_map = folium.Map(location=[lat, lon], zoom_start=14)

    # Divide the area into 12 radial sections
    sections = 12
    angle_step = 360 / sections

    for i in range(sections):
        start_angle = i * angle_step
        end_angle = (i + 1) * angle_step
        points = [(lat, lon)]  # start polygon at center

        # We'll sample points along the arc to form the polygon edge
        arc_samples = 5  # number of points along each arc
        step = (end_angle - start_angle) / arc_samples
        for s in range(arc_samples + 1):
            current_angle = start_angle + s * step
            new_lat, new_lon = offset_coordinates(lat, lon, radius_km, current_angle)
            points.append((new_lat, new_lon))
        # Close the polygon returning to center
        points.append((lat, lon))

        # Add the polygon to the map with a tooltip
        folium.Polygon(
            locations=points,
            color="blue",
            weight=2,
            fill=True,
            fill_color="cyan",
            fill_opacity=0.3,
            tooltip=f"Section {i+1}"
        ).add_to(my_map)

    # Ask the user to select a segment
    segment_choice = get_segment_choice()
    random_lat, random_lon = pick_random_coordinate(segment_choice, lat, lon, radius_km)
    print(f"Random coordinate in segment {segment_choice}: lat={random_lat}, lon={random_lon}")

    # Add a red dot for the random coordinate on the map
    folium.Marker(
        location=[random_lat, random_lon],
        popup=f"Random point in segment {segment_choice}",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(my_map)

    # Save the result
    output_file = "divided_map.html"
    my_map.save(output_file)
    print(f"\nMap successfully saved as {output_file}. Open it in a browser to view.")

if __name__ == "__main__":
    main()
