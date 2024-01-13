def degrees_to_compass(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degrees / (360.0 / len(directions))) % len(directions)
    return directions[index]

# Example usage:
# wind_direction_degrees = 2
# wind_direction_compass = degrees_to_compass(wind_direction_degrees)
# print(f"Wind Direction (Degrees): {wind_direction_degrees}°")
# print(f"Wind Direction (Compass): {wind_direction_compass}")