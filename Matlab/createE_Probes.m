%=========================================================================
% createLinear_Probes.m
%
% Created: Thu Nov 12 11:11:47 CET 2020
%
% Creates the coordinates of ASSY-77-E1 and E2 CambridgeNeurotech probes
% It will design it as a linear probe (one probe after each other)
% because both KiloSort and Phy are designed better for linear probes.
% it will not affect the sorting, since the probes are independent.
%=======================================================================

%%=======================================================================
%% 64E.mat
%% 4 shanks names A, B, C and D.
%% shanks contain 16 electrodes
%% three auxiliary channels
%%=======================================================================
fname2 = '~/git/minibrain/Matlab/Kilosort2/configFiles/64E.mat';
fname3 = '~/git/minibrain/Matlab/Kilosort3/configFiles/64E.mat';

Nchannels = 67; % Total number of channels
connected = true(Nchannels,1); % zero if bad channel 
connected(65:67) = 0; % AUX channels
chanMap = 1:Nchannels;
chanMap0ind = chanMap - 1; % zero-index channel

% xlocation of 16 electrodes in shanks
xloc = [0;70;5;65;10;60;15;55;20;50;25;45;30;40;35;35];

xlocAUX = ones(3,1)*35; % AUX far away
xcoords = vertcat(xloc, xloc, xloc, xloc, xlocAUX); 

% ylocation of 16 electrodes shanks
ylocA = [0;-25;-40;-65;-80;-105;-120;-145;-160;-185;-200;-225;-240;-265;-280;-305];
ylocB = ylocA - 600;
ylocC = ylocB - 600;
ylocD = ylocC - 600;

ylocAUX = [-4600;-4650;-4700]; % AUX far away
ycoords = vertcat(ylocA, ylocB, ylocC, ylocD, ylocAUX);

% not used in Kilosort2 
% (see https://github.com/MouseLand/Kilosort2/issues/155)
kcoords = ones(Nchannels,1);

fs = 30000;
save(fname2, ...
    'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')
fprintf('Creating  %s \n', fname2)

save(fname3, ...
    'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')
fprintf('Creating  %s \n', fname3)
%%=======================================================================


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
