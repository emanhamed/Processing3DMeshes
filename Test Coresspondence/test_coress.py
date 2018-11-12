import numpy as np
import json
import torch
import pickle
import torch_geometric.transforms as transforms
from torch_geometric.data import Batch, Data, DataLoader
from torch_geometric.nn import SplineConv
from torch_geometric.utils import degree
from vispy.io import write_mesh, read_mesh, load_data_file
import os.path as osp
import torch.nn.functional as F
from torch_geometric.datasets import FAUST
import torch_geometric.transforms as T
import os
import collections

def FindDuplicates(in_list):
    unique = set(in_list)
    for each in unique:
        count = in_list.count(each)
        if count > 1:
            print ('There are duplicates in this list' )
            return True
    print ('There are no duplicates in this list')
    return False



class MyTransform(object):
    def __call__(self, data):
        data.face, data.x = None, torch.ones(data.num_nodes, 1)
        return data

def norm(x, edge_index):
    deg = degree(edge_index[0], x.size(0), x.dtype, x.device) + 1
    return x / deg.unsqueeze(-1)

path = osp.join(osp.dirname(osp.realpath(__file__)), '..', 'data', 'FAUST')
pre_transform = T.Compose([T.FaceToEdge(), MyTransform()])
train_dataset = FAUST(path, True, T.Cartesian(), pre_transform)
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
d = train_dataset[0]


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = SplineConv(1, 32, dim=3, kernel_size=5, norm=False)
        self.conv2 = SplineConv(32, 64, dim=3, kernel_size=5, norm=False)
        self.conv3 = SplineConv(64, 64, dim=3, kernel_size=5, norm=False)
        self.conv4 = SplineConv(64, 64, dim=3, kernel_size=5, norm=False)
        self.conv5 = SplineConv(64, 64, dim=3, kernel_size=5, norm=False)
        self.conv6 = SplineConv(64, 64, dim=3, kernel_size=5, norm=False)
        self.fc1 = torch.nn.Linear(64, 256)
        self.fc2 = torch.nn.Linear(256, d.num_nodes)

    def forward(self, data):
        x, edge_index, pseudo = data.x, data.edge_index, data.edge_attr
        x = F.elu(norm(self.conv1(x, edge_index, pseudo), edge_index))
        x = F.elu(norm(self.conv2(x, edge_index, pseudo), edge_index))
        x = F.elu(norm(self.conv3(x, edge_index, pseudo), edge_index))
        x = F.elu(norm(self.conv4(x, edge_index, pseudo), edge_index))
        x = F.elu(norm(self.conv5(x, edge_index, pseudo), edge_index))
        x = F.elu(norm(self.conv6(x, edge_index, pseudo), edge_index))
        x = F.elu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = Net().to(device)
model.load_state_dict(torch.load("/home/eman/Documents/PhD/pytorch_geometric-master/examples/tr_faust_Tuesday__12_40am__.pt"))

def test():
    model.eval()
    correct = 0

    #for data in test_loader:
    pred = model(data.to(device)).max(1)[1]
    print (len(pred))
    pred.cpu().numpy()
    pred = pred.tolist()
    length = len(set(pred))
    print (len(pred))
    print (length)
    FindDuplicates(pred)

    json_object = {
        'mesh_indices': vertices,
        'predicted_vertex_indices': pred,
    }
    with open(out_File_Name, 'wt') as f:
        json.dump(json_object, f)
    #print (pred.shape)


#data_path = '/home/eman/Documents/PhD/pytorch_geometric-master/examples/Test Meshes/shapify/' #shapify data
#data_path = '/home/eman/Documents/PhD/pytorch_geometric-master/examples/ALL_FAUST/' #FAUST data
data_path = '/home/eman/Documents/PhD/body-modeling-master_initial/smpl-viewer/Data-survey-smpl/AllData/' #SMPL data
dirs= os.listdir(data_path)

for data_size in range(len(dirs)):
	vertices, faces, normals, nothin  = read_mesh(data_path+dirs[data_size])
	out_File_Name = dirs[data_size]+'.json'

	print (vertices.shape)
	print (faces.shape)
	vertices = vertices.astype(np.float)
	faces = faces.astype(np.int32)
	vertices = torch.tensor(vertices, dtype=torch.float)
	faces = torch.tensor(faces.T, dtype=torch.long)
	data = Data(pos=vertices)
	data.face = faces
	data = transforms.FaceToEdge()(data)
	data.face = None
	data.x = torch.ones((data.num_nodes, 1))
	data = transforms.Cartesian()(data)
	test_loader = DataLoader(data, batch_size=1)
	################
	vertices.cpu().numpy()
	vertices = vertices.tolist()
	test_acc = test()









#for epoch in range(100,101 ):
    #train(epoch)
    #Load a pre-trained model for testing
    #model.load_state_dict(torch.load("/home/eman/Documents/PhD/pytorch_geometric-master/examples/tr_faust_Tuesday__12_40am__.pt"))
    #test_acc = test()
    #print('Epoch: {:02d}, Test: {:.4f}'.format(epoch, test_acc))
