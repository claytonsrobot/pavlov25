'''
Title: metadata.py
Author: Clayton Bennett
Created: 14 February 2024
'''
#C:\Program Files\Autodesk\FBX\FBX Python SDK\2020.3.2\samples\ImportScene\DisplayUserProperties.py
#https://github.com/metarutaiga/FBXSDK/blob/master/samples/ExportScene05/main.cxx
#https://python.hotexamples.com/examples/fbx/FbxNode/-/python-fbxnode-class-examples.html
#https://discussions.unity.com/t/what-is-the-correct-way-to-set-fbx-user-properties-for-import-in-unity/120286/2

'''
df[metadataColumns].iloc[1]
siteag         USGS_350114090071701
stationnm                  Sh:J-146
agencycd                       USGS
mediumcd                         WG
sampledt                      36769
year                           2000
sampletm                   0.534722
dttm                    36769.53472
altva                           247
declatva                  35.020649
declongva                -90.121482
nataqfrcd                S100MSEMBM
aqfrcd                      124MMPS
welldepthva                   446.0
Name: 1, dtype: object
'''
import os
if False:
    import pandas as pd

""" from fbx import FbxProperty # metadata
from fbx import FbxString
#from fbx import FbxBool # nope
from fbx import FbxDouble4
from fbx import FbxStringDT
from fbx import FbxBoolDT
from fbx import FbxDoubleDT
#from fbx import FbxObjectMetaData # nope
from fbx import FbxObject # supposedly not different from FbxObjectMetaData
from fbx import FbxPropertyFlags
from fbx import FbxDataType
from fbx import FbxManager """
import fbx
 
# (lProperty.GetFlag(FbxPropertyFlags::eUserDefined))
'''
Data import
'''
d = os.path.normpath(d)
d=d+"\\"+"MemphisAquiferChemistry.csv"
df = pd.read_csv(d)
df = pd.read_csv(d)
#df.columns

metadataColumns = list(df.columns[:14])
#metadataColumns
#df[metadataColumns]
df_metadata=df[metadataColumns]
df_metadata.keys()

row=7 #  well # 7, metadata for the data Object, not the datapoint

table_i=df[metadataColumns].iloc[row]
key_list=list(df_metadata.keys())
metadata_col=13 # some number in the metadataColumns # numerical reference a key
# down the line, just treat every property as a string
key_i = key_list[metadata_col]
value_i = table_i[metadata_col] # indiviudal metadata for the row, transformed sideways
value_i = table_i[key_i] # same same
'''
FBX SDK 
'''
lSdkManager = fbx.FbxManager.Create()

dict_curve_object_metadata = dict()
for row in range(0,len(df)):
    table_i=df[metadataColumns].iloc[row]
    dict_unique_FbxProperty=dict()
    for col,value in enumerate(table_i):
        key=key_list[col]
        unique_key = "key_"+str(key)+"__col_"+str(col)+"_row_"+str(row)
        dict_unique_FbxProperty.update({key:fbx.FbxPropertyString(fbx.FbxProperty.Create(curve_object_metadata,fbx.FbxStringDT,"metadata_"+str(key)+"_col"+str(col),key))})
        dict_unique_FbxProperty[key].Set(value)
        dict_curve_object_metadata.update({row:dict_unique_FbxProperty})

print('metadata.py')
for key, value in dict_unique_FbxProperty.items():
    print((key, value))  
dict_unique_FbxProperty[key].Get()
dict_unique_FbxProperty[key].GetName()
dict_unique_FbxProperty[key].GetLabel()

# now to assign
'''
make dictionary for number of properties (columns for single sheet,rows for multisheet, etc) found, so that the property keys and custom FbxProperty variables can be reused
'''
curve_object_metadata = fbx.FbxObject.Create(lSdkManager,"metadata_0")

def create_fbxPropertiesFrom_df_metadata(curve_object,lDatasNode):
    table_i=curve_object.df_metadata
    dict_unique_FbxProperty=dict()
    for col,value in enumerate(table_i):
        key=key_list[col]
        #unique_key = "key_"+str(key)+"__col_"+str(col)+"_row_"+str(row)
        dict_unique_FbxProperty.update({key:fbx.FbxPropertyString(fbx.FbxProperty.Create(curve_object_metadata,fbx.FbxStringDT,"metadata_"+str(key)+"_col"+str(col),key))})
        dict_unique_FbxProperty[key].Set(value)
        dict_curve_object_metadata.update({row:dict_unique_FbxProperty})
        #lDatasNode.AddChild(dict_unique_FbxProperty[key])
        # ConnectSrcObject(self, FbxObject, FbxConnection.EType = FbxConnection.eNone): argument 1 has unexpected type 'FbxPropertyString'
        curve_object_metadata
        lDatasNode.ConnectSrcObject(curve_object_metadata) ## works, makes file bigger, but not seen in CAD Assistant


