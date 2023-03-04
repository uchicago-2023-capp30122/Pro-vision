


###### SOURCE: https://pro.arcgis.com/en/pro-app/latest/tool-reference/analysis/polygon-neighbors.htm #####

import arcpy

arcpy.management.MakeFeatureLayer(r"C:\Data\Canada\CanadaElecDist.shp", 
                                  "Canada_ElectoralDist")

arcpy.management.SelectLayerByAttribute("Canada_ElectoralDist", "NEW_SELECTION", 
                                        "\"PROVCODE\" = 'NS'")
count = arcpy.management.GetCount("Canada_ElectoralDist")[0]
print("Selected feature count: {}".format(count))

arcpy.analysis.PolygonNeighbors("Canada_ElectoralDist", 
                                r"C:\Data\Output\NS_elec_neigh.dbf", "ENNAME")
print(arcpy.GetMessages())





###### SETU #######
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# Connect to your ArcGIS Online organization or Portal for ArcGIS
gis = GIS("https://www.arcgis.com", "username", "password")

# Specify the feature layer containing the polygons
layer_url = "https://services.arcgis.com/{your-org-id}/arcgis/rest/services/{your-layer-name}/FeatureServer/0"
layer = FeatureLayer(layer_url, gis=gis)

# Define the query to retrieve the polygon of interest
query = layer.query(where="OBJECTID = 1", out_fields="*")

# Get the geometry of the polygon
geometry = query.features[0].geometry

# Use the `query` method to find the neighboring polygons
neighboring_features = layer.query(geometry=geometry, spatial_relationship="esriSpatialRelTouches")

# Print the OBJECTIDs of the neighboring polygons
for feature in neighboring_features.features:
    print(feature.attributes["OBJECTID"])