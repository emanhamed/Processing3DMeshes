function [ points3DfaceSeq, triSeq ] = readObjSeq( path, files, nFrames )
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
    [points3Dface,tri] = read_obj(fname);
%    fprintf('done\n');   
    points3DfaceSeq{i} = points3Dface;
    triSeq{i}= tri;    
end
% save(fullfile(path,'data.mat'), 'points3DfaceSeq', 'triSeq');

end

