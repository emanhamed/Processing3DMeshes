import argparse

import numpy as np
import openmesh
from vispy.io import write_mesh, read_mesh, load_data_file


def decimate(mesh, n_vertices):
    """Decimate a mesh with a target number of vertices."""
    decimater = openmesh.TriMeshDecimater(mesh)
    mod = openmesh.TriMeshModQuadricHandle()
    decimater.add(mod)
    decimater.initialize()
    decimater.decimate_to(n_vertices)
    mesh.garbage_collection()
    return mesh


def test_decimate():
    mesh = openmesh.TriMesh()

    # Test setup:
    #  1------2\
    #  |\   B | \
    #  |  \   |C 4
    #  | A  \ | /
    #  0------3/

    # Add vertices
    vhandle = []
    vhandle.append(mesh.add_vertex(np.array([0, 0, 0])))
    vhandle.append(mesh.add_vertex(np.array([0, 1, 0])))
    vhandle.append(mesh.add_vertex(np.array([1, 1, 0])))
    vhandle.append(mesh.add_vertex(np.array([1, 0, 0])))
    vhandle.append(mesh.add_vertex(np.array([1.5, 0.5, 0])))

    # Add faces
    faces = [[0, 1, 3], [1, 2, 3], [2, 4, 3]]
    for v in faces:
        face_vhandles = []
        face_vhandles.append(vhandle[v[0]])
        face_vhandles.append(vhandle[v[1]])
        face_vhandles.append(vhandle[v[2]])
        mesh.add_face(face_vhandles)

    decimated = decimate(mesh, 3)
    print(decimated.n_vertices())
    print(mesh.n_vertices())

    assert decimated.n_vertices() == 3


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_mesh')
    parser.add_argument('output_mesh')
    parser.add_argument('--vertices', type=int, default=6890)
    args = parser.parse_args()

    mesh = openmesh.read_trimesh(args.input_mesh)
    decimated = decimate(mesh, args.vertices)
    openmesh.write_mesh(args.output_mesh, decimated)
    vertices1, faces1, normals, nothin  = read_mesh("faust_ref.obj")
    vertices2, faces, normals, nothin  = read_mesh("testtest.obj")
