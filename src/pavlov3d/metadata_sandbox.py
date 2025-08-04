'''
Title: metadata_sandbox.py
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
import copy

from fbx import FbxProperty # metadata
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
from fbx import FbxManager
import fbx

'''
Data import
'''
d = 'D:\Documents_main\Work\Pavlov\data_sources\gratzer'
d = os.path.normpath(d)
d=d+"\\"+"MemphisAquiferChemistry.csv"
df = pd.read_csv(d)
df = pd.read_csv(d)
#df.columns

metadataColumns = list(df.columns[:14])
#metadataColumns
#df[metadataColumns]
f=df[metadataColumns]
f.keys()

row=7 #  well # 7, metadata for the data Object, not the datapoint

table_i=df[metadataColumns].iloc[row]

key_list=list(f.keys())
metadata_col=13 # some number in the metadataColumns # numerical reference a key
# down the line, just treat every property as a string
key_i = key_list[metadata_col]
value_i = table_i[metadata_col] # indiviudal metadata for the row, transformed sideways
value_i = table_i[key_i] # same same
'''
FBX SDK 
'''


###datapoint_metadata.GetName()
###lFbxType = lFbxProp.GetPropertyDataType()
##
##c=FbxProperty.Create(datapoint_metadata,fbx.FbxStringDT,"me","clayton")#.Set(FbxString("datapoint"))
##c.GetName()=='me'
##c.GetLabel()=='clayton'
##
##
##s=FbxProperty.Create(datapoint_metadata,fbx.FbxStringDT,"siteag","siteag")#.Set(FbxString("datapoint"))
##b=FbxProperty.Create(datapoint_metadata,fbx.FbxBoolDT,"USGS","USGS")#.Set(True)
##d=FbxProperty.Create(datapoint_metadata,fbx.FbxDoubleDT,"df[metadataColumns].iloc[1][13]","welldepthva")#.Set(FbxDouble(1234.567))
##s_custom_property = fbx.FbxPropertyString(s)
##b_custom_property = fbx.FbxPropertyBool1(b)
##d_custom_property = fbx.FbxPropertyDouble1(d)
##
##b_custom_property.Set(True)
##d_custom_property.Set(446.0)

'''
go through the colums headers/keys for the metadataColumns and create each FBX property.
Once they exist, cycle through each  data object (row), set the value, and assign the FbxProperty to the FbxObject
You may need to copy, rather than assign, such that the OOP doesnt reference the same FBX Property in two different data objects.
'''
'''
dict_FbxProperties=dict()
for i,key in enumerate(key_list):
    prop=FbxProperty.Create(datapoint_metadata,fbx.FbxStringDT,"metadata_"+str(i)+"_"+str(key),key)#.Set(FbxString("datapoint")
    custom_prop=fbx.FbxPropertyString(prop)
    dict_FbxProperties.update({key:custom_prop})
    # unfortunately i don't think we can effectively copy.deepcopy() the FbxProperty vars'''

lSdkManager = fbx.FbxManager.Create()
datapoint_metadata = fbx.FbxObject.Create(lSdkManager,"metadata_p0")
dict_curve_object_metadata = dict()
for row in range(0,len(df)):
    table_i=df[metadataColumns].iloc[row]
    dict_unique_FbxProperty=dict()
    for col,value in enumerate(table_i):
        key=key_list[col]
        unique_key = "key_"+str(key)+"__col_"+str(col)+"_row_"+str(row)
        #dict_unique_FbxProperty.update({unique_key:fbx.FbxPropertyString(FbxProperty.Create(datapoint_metadata,fbx.FbxStringDT,"metadata_"+str(key)+"_col"+str(col),key))})
        #dict_unique_FbxProperty[unique_key].Set(value)
        dict_unique_FbxProperty.update({key:fbx.FbxPropertyString(FbxProperty.Create(datapoint_metadata,fbx.FbxStringDT,"metadata_"+str(key)+"_col"+str(col),key))})
        dict_unique_FbxProperty[key].Set(value)
        dict_curve_object_metadata.update({row:dict_unique_FbxProperty})
        # is this actually necessary or can an FbxProperty object be resued?
        #dict_FbxProperties[key]
        ##custom_prop=fbx.FbxPropertyString(FbxProperty.Create(datapoint_metadata,fbx.FbxStringDT,"metadata_"+str(key)+"_col"+str(col),key))
        ##custom_prop.Set(value)

print('metadata_sandbox')

for key, value in dict_unique_FbxProperty.items():
    print((key, value))  
dict_unique_FbxProperty[key].Get()
dict_unique_FbxProperty[key].GetName()
dict_unique_FbxProperty[key].GetLabel()

# now to assign
'''
make dictionary for number of properties (columns for single sheet,rows for multisheet, etc) found, so that the property keys and custom FbxProperty variables can be reused
'''

