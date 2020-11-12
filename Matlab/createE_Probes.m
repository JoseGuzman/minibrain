%=========================================================================
% createE_Probes.m
%
% Created: Thu Nov 12 11:11:47 CET 2020
%
% Creates the coordinates of ASSY-77-E1 and E2 CambridgeNeurotech probes
% It will design it as a linear probe (one probe after each other)
% because both KiloSort2 and Phy are designed better for linear probes.
% it will not affect the sorting, since the probes are independent.
%=======================================================================

%%=======================================================================
%% 64E.mat
%% 4 shanks names A, B, C and D.
%% shanks contain 16 electrodes
%% THREE auxiliary channels
%%=======================================================================
fname = '~/SiliconProbes/Kilosort2/configFiles/Eprobes/64E.mat';
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

ylocAUX = [-4600;-4650;-4700;]; % AUX far away
ycoords = vertcat(ylocA, ylocB, ylocC, ylocD, ylocAUX);

% not used in Kilosort2 
% (see https://github.com/MouseLand/Kilosort2/issues/155)
kcoords = ones(Nchannels,1);

fs = 30000;
save(fname, ...
'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')

fprintf('Creating  %s \n', fname)
%%=======================================================================

%%=======================================================================
%% 64E_64E.mat
%% 8 shanks named (A,B,C,D) and (E,F,G,H)
%% all with 16 electrodes
%% SIX auxiliary channels
%%=======================================================================
fname = '~/SiliconProbes/Kilosort2/configFiles/Eprobes/64E_64E.mat';
Nchannels = 134; % Total number of channels
connected = true(Nchannels,1); % zero if bad channel 
connected(129:134) = 0; % AUX channels
chanMap = 1:Nchannels;
chanMap0ind = chanMap - 1; % zero-index channel

% xlocation of 16 electrodes in shanks
xloc = [0;70;5;65;10;60;15;55;20;50;25;45;30;40;35;35];

xlocAUX = ones(6,1)*35; % AUX far away
xcoords = vertcat(xloc, xloc, xloc, xloc, xloc, xloc, xloc, xloc, xlocAUX);

% ylocation of 16 electrodes shanks
ylocA = [0;-25;-40;-65;-80;-105;-120;-145;-160;-185;-200;-225;-240;-265;-280;-305];
ylocB = ylocA - 600;
ylocC = ylocB - 600;
ylocD = ylocC - 600;

ylocE = ylocD - 600;
ylocF = ylocE - 600;
ylocG = ylocF - 600;
ylocH = ylocG - 600;

% Auxiliary channels far away
ylocAUX = [-4600;-4650;-4700;-4750;-4800;-4850];
ycoords = vertcat(ylocA, ylocB, ylocC, ylocD, ylocE, ylocF, ylocG, ylocH, ylocAUX);

% not used in Kilosort2 
%(see https://github.com/MouseLand/Kilosort2/issues/155)
kcoords = ones(Nchannels,1);

fs = 30000;
save(fname, ...
'chanMap','connected','xcoords','ycoords','kcoords','chanMap0ind','fs')

fprintf('Creating  %s \n', fname)
%%=======================================================================
