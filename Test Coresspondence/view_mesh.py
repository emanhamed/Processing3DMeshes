import argparse
import glob
import json
import logging
import os.path
import sys

import numpy as np
import vispy
import vispy.color
import vispy.scene
import vispy.visuals
from psbody.mesh import Mesh, MeshViewers, MeshViewer
from vispy.io import write_mesh, read_mesh, load_data_file
import os
import time , math
import matplotlib
import matplotlib.cm as cm


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



parser = argparse.ArgumentParser(
    description='display correspondence results'
)
#parser.add_argument('mesh_file', help='npz file with the mesh data')
parser.add_argument('--case', choices=('Shapify', 'Faust','MPI','ref'),
                    default='ref')
args = parser.parse_args()


if args.case == 'ref':
	ref = '/home/eman/Documents/PhD/pytorch_geometric-master/examples/ref.obj'

	mesh = Mesh(filename = ref)

	if mesh.v.max() > 1e3:
		mesh.v /= 1e3

	n_vertices = len(mesh.v)

	prediction_vertex_values = np.arange(n_vertices)

	minima = min(prediction_vertex_values)
	maxima = max(prediction_vertex_values)
	norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
	mapper = cm.ScalarMappable(norm=norm, cmap=cm.viridis)

	mapper_list = [mapper.to_rgba(x)[0] for x in prediction_vertex_values]

	mesh.vc = mapper_list
	mv = MeshViewer()
	mv.dynamic_meshes= [mesh]
	time.sleep(100)
	mv.save_snapshot('/home/eman/Documents/PhD/pytorch_geometric-master/examples/reference-mesh.png')





####################################################################

if args.case == 'MPI':
	data_path = '/home/eman/Documents/PhD/body-modeling-master_initial/smpl-viewer/Data-survey-smpl/AllData/'
	dirs= os.listdir(data_path)
	dirs.sort()

	print (dirs)

	meshes = []

	for data_size in range(len(dirs)):
		prediction_file = dirs[data_size]+'.json'
		with open(prediction_file, 'rt') as f:
			prediction_data = json.load(f)

		mesh_indices = prediction_data['mesh_indices']
		mesh_index = None if len(mesh_indices) == 0 else mesh_indices[0]
		predicted_indices = np.array(
		prediction_data['predicted_vertex_indices'][:],
		dtype=int
		)

		test_Mesh = data_path + dirs[data_size]
		#vertices, faces, normals, nothin  = read_mesh(args.mesh_file)
		test_vertices, test_faces, normals, nothin  = read_mesh(test_Mesh)

		#if vertices.max() > 1e3:
		#	vertices /= 1e3

		if test_vertices.max() > 1e3:
			test_vertices /= 1e3

		n_vertices = len(test_vertices)

		assert n_vertices == len(predicted_indices), \
		'number of vertices do not match {:d} != {:d}' \
		.format(n_vertices, len(predicted_indices))


		prediction_vertex_values = predicted_indices

		minima = min(prediction_vertex_values)
		maxima = max(prediction_vertex_values)
		norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
		mapper = cm.ScalarMappable(norm=norm, cmap=cm.viridis)

		mapper_list = [mapper.to_rgba(x)[0] for x in prediction_vertex_values]

		mesh = Mesh(v=test_vertices,f=test_faces, vc = mapper_list)#,vc=prediction_vertex_values)
		meshes.append(mesh)


	mvs = MeshViewers(shape=[6, 6])
	print len(meshes)
	print meshes




	mvs[5][0].set_static_meshes([meshes[6]])
	mvs[5][1].set_static_meshes([meshes[7]])
	mvs[5][2].set_static_meshes([meshes[8]])
	mvs[5][3].set_static_meshes([meshes[9]])
	mvs[5][4].set_static_meshes([meshes[10]])
	mvs[5][5].set_static_meshes([meshes[11]])

	mvs[4][0].set_static_meshes([meshes[0]])
	mvs[4][1].set_static_meshes([meshes[2]])
	mvs[4][2].set_static_meshes([meshes[1]])
	mvs[4][3].set_static_meshes([meshes[3]])
	mvs[4][4].set_static_meshes([meshes[5]])
	mvs[4][5].set_static_meshes([meshes[4]])

	mvs[3][0].set_static_meshes([meshes[12]])
	mvs[3][1].set_static_meshes([meshes[13]])
	mvs[3][2].set_static_meshes([meshes[14]])
	mvs[3][3].set_static_meshes([meshes[15]])
	mvs[3][4].set_static_meshes([meshes[16]])
	mvs[3][5].set_static_meshes([meshes[17]])

	mvs[2][0].set_static_meshes([meshes[18]])
	mvs[2][1].set_static_meshes([meshes[19]])
	mvs[2][2].set_static_meshes([meshes[20]])
	mvs[2][3].set_static_meshes([meshes[21]])
	mvs[2][4].set_static_meshes([meshes[22]])
	mvs[2][5].set_static_meshes([meshes[23]])

	mvs[1][0].set_static_meshes([meshes[24]])
	mvs[1][1].set_static_meshes([meshes[25]])
	mvs[1][2].set_static_meshes([meshes[26]])
	mvs[1][3].set_static_meshes([meshes[27]])
	mvs[1][4].set_static_meshes([meshes[28]])
	mvs[1][5].set_static_meshes([meshes[29]])


	mvs[0][0].set_static_meshes([meshes[30]])
	mvs[0][1].set_static_meshes([meshes[31]])
	mvs[0][2].set_static_meshes([meshes[32]])
	mvs[0][3].set_static_meshes([meshes[33]])
	mvs[0][4].set_static_meshes([meshes[34]])
	mvs[0][5].set_static_meshes([meshes[35]])

	time.sleep(1000)

##################################################################################################

if args.case == 'Shapify':
	data_path = '/home/eman/Documents/PhD/pytorch_geometric-master/examples/Test Meshes/shapify/'
	dirs= os.listdir(data_path)
	dirs.sort()

	print (dirs)

	meshes = []

	for data_size in range(len(dirs)):
		prediction_file = dirs[data_size]+'.json'
		with open(prediction_file, 'rt') as f:
			prediction_data = json.load(f)

		mesh_indices = prediction_data['mesh_indices']
		mesh_index = None if len(mesh_indices) == 0 else mesh_indices[0]
		predicted_indices = np.array(
		prediction_data['predicted_vertex_indices'][:],
		dtype=int
		)

		test_Mesh = data_path + dirs[data_size]
		#vertices, faces, normals, nothin  = read_mesh(args.mesh_file)
		test_vertices, test_faces, normals, nothin  = read_mesh(test_Mesh)

		if test_vertices.max() > 1e3:
			test_vertices /= 1e3

		#if test_vertices.max() > 1e3:
		#	test_vertices /= 1e3

		n_vertices = len(test_vertices)

		assert n_vertices == len(predicted_indices), \
		'number of vertices do not match {:d} != {:d}' \
		.format(n_vertices, len(predicted_indices))


		prediction_vertex_values = predicted_indices

		angle1 = 1.5708
		angle2 = 1.5708

		axis1 = [0, 1, 0]
		axis2 = [0, 0, 1]

		verts =  (np.dot(rotation_matrix(axis1, angle1), test_vertices.transpose()))
		newVerts =  (np.dot(rotation_matrix(axis2, angle2), verts))

		minima = min(prediction_vertex_values)
		maxima = max(prediction_vertex_values)
		norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
		mapper = cm.ScalarMappable(norm=norm, cmap=cm.viridis)

		mapper_list = [mapper.to_rgba(x)[0] for x in prediction_vertex_values]

		mesh = Mesh(v=newVerts.transpose(),f=test_faces, vc = mapper_list)#,vc=prediction_vertex_values)
		#mesh = Mesh(v=test_vertices,f=test_faces, vc = mapper_list)
		meshes.append(mesh)

	mvs = MeshViewers(shape=[2, 5])
	print len(meshes)


	#Original FAUST
	mvs[1][0].set_static_meshes([meshes[0]])
	mvs[1][1].set_static_meshes([meshes[1]])
	mvs[1][2].set_static_meshes([meshes[2]])
	mvs[1][3].set_static_meshes([meshes[3]])
	mvs[1][4].set_static_meshes([meshes[4]])

	#level3
	mvs[0][0].set_static_meshes([meshes[5]])
	mvs[0][1].set_static_meshes([meshes[6]])
	mvs[0][2].set_static_meshes([meshes[7]])
	mvs[0][3].set_static_meshes([meshes[8]])
	mvs[0][4].set_static_meshes([meshes[9]])

	time.sleep(100)


########################################################################################


if args.case =='Faust':
	data_path = '/home/eman/Documents/PhD/pytorch_geometric-master/examples/ALL_FAUST/'
	dirs= os.listdir(data_path)
	dirs.sort()
	meshes = []

	for data_size in range(len(dirs)):
		prediction_file = dirs[data_size]+'.json'
		with open(prediction_file, 'rt') as f:
			prediction_data = json.load(f)

		mesh_indices = prediction_data['mesh_indices']
		mesh_index = None if len(mesh_indices) == 0 else mesh_indices[0]
		predicted_indices = np.array(
		prediction_data['predicted_vertex_indices'][:],
		dtype=int
		)

		test_Mesh = data_path + dirs[data_size]
		#vertices, faces, normals, nothin  = read_mesh(args.mesh_file)
		test_vertices, test_faces, normals, nothin  = read_mesh(test_Mesh)

		#if vertices.max() > 1e3:
		#	vertices /= 1e3

		if test_vertices.max() > 1e3:
			test_vertices /= 1e3

		n_vertices = len(test_vertices)

		assert n_vertices == len(predicted_indices), \
		'number of vertices do not match {:d} != {:d}' \
		.format(n_vertices, len(predicted_indices))

		
		prediction_vertex_values = predicted_indices
		ref_vertex_values = np.arange(n_vertices)

		minima = min(prediction_vertex_values)
		maxima = max(prediction_vertex_values)
		norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
		mapper = cm.ScalarMappable(norm=norm, cmap=cm.viridis)
		mapper_list = [mapper.to_rgba(x)[0] for x in prediction_vertex_values]

		mesh = Mesh(v=test_vertices,f=test_faces, vc = mapper_list)
		meshes.append(mesh)
	mvs = MeshViewers(shape=[5, 4])


	#Original FAUST
	mvs[4][0].set_static_meshes([meshes[0]])
	mvs[4][1].set_static_meshes([meshes[1]])
	mvs[4][2].set_static_meshes([meshes[2]])
	mvs[4][3].set_static_meshes([meshes[3]])

	#level 1
	mvs[3][0].set_static_meshes([meshes[8]])
	mvs[3][1].set_static_meshes([meshes[9]])
	mvs[3][2].set_static_meshes([meshes[10]])
	mvs[3][3].set_static_meshes([meshes[11]])

	#level 2
	mvs[2][0].set_static_meshes([meshes[12]])
	mvs[2][1].set_static_meshes([meshes[13]])
	mvs[2][2].set_static_meshes([meshes[14]])
	mvs[2][3].set_static_meshes([meshes[15]])


	#level3
	mvs[1][0].set_static_meshes([meshes[16]])
	mvs[1][1].set_static_meshes([meshes[17]])
	mvs[1][2].set_static_meshes([meshes[18]])
	mvs[1][3].set_static_meshes([meshes[19]])

	#Level 4
	mvs[0][0].set_static_meshes([meshes[4]])
	mvs[0][1].set_static_meshes([meshes[5]])
	mvs[0][2].set_static_meshes([meshes[6]])
	mvs[0][3].set_static_meshes([meshes[7]])

	time.sleep(100)
