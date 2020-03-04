%=========================================================================
% createASSY77E2MapFile.m
%
% Creates the coordinates of the ASSY-77-E2 probe of Cambridge Neurotech 
% It will design it as a linear probe (one probe after each other)
% because both KiloSort2 and Phy are designed better for linear probes.
% it will not affect the sorting, since the probes are independent.
%=======================================================================

%% 1) All 128 channels of a 128 sites recording.
fname = '~/SiliconProbes/Kilosort2/configFiles/128ASSY77E2.mat';
Nchannels = 134; % Total number of channels
connected = true(Nchannels,1); % zero if bad channel 
connected(33) = 0;
connected(129:134) = 0; % AUX channels
chanMap = 1:Nchannels;
chanMap0ind = chanMap - 1; % zero-index channel

% xlocation of the 16 electrodes in A,B,C,D,E,F and G shanks
xloc = [0;70;5;65;10;60;15;55;20;50;25;45;30;40;35;35];

xlocAUX = ones(6,1)*35;
xcoords = vertcat(xloc, xloc, xloc, xloc, xloc, xloc, xloc, xloc, xlocAUX); 

% ylocation of the electrodes in A,B,C,D,E,F and G shanks
ylocA = [0;-25;-40;-65;-80;-105;-120;-145;-160;-185;-200;-225;-240;-265;-280;-305];
ylocB = ylocA - 600;
ylocC = ylocB - 600;
ylocD = ylocC - 600;

ylocE = ylocD - 600;
ylocF = ylocE - 600;
ylocG = ylocF - 600;
ylocH = ylocG - 600;

ylocAUX = [-4600;-4650;-4700;-4750;-4800;-4850];
ycoords = vertcat(ylocA, ylocB, ylocC, ylocD, ylocE, ylocF, ylocG, ylocH, ylocAUX);

% not used in Kilosort2 (see https://github.com/MouseLand/Kilosort2/issues/155)
kcoords = ones(Nchannels,1);

fs = 30000;
save(fname, ...
'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')

fprintf('Creating  %s \n', fname)

%% 2) the first 64 channels of a 128 sites recording
fname = '~/SiliconProbes/Kilosort2/configFiles/128aASSY77E2.mat';
connected = true(Nchannels,1); % zero if channel if bad channel

connected(33) = 0;
connected(65:128) = 0; % blank Shanks E, F, G and H (128a.mat)
connected(129:134) = 0; % AUX channels
chanMap = 1:Nchannels;
chanMap0ind = chanMap - 1; % zero-index channel

save(fname, ...
'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')

fprintf('Creating  %s \n', fname)

%% 3) the last 64 channels of a 128 sites recording
fname = '~/SiliconProbes/Kilosort2/configFiles/128bASSY77E2.mat';
connected = true(Nchannels,1); % zero if channel if bad channel

connected(33) = 0;
connected(1:64) = 0; % blank Shanks A, B, C, and D (128b.mat)
connected(129:134) = 0; % AUX channels
chanMap = 1:Nchannels;
chanMap0ind = chanMap - 1; % zero-index channel

save(fname, ...
'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')

fprintf('Creating  %s \n', fname)

%% 4) 64 sites recording
fname = '~/SiliconProbes/Kilosort2/configFiles/64ASSY77E2.mat';
Nchannels = 67; % Total number of channels
connected = true(Nchannels,1); % zero if bad channel 
%%connected(33) = 0;
chanMap = 1:Nchannels;
chanMap0ind = chanMap - 1; % zero-index channel

% xlocation of the 16 electrodes in A,B,C,D, shanks
xloc = [0;70;5;65;10;60;15;55;20;50;25;45;30;40;35;35];

xlocAUX = ones(3,1)*35;
xcoords = vertcat(xloc, xloc, xloc, xloc, xlocAUX); 

% ylocation of the electrodes in A,B,C,D, and G shanks
ylocA = [0;-25;-40;-65;-80;-105;-120;-145;-160;-185;-200;-225;-240;-265;-280;-305];
ylocB = ylocA - 600;
ylocC = ylocB - 600;
ylocD = ylocC - 600;

ylocAUX = [-4600;-4650;-4700];
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

