'''
Title: metadata.py
Author: Clayton Bennett
Created: 14 February 2024
'''
#C:\Program Files\Autodesk\FBX\FBX Python SDK\2020.3.2\samples\ImportScene\DisplayUserProperties.py
#https://github.com/metarutaiga/FBXSDK/blob/master/samples/ExportScene05/main.cxx
#https://python.hotexamples.com/examples/fbx/FbxNode/-/python-fbxnode-class-examples.html
#https://discussions.unity.com/t/what-is-the-correct-way-to-set-fbx-user-properties-for-import-in-unity/120286/2

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
 for number of properties (columns for single sheet,rows for multisheet, etc) found, so that the property keys and custom FbxProperty variables can be reused
'''
lSdkManager = fbx.FbxManager.Create()
dict_curve_object_metadata = dict()
curve_object_metadata = fbx.FbxObject.Create(lSdkManager,"metadata_0")
def create_fbxPropertiesFrom_df_metadata(curve_object,lDatasNode):
    table_i=curve_object.df_metadata
    key_list=list(curve_object.df_metadata.keys())
    dict_unique_FbxProperty=dict()
    for col,value in enumerate(table_i):
        key=key_list[col]
        #unique_key = "key_"+str(key)+"__col_"+str(col)+"_row_"+str(row)
        dict_unique_FbxProperty.update({key:fbx.FbxPropertyString(fbx.FbxProperty.Create(curve_object_metadata,fbx.FbxStringDT,"metadata_"+str(key)+"_col"+str(col),key))})
        dict_unique_FbxProperty[key].Set(value)
        dict_curve_object_metadata.update({key:dict_unique_FbxProperty})
        #lDatasNode.AddChild(dict_unique_FbxProperty[key])
        # ConnectSrcObject(self, FbxObject, FbxConnection.EType = FbxConnection.eNone): argument 1 has unexpected type 'FbxPropertyString'
        curve_object_metadata
        lDatasNode.ConnectSrcObject(curve_object_metadata) ## works, makes file bigger, but not seen in CAD Assistant


