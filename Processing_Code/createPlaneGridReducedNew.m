function [ Xplane,Yplane, Zplane] = createPlaneGridReducedNew( principalDirections, points3Dface, xnose3D, ynose3D, val, pointsGridX, pointsGridY, reduction)
% Creates a gridded plane over the plane in front of the face. It uses the
% nose location in 3D and the principal components of the point cloud for
% the plane generation. The amount of points in X and Y directions should
% be given (usually is the same to have square images later on). The last  
% parameter regulates the reduction of the face.
% Inputs:
%           Zprincipal : Principal direction that matches with the normal to the plane
%           xFace, yFace : List of x and y coordinates for the 3D facial points 
%           xNose3D, yNose3D, zNose3D : Location of the nose
%           pointsGridX, pointsGridY : Number of points in x and y for the grid over the plane
%           reduction : Plane is limited by (minX, maxX) and (minY, maxY). This parameter will limit these for values by multiplying them by a factor between (0, 1)
%
% Outputs:
%           Xplane, Yplane, Zplane : Points of the grid in 3D
%
% NOTE: The function is considering that the face is aligned with two of the
% principal components in X and Y axis (or almost). This is very convinient
% due to the function 'meshgrid' that allows the creation of a grid in x, y 
% standard coordinates.
%
% TO DO (improvement):
% For a more precise result a homography should be calculated 
% align the facial points with respect to x, y standard coordinate system.
% After alignment grid should be created. And as a last step, all the
% points in the grid should be back to the xprincipal, yprincipal
% coordinate system using the inverse of the homography.


nose = [xnose3D, ynose3D, val];
% Principal directions 
 Yprincipal = principalDirections(:,1); % CAREFUL WITH THIS
 Xprincipal = principalDirections(:,2);
 Zprincipal = principalDirections(:,3);
% Projection information
proj_points = zeros(size(points3Dface));
proj_X = zeros(1, size(points3Dface,1));
proj_Y = zeros(1, size(points3Dface,1));  
for j = 1:size(points3Dface,1)
    proj_points(j,:) = points3Dface(j,:) - dot(points3Dface(j,:) - nose, Zprincipal')*Zprincipal';
    proj_X(j) = dot(proj_points(j,:) - nose, Xprincipal'); 
    proj_Y(j) = dot(proj_points(j,:) - nose, Yprincipal');
end
[~,maxXprinIdx] = max(proj_X);
[~,minXprinIdx] = min(proj_X);
[~,maxYprinIdx] = max(proj_Y);
[~,minYprinIdx] = min(proj_Y);
scatter3(proj_points(:,1),proj_points(:,2),proj_points(:,3),1,[0,0,1],'filled');
scatter3(proj_points(maxXprinIdx,1),proj_points(maxXprinIdx,2),proj_points(maxXprinIdx,3),20,[0,1,0],'filled');
scatter3(proj_points(minXprinIdx,1),proj_points(minXprinIdx,2),proj_points(minXprinIdx,3),20,[0,1,0],'filled');
scatter3(proj_points(maxYprinIdx,1),proj_points(maxYprinIdx,2),proj_points(maxYprinIdx,3),20,[1,0,0],'filled');
scatter3(proj_points(minYprinIdx,1),proj_points(minYprinIdx,2),proj_points(minYprinIdx,3),20,[1,0,0],'filled');
maxX = proj_points(maxXprinIdx,1);
minX = proj_points(minXprinIdx,1);
maxY = proj_points(maxYprinIdx,2);
minY = proj_points(minYprinIdx,2);
% Reduction of the limits
maxX = xnose3D + (maxX-xnose3D)*reduction;
minX = xnose3D - (xnose3D-minX)*reduction;
maxY = ynose3D + (maxY-ynose3D)*reduction;
minY = ynose3D - (ynose3D-minY)*reduction;

% Plane representation Ax + By + Cz + D = 0
A = Zprincipal(1);
B = Zprincipal(2);
C = Zprincipal(3);
D = -dot(Zprincipal, [xnose3D, ynose3D, val]);

%% Need affine transformations
% 1º- To see plane in X,Y,Z world original coordinates and sample
% 2º- To return the plane to the face coordinate system and then interpolate over the face
% Temporal solution -> TO CHANGE
xx = linspace(minX, maxX,pointsGridX);
yy = linspace(minY, maxY,pointsGridY);
[Xplane,Yplane] = meshgrid(xx,yy);
Zplane = (A*Xplane + B*Yplane + D)/(-C);

end

