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
load(fullfile('Pre-ProcessedData_TrainingSeq_Shape.mat'));
%     fprintf(' done\n');
% else        % Read the sequence and storage vertex and faces in '.mat' file
%     [ points3DfaceSeq, triSeq] = readWrlSeq( path, files, nFrames );
%     save('Pre-ProcessedData_TrainingSeq_Shape.mat', 'points3DfaceSeq')
%save('Pre-ProcessedData_TrainingSeq_Shape.mat', 'points3DfaceSeq')
%
% end
% fprintf('Just finished reading the data \n');

% % % [points3Dface,tris] = read_wrl('Ref.wrl');
% % points3Dface = points3Dface';
% % [val, idx] = max(points3Dface(:,3));
% % noseR = points3Dface(idx,1);
% % noseC = points3Dface(idx,2);
% % 

load(fullfile('croppedIndex.mat'));
load(fullfile('triSeq.mat'));
%% CROP THE FACE
points3Dface = points3DfaceSeq{1};
points3Dface = points3Dface';
[val, idx] = max(points3Dface(:,3));
noseR = points3Dface(idx,1);
noseC = points3Dface(idx,2);
[faceCroppedIdx,~] = rangesearch(points3Dface,[noseR, noseC, val],26);
X = points3Dface(faceCroppedIdx{:},1);
Y = points3Dface(faceCroppedIdx{:},2);
Z = points3Dface(faceCroppedIdx{:}, 3);
points3Dface = [X,Y,Z];
save('croppedIndex.mat', 'faceCroppedIdx')
tris = triSeq{1,1}
% tris = tris';
F1 = tris(1,:);
F2 = tris(2,:);
F3 = tris(3,:);

count = 1;
newFaces = [];
for i = 1 :(length(F1))
    if ((ismember(F1(i),faceCroppedIdx{1,1})) && (ismember(F2(i),faceCroppedIdx{1,1})) && (ismember(F3(i),faceCroppedIdx{1,1})))
        idx1 = find(faceCroppedIdx{1,1} == F1(i));
        idx2 = find(faceCroppedIdx{1,1} == F2(i));
        idx3 = find(faceCroppedIdx{1,1} == F3(i));
        newFaces(count,:) = [idx1, idx2, idx3];
        count = count + 1;
    end
end

write_ply(points3Dface,newFaces,'NewRef.ply','ascii');



for i = 1:nFrames
    points3Dface = points3DfaceSeq{i};
    points3Dface = points3Dface';
    X = points3Dface(faceCroppedIdx{:},1);
    Y = points3Dface(faceCroppedIdx{:},2);
    Z = points3Dface(faceCroppedIdx{:}, 3);
    points3Dface = [X,Y,Z];
    
    tris = triSeq{1,i}
    % tris = tris';
    F1 = tris(1,:);
    F2 = tris(2,:);
    F3 = tris(3,:);
    
    count = 1;
    newFaces = [];
    for k = 1 :(length(F1))
        if ((ismember(F1(k),faceCroppedIdx{1,1})) && (ismember(F2(k),faceCroppedIdx{1,1})) && (ismember(F3(k),faceCroppedIdx{1,1})))
            idx1 = find(faceCroppedIdx{1,1} == F1(k));
            idx2 = find(faceCroppedIdx{1,1} == F2(k));
            idx3 = find(faceCroppedIdx{1,1} == F3(k));
            newFaces(count,:) = [idx1, idx2, idx3];
            count = count + 1;
        end
    end
    write_ply(points3Dface,newFaces,[erase(files{i,1},'.wrl') '.ply'],'ascii');
    
end
%write_ply(points3Dface,newFaces,'NewRef.ply','ascii');

%% FOR ALL THE FRAMES IN THE SEQUENCE

% % % % % % % % % % % % % % % parfor i = 1:nFrames
% % % % % % % % % % % % % % %     points3Dface = points3DfaceSeq{i};
% % % % % % % % % % % % % % %     points3Dface = points3Dface';
% % % % % % % % % % % % % % %     %% FIND THE NOSE
% % % % % % % % % % % % % % %     [val, idx] = max(points3Dface(:,3));
% % % % % % % % % % % % % % %     noseR = points3Dface(idx,1);
% % % % % % % % % % % % % % %     noseC = points3Dface(idx,2);
% % % % % % % % % % % % % % %
% % % % % % % % % % % % % % %     %% CROP THE FACE
% % % % % % % % % % % % % % %     [faceCroppedIdx,~] = rangesearch(points3Dface,[noseR, noseC, val],85);
% % % % % % % % % % % % % % %     X = points3Dface(faceCroppedIdx{:},1);
% % % % % % % % % % % % % % %     Y = points3Dface(faceCroppedIdx{:},2);
% % % % % % % % % % % % % % %     Z = points3Dface(faceCroppedIdx{:}, 3);
% % % % % % % % % % % % % % %     points3Dface = [X,Y,Z];
%ResultsCroped{i}=points3Dface;




% % % % %     principalDirections = pca([X,Y,Z]);
% % % % %     Xprincipal = principalDirections(:,1);
% % % % %     Yprincipal = principalDirections(:,2);
% % % % %     Zprincipal = principalDirections(:,3);
% % % % %
% % % % %     pointsGridX = 115;%round(sqrt(size(points3Dface,1)/alpha));
% % % % %     pointsGridY = 115;%pointsGridX;
% % % % %     pointsGridTotal = pointsGridX*pointsGridY;
% % % % %     [ Xplane,Yplane, Zplane] = createPlaneGridReducedNew( principalDirections, points3Dface, noseR, noseC, val, pointsGridX, pointsGridY, reduction);
% % % % %     % Representing the grid
% % % % %     XplaneLine = Xplane(:);
% % % % %     YplaneLine = Yplane(:);
% % % % %     ZplaneLine = Zplane(:);
% % % % %     % Interpolating over the surface, around the grid projection
% % % % %     %    fprintf('Interpolation over surface with grid...');
% % % % %     F = scatteredInterpolant(X,Y,Z,'nearest');  %%%% , 'nearest'PROBLEM HERE .....// Points go to the back the data get corrupted
% % % % %     Zq = F(Xplane,Yplane);
% % % % %
% % % % %     newX = reshape(Xplane,[13225,1]);
% % % % %     newY = reshape(Yplane,[13225,1]);
% % % % %     newZ = reshape(Zq,[13225,1]);
% % % % %     Result = [newX,newY,newZ];
% % % % %     write_ply(Result,tri,[erase(files{i},'.wrl') '.ply'],'ascii');
% % % % %
% % % % % end
%save('ResultsSampled_TrainingSeq_Shape.mat', 'ResultsSampled');
%save('ResultsCropped_TrainingSeq_Shape.mat','ResultsCroped');
