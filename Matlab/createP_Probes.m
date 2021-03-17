%=========================================================================
% createP_Probes.m
%
% Creates the coordinates of the ASSY77_P probes of Cambridge Neurotech 
% It will design it as a linear probe (one probe after each other)
% because both KiloSort2 and Phy are designed better for linear probes.
% it will not affect the sorting, since the probes are independent.
%=======================================================================


%%=======================================================================
%% 64_P.mat
%%=======================================================================
fname = '~/git/minibrain/Matlab/Kilosort3/configFiles/64P.mat';
Nchannels = 67; % Total number of channels
connected = true(Nchannels,1); % zero if bad channel 
connected(65:67) = 0; % AUX channels
chanMap = 1:Nchannels;
chanMap0ind = chanMap - 1; % zero-index channel

% xlocation of 16 electrodes in shanks
xlocA = [0;-22.5;0;-22.5;0;-22.5;0;-22.5;0;-22.5;0;-22.5;0;-22.5;0;-22.5];
xlocB = xlocA + 250;
xlocC = xlocB + 250;
xlocD = xlocC + 250;

xlocAUX = [125;375;625];
xcoords = vertcat(xlocA, xlocA, xlocA, xlocA, xlocAUX); 

% ylocation of 16 electrodes shanks
ylocA = [0;-12.5;-25;-37.5;-50;-62.5;-75;-87.5;-100;-112.5;-125;-137.5;-150;-162.5;-175;-187.5];
ylocB = ylocA - 600;
ylocC = ylocB - 600;
ylocD = ylocC - 600;

% Auxiliary channels far away
ylocAUX = [-500;-500;-500;];
ycoords = vertcat(ylocA, ylocB, ylocC, ylocD, ylocAUX);

% not used in Kilosort2 (see https://github.com/MouseLand/Kilosort2/issues/155)
kcoords = ones(Nchannels,1);

fs = 30000;
save(fname, ...
    'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')

fprintf('Creating  %s \n', fname)
%%

% kcoords is used to forcefully restrict templates to channels in the same
% channel group. An option can be set in the master_file to allow a fraction 
% of all templates to span more channel groups, so that they can capture shared 
% noise across all channels. This option is

% ops.criterionNoiseChannels = 0.02; 

% if this number is less than 1, it will be treated as a fraction of the total number of clusters

% if this number is larger than 1, it will be treated as the "effective
% number" of channel groups at which to set the threshold. So if a template
% occupies more than this many channel groups, it will not be restricted to
% a single channel group. 

