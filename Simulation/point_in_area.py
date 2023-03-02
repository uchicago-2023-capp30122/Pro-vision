import geopandas as gpd

def point_in_area(points, polygon):
    """
    Verifies whether a point in a given set is geographically within an area.
    Parameters:
    Returns
    """

    for p in points:
        if p.within(polygon):
            return True
    return False 