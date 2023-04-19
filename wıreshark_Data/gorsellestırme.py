import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd
from fastkml import kml

from pykml import parser
import re
import folium

# Wireshark'ın Python API'sini import edin
from pyshark import FileCapture

# Ağ izlemeyi başlatın
capture = FileCapture("wire.pcap")

# Verileri toplayın
for packet in capture:
    # Paket içeriğini ekrana yazdırın
    print(packet)
