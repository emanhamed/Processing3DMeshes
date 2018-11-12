#Eman Ahmed - SnT
###############################################################################
import unittest
import numpy as np
import os
import time
from psbody.mesh import Mesh, MeshViewers, MeshViewer
from psbody.mesh.meshviewer import MeshViewerSingle
from pymesh import obj
from vispy.io import write_mesh, read_mesh, load_data_file
import math
import glob

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


axis = [0, 1, 0]
axis2 = [0, -1, 0]
theta_r = 3.6159#-1.3
theta_l = 1.3


#Reading all the data from the files
path = '/media/eman/HDD/SecondYear/ICIP/MV/M44/'
dirs= os.listdir(path)
saving_path = '/media/eman/HDD/SecondYear/ICIP/MV/M44_results/'


objFiles = [file for file in os.listdir(path) if file.endswith('.obj')]
bmpFiles = [file for file in os.listdir(path) if file.endswith('.bmp')]
objFiles.sort()
bmpFiles.sort()
print len(objFiles)

for i in range (len(objFiles)):
    #Displaying original faces
    #i = 24
    originalMeshFile = Mesh(filename = path + objFiles[i])
    originalMeshFile.texture_filepath = path + bmpFiles[i]

    leftVerts = originalMeshFile
    rightVerts = originalMeshFile

    #print vars(leftVerts)

    name = (objFiles[i])[:-4]

    mv = MeshViewer()

    mv.dynamic_meshes= [originalMeshFile]
    time.sleep(0.3)
    mv.save_snapshot(saving_path + name + '_frontal.png')
    #time.sleep(0.1)
    #mv.


     #Left view
    newleftVerts =  (np.dot(rotation_matrix(axis, theta_l), (leftVerts.v).transpose()))
    leftVerts.v = newleftVerts.transpose()
    #mv_l = MeshViewer()
    mv.dynamic_meshes= [leftVerts]
    time.sleep(0.3)
    mv.save_snapshot(saving_path + name + '_left.png')
    #write_mesh('left.obj',vertices=leftVerts.v, faces=leftVerts.f, normals=None, texcoords=None, overwrite=True)

    #time.sleep(0.1)


     #Right view
    #print ("Hi")
    newrightVerts =  (np.dot(rotation_matrix(axis, theta_r), (rightVerts.v).transpose()))
    rightVerts.v = newrightVerts.transpose()
    mv_r = MeshViewer()

    mv_r.dynamic_meshes = [rightVerts]
    time.sleep(0.3)
    mv_r.save_snapshot(saving_path + name + '_right.png')
    #write_mesh('right.obj',vertices=rightVerts.v, faces=rightVerts.f, normals=None, texcoords=None, overwrite=True)
    #print ("Hi again")
    #time.sleep(0.2)
