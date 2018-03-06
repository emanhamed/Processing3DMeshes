function imOut = removeOutliers( imIn, percentage, nbins )
% Function to remove a certain percentage of the data that are outliers.
% This values are higher than any other in the distribution. Before using
% this function it is needed to check in the original histogram that there
% is a break on the continuity of the function.
%   Inputs:
%           imIn : Initial image to analyze. Curvature map in our case
%           percentage : Upper value used as threshold
%           nbins : Number of bins for the histogram
%   Outpus:
%           imOut : Curvature map with outliers set to zero. 
%
% NOTE: Instead of setting to zero the outliers, it could could be improved
% by approximating this values to the nearest neighbours values, with
% bilinear approximation or any other.

[PixelCounts, values] = imhist(imIn, nbins); 
% Allocating the memory for the output
[nSize,mSize]=size(imIn);
imOut = zeros(size(imIn));

% Calculate CDF, Cumulative Distribution Function
cdf = zeros(1, nbins);
CDFPercentiles = zeros(100, 1);
CDFIndexes = uint32(zeros(100, 1));
% Get the Cumulative Distribution Function.
cdf = cumsum(PixelCounts);
% Now normalize the CDF to 0-1.
biggestValue = cdf(nbins);
normalizedCDF = cdf / biggestValue;
% And scale it for the range of the plot.
maxY = ylim;
scaledCDF = maxY(2) * normalizedCDF ;

% Find out what value corresponds to a given percentile.
valueAtGivenPercentile = zeros(100, 1);
[x, m, n] = unique(normalizedCDF);	 % Need to have no duplicate values in the x direction (which is the CDF).
y = values(m);
xi = 0.01 : 0.01 : 1.00;	% Make up an array to have every percentage from 1% to 100%
% Do the interpolation to get EVERY percent (even if it doesn't appear in the CDF).
valueAtGivenPercentile = interp1(x, y, xi);

lowestValueToPlot = valueAtGivenPercentile(1);
highestValueToPlot = valueAtGivenPercentile(percentage);
%xlim([lowestValueToPlot highestValueToPlot]);

% Return the image with only the non-rejected pixels
imInLine = imIn(:);
mask = (imInLine<highestValueToPlot);
imOutLine = imInLine.*mask;
imOut = reshape(imOutLine, [nSize mSize]);
end

