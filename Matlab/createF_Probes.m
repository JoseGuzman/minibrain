%=========================================================================
% createF_Probes.m
%
% Created: Fri Sep 11 14:20:43 CEST 2020
%
% Creates the coordinates of the ASSY77_F probes of Cambridge Neurotech 
% It will design it as a linear probe (one probe after each other)
% because both KiloSort2 and Phy are designed better for linear probes.
% it will not affect the sorting, since the probes are independent.
%=======================================================================

%%=======================================================================
%% 64F
%% 6 shanks named A, B, C, D, E, and F. 
%% (A,F) with 10 electrodes,
%% (B,C,D,E) contains 11 electrodes.
%% three auxiliary channels 
%%=======================================================================
fname = '~/SiliconProbes/Kilosort2/configFiles/64F.mat';
Nchannels = 67; % Total number of channels
connected = true(Nchannels,1); % zero if bad channel 
connected(65:67) = 0; % AUX channels
chanMap = 1:Nchannels;
chanMap0ind = chanMap - 1; % zero-index channel

% xlocation electrodes in shanks
xloc_10 = [0 -16.5 0 -16.5 0 -16.5 0 -16.5 0 -16.5 ]; % 10 electrodes
xloc_11 = [0 -16.5 0 -16.5 0 -16.5 0 -16.5 0 -16.5 0];% 11 electrodes

xlocA = xloc_10 ;
xlocB = xloc_11 ;
xlocC = xloc_11 ;
xlocD = xloc_11 ;
xlocE = xloc_11 ;
xlocF = xloc_10 ;

xlocAUX = [-125 -375 -625]; % AUX far away
%xcoords = vertcat(xlocA, xlocB, xlocC, xlocD, xlocE, xlocF, xlocAUX); 
xcoords = horzcat(xlocA, xlocB, xlocC, xlocD, xlocE, xlocF, xlocAUX);

% ylocation of electrodes shanks
yloc_10 = [  -15 -30 -45 -60 -75 -90 -105 -120 -135 -150]; % 10 electrodes
yloc_11 = [0 -15 -30 -45 -60 -75 -90 -105 -120 -135 -150]; % 11 electrodes

ylocA = yloc_10 - 1500;
ylocB = yloc_11 - 3000;% - 1500;
ylocC = yloc_11 - 4500;% - 3000;
ylocD = yloc_11 - 6000;% - 4500;
ylocE = yloc_11 - 7500;% - 6000;
ylocF = yloc_10 - 9000;% - 7500;

ylocAUX = [500 500 500;]; % AUX far away
ycoords = horzcat(ylocA, ylocB, ylocC, ylocD, ylocE, ylocF, ylocAUX);

% not used in Kilosort2 
% (see https://github.com/MouseLand/Kilosort2/issues/155)
kcoords = ones(Nchannels,1);

fs = 30000;
save(fname, ...
'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')

fprintf('Creating  %s \n', fname)
%%=======================================================================


%%=======================================================================
%% 64F_64F.mat
%% 12 shanks named (A,B,C,D,E,F) and (G,H,I,J,K)
%% (A,F,G,K) with 10 electrodes
%% (B,C,D,E,H,I,K) with 11 electrodes
%% six auxiliary channels
%%=======================================================================
fname = '~/SiliconProbes/Kilosort2/configFiles/64F_64F.mat';
Nchannels = 134; % Total number of channels
connected = true(Nchannels,1); % zero if bad channel

connected(129:134) = 0; % AUX channels
chanMap = 1:Nchannels;
chanMap0ind = chanMap - 1; % zero-index channel

% xlocation of electrodes in shanks
xloc_10 = [0 -16.5 0 -16.5 0 -16.5 0 -16.5 0 -16.5 ]; % 10 electrodes
xloc_11 = [0 -16.5 0 -16.5 0 -16.5 0 -16.5 0 -16.5 0];% 11 electrodes

xlocA = xloc_10 ;
xlocB = xloc_11 ;
xlocC = xloc_11 ;
xlocD = xloc_11 ;
xlocE = xloc_11 ;
xlocF = xloc_10 ;

xlocG = xloc_10 ;
xlocH = xloc_11 ;
xlocI = xloc_11 ;
xlocJ = xloc_11 ;
xlocK = xloc_11 ;
xlocL = xloc_10 ;

xlocAUX = ones(1,6)*35; % AUX far away
xcoords = horzcat(xlocA, xlocB, xlocC, xlocD, xlocE, xlocF, xlocG, xlocH, xlocI, xlocJ, xlocK, xlocL, xlocAUX);

% ylocation of electrodes in shanks
yloc_10 = [  -15 -30 -45 -60 -75 -90 -105 -120 -135 -150]; % 10 electrodes
yloc_11 = [0 -15 -30 -45 -60 -75 -90 -105 -120 -135 -150]; % 11 electrodes

ylocA = yloc_10 - 1500;
ylocB = yloc_11 - 3000;% - 1500;
ylocC = yloc_11 - 4500;% - 3000;
ylocD = yloc_11 - 6000;% - 4500;
ylocE = yloc_11 - 7500;% - 6000;
ylocF = yloc_10 - 9000;% - 7500;

ylocG = yloc_10 - 11500;
ylocH = yloc_11 - 13000;% - 1500;
ylocI = yloc_11 - 14500;% - 3000;
ylocJ = yloc_11 - 16000;% - 4500;
ylocK = yloc_11 - 17500;% - 6000;
ylocL = yloc_10 - 19000;% - 7500;

ylocAUX = [4600 4650 4700 4750 4800 4850]; % AUX far away
ycoords = horzcat(ylocA, ylocB, ylocC, ylocD, ylocE, ylocF, ylocG, ylocH, ylocI, ylocJ, ylocK, ylocL, ylocAUX);

% not used in Kilosort2
% (see https://github.com/MouseLand/Kilosort2/issues/155)
kcoords = ones(Nchannels,1);

fs = 30000;
save(fname, ...
'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')

fprintf('Creating  %s \n', fname)
%%=======================================================================
