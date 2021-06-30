%=========================================================================
% main_kilosort3.m
%
% For recording TC049_e1r2
% Jose Guzman, jose.guzman<at>guzman-lab.com
% Created: Fri 05 Mar 2021 04:15:43 PM CET
%
% this script will execute Kilosort2.5 by first reading a configFile called
% 'MinibrainConfig.m' and the probe created with 'createP_Probes.m'
%=========================================================================

addpath(genpath('~/git/Kilosort')) % path to KiloSort2 folder
addpath('~/git/npy-matlab/npy-matlab/') % for converting to python
rootZ = './'; % the raw data binary file is in current directory
outDir = './sorting3'; % output directory
rootH = '/data/tmp'; % path to temporary binary file ( on fast SSD)
pathToYourConfigFile = '~/git/minibrain/Matlab/Kilosort3/configFiles'; 

chanMapFile = '64E.mat';

ops.trange    = [0 inf]; % time range to sort
ops.NchanTOT  = 67; % total number of channels in your recording

run(fullfile(pathToYourConfigFile, 'MinibrainConfig.m'))
%ops.nskip = 10;
%ops.Th = [8 4];  % default [10 4]
%ops.NT = 10*64*1024+ ops.ntbuff;

ops.fproc       = fullfile(rootH, 'temp_wh.dat'); % proc file on a fast SSD
ops.chanMap = fullfile(pathToYourConfigFile, chanMapFile);

%% this block runs all the steps of the algorithm
fprintf('Looking for data inside %s \n', rootZ)

% is there a channel map file in this folder?
fs = dir(fullfile(rootZ, 'chan*.mat'));
if ~isempty(fs)
    ops.chanMap = fullfile(rootZ, fs(1).name);
end

% find the binary file
fs          = [dir(fullfile(rootZ, '*.bin')) dir(fullfile(rootZ, '*.dat'))];
ops.fbinary = fullfile(rootZ, fs(1).name);

% preprocess data to create temp_wh.dat
rez = preprocessDataSub(ops);
%
% NEW STEP TO DO DATA REGISTRATION
rez = datashift2(rez, 1); % last input is for shifting data


[rez, st3, tF]     = extract_spikes(rez);

rez                = template_learning(rez, tF, st3);

[rez, st3, tF]     = trackAndSort(rez);

rez                = final_clustering(rez, tF, st3);

% final merges
rez = find_merges(rez, 1);

fprintf('found %d good units \n', sum(rez.good>0))

% write to Phy
%fprintf('Saving results to Phy  \n')
%rezToPhy(rez, rootZ);
%fprintf('Saving results to Phy %s \n', outDir)
%rezToPhy(rez, outDir);

rootZ = fullfile(rootZ, 'kilosort3');
mkdir(rootZ)
rezToPhy2(rez, rootZ);
