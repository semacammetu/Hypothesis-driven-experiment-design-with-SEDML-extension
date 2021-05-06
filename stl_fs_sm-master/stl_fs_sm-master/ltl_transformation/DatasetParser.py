import os
import pandas as pd

from XmlOperations import writeDatasetsToXml

sabit_folder = 'D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/test_data/traffic_data/traffic_data_l6'
xml = []
for file in os.listdir(sabit_folder):
    filepath = os.path.join(sabit_folder, file)
    data = []
    with open(filepath, 'r') as f:
        if not file.endswith('label') and not file.endswith('properties'):
            data = pd.read_csv(sabit_folder+'/'+file, sep=" ", header=None)
            data.columns = ["step", "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7"]
            #print(data)
            #xml.append(d2x(data))
            xml.append(data)

        f.close()
writeDatasetsToXml(xml)

