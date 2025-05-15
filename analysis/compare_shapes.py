import numpy as np

def compare_mouth_shapes(normal_coords, error_coords):
    normal = np.array(normal_coords)
    error = np.array(error_coords)

    if normal.shape != error.shape:
        raise ValueError("Shape mismatch")

    diff = np.linalg.norm(normal - error, axis=1)
    avg_diff = np.mean(diff)
    return avg_diff
def calculate_similarity(normal_coords, error_coords, scale=400):
    normal = np.array(normal_coords)
    error = np.array(error_coords)

    if normal.shape != error.shape:
        raise ValueError("Shape mismatch")

    diff = np.linalg.norm(normal - error, axis=1)
    avg_diff = np.mean(diff)

    similarity = max(0, 100 - (avg_diff * scale))
    return round(similarity, 2)