%=========================================================================
% createCA3_Probes.m
%
% Created: Thu Nov 12 11:11:47 CET 2020
%
% Magdalena Picher, magdalena.picher<at>ist.ac.at
% Alois Schloegl, alois.schloegl<at>ist.ac.at
% Jose Guzman, jose.guzman<at>guzman-lab.com
%
% Creates the coordinates for CA3 recordings
% It will design it as a linear probe (one probe after each other)
% It contains 9 patch-clamp recordings + 32 extracellular recordings
% because both KiloSort2 and Phy are designed better for linear probes.
% it will not affect the sorting, since the probes are independent.
%=======================================================================

%%=======================================================================
%% 41_CA3probe.mat
%%=======================================================================
fname2 = './Kilosort2/configFiles/41_CA3probe.mat';
fname3 = './Kilosort3/configFiles/41_CA3probe.mat';
Nchannels = 41; % Total number of channels
connected = true(Nchannels,1); % zero if bad channel 
connected(1:9) = 0; % patch-clamp channels
chanMap = 1:Nchannels;
chanMap0ind = chanMap - 1; % zero-index channel

xcoords = zeros(Nchannels,1);
ycoords = [1:Nchannels]'*10;
% not used in Kilosort2 
% (see https://github.com/MouseLand/Kilosort2/issues/155)
kcoords = ones(Nchannels,1);

fs = 25000;
% Saving in Kilosort2 folder
save(fname2, ...
'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')
fprintf('Creating  %s \n', fname2)

% Saving in Kilosort3 folder
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
