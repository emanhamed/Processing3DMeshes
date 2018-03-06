function [ points3DfaceSeq, triSeq ] = readPlySeq( path, files, nFrames )
% Function to read '.obj' files and save the 3D points and the faces
%       Inputs:
%               path : full path of the sequence 
%               files : list of the files ('.obj' files)
%               nFrames : total amount of frames for a sequence
%       Outpus:
%               points3DfaceSeq : cell array with the 3D point cloud for each frame
%               triSeq : cell array with the faces of the 3D point cloud for each frame

points3DfaceSeq = cell(1,nFrames);
triSeq = cell(1,nFrames);
for i = 1:nFrames
%    fprintf('\n --------------------------\n');
%    fprintf('FRAME %d\n', i);
%    fprintf('Reading ... ');
    fname = fullfile(path, files{i});
    %[points3Dface,tri] = read_obj(fname);
    [points3Dface,tri] = read_ply(fname);
    %val = int(87727/3);
    %new = reshape (tri,[val,3]);
    %mesh = readObj(fname);
    %points3Dface = mesh.v;
    %tri = mesh.f.v;
%    fprintf('done\n');   
    points3DfaceSeq{i} = points3Dface;
    triSeq{i}= tri;    
end
% save(fullfile(path,'data.mat'), 'points3DfaceSeq', 'triSeq');

end

