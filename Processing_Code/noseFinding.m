function [ xNose, yNose, zNose ] = noseFinding( points3Dface, uvMap, img )
% Function to find the nose using Viola Jones method over a 2D image, and
% maps back into 3D. Once the 3D area is bounded, point with the minimum
% depth is located as the nose-tip.
%
%   Inputs:
%           points3Dface : 3D points of the face
%           uvMap :  relationship between 2D image and 3D point cloud
%           img :   2D facial image

rdist = 10;  % Value in pixels

faceDetector = vision.CascadeObjectDetector('Nose'); 
faceDetector.MergeThreshold = 10;  % Avoid to get more than one detection     
bbox = step(faceDetector, img);
%%% Middle point of the box, return to 3D interpolation, find among neighbors
noseTipY = bbox(1)+ idivide(bbox(3),uint32(2)); % Y is horizontal
noseTipX = bbox(2)+ idivide(bbox(4),uint32(2)); % X is vertical
noseTipY = double(noseTipY);
noseTipX = double(noseTipX);
% Converting map from normalized to point in image
[height, width] = size(img);
npixels = size(points3Dface,1);
a = repmat([height width], npixels, 1); % Repetition of the size of the 2D image
uvMapPoints2D = uvMap.*a;                % Conversion of the normalized 2D points

% Look for uv points around the found nose
noseGuess = [noseTipY, noseTipX];
[possibleNose, distNeigh] = rangesearch(uvMapPoints2D,noseGuess,rdist);
% Map back to 3D points
[~,idx]=ismember(uvMapPoints2D(possibleNose{:},:), uvMapPoints2D, 'rows');
% Find among the selected ones, the one with minimum depth
points3Dpossible = points3Dface(idx);
[zNose, pos] = max(points3Dpossible(:,3));
xNose = points3Dpossible(pos,1);
yNose = points3Dpossible(pos,2);



end

