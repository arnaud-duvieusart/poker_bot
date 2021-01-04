

def discretize(val, val_min, val_max, max_points):
    # TODO: try non-linear spacing between discrete points
    step_size = (val_max - val_min) / max_points

    closest_distance = float("inf")
    current_best = None

    # Iterate through all discrete points and compare their distance to val to get the closest one.
    for index in range(1, max_points + 1):
        point = step_size * index
        distance = abs(val - point)
        if distance < closest_distance:
            closest_distance = distance
            current_best = point

    return current_best

def discretize_price(val):
    return discretize(val, 0, 1, 4)
