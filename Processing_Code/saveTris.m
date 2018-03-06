close all;
clc;
clear all;

%% Folder, files and configuration parameters
%Paths of the training and testing meshes to be croped and aligned
path = 'Z:\CV_Lab\DATASET\BU4D_registered\BU3D\RawData'

%% Process the files
% List the documents needed
files = dir(fullfile(path,'*.wrl'));
files = {files.name}';
nFrames = numel(files);
ResultsCroped = cell(1,nFrames);
ResultsSampled = cell(1,nFrames);
alpha = 10.00;
reduction = 1;

% Check if the sequence has been read or not
% if exist(fullfile('Pre-ProcessedData_TrainingSeq_Shape.mat'),'file')
%     fprintf('Loading the storaged sequence...');
%load(fullfile('Pre-ProcessedData_TrainingSeq_Shape.mat'));
%     fprintf(' done\n');
% else        % Read the sequence and storage vertex and faces in '.mat' file
     [ points3DfaceSeq, triSeq] = readWrlSeq( path, files, nFrames );
%     save('Pre-ProcessedData_TrainingSeq_Shape.mat', 'points3DfaceSeq')
    save('triSeq.mat', 'triSeq')