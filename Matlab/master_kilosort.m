%=========================================================================
% master_kilosort.m
% 
% Jose Guzman, jose.guzman<at>guzman-lab.com
% Created: Sat Dec 14 18:56:49 CET 2019
%
% this script will execute Kilosort2 by first reading a configFile called
% 'minibrainConfig.m' and reading a probe created with 
% 'createASSY77E2.mat'
%=========================================================================

addpath(genpath('~/git/Kilosort2')) % path to KiloSort2 folder
addpath('~/git/npy-matlab/npy-matlab/') % for converting to python
rootZ = './'; % the raw data binary file is in current directory
outDir = './test';
rootH = '/data/tmp'; % path to temporary binary file ( on fast SSD)
pathToYourConfigFile = '~/SiliconProbes/Kilosort2/configFiles'; % take from Github folder and put it somewhere else (together with the master_file)
chanMapFile = '128bASSY77E2.mat';


ops.trange = [0 20*60]; % time range to sort
ops.NchanTOT = 134; % total number of channels in your recording

run(fullfile(pathToYourConfigFile, 'minibrainConfig.m'))
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

% time-reordering as a function of drift
rez = clusterSingleBatches(rez);

% saving here is a good idea, because the rest can be resumed after loading rez
save(fullfile(rootZ, 'rez.mat'), 'rez', '-v7.3');

% main tracking and template matching algorithm
rez = learnAndSolve8b(rez);

% final merges
rez = find_merges(rez, 1);

% final splits by SVD
rez = splitAllClusters(rez, 1);

% final splits by amplitudes
rez = splitAllClusters(rez, 0);

% decide on cutoff
rez = set_cutoff(rez);

fprintf('found %d good units \n', sum(rez.good>0))

% write to Phy
fprintf('Saving results to Phy %s \n', outDir)
rezToPhy(rez, outDir);
%rezToPhy(rez, rootZ);

%% if you want to save the results to a Matlab file...

% discard features in final rez file (too slow to save)
%rez.cProj = [];
%rez.cProjPC = [];

%% save final results as rez2
%fprintf('Saving final results in rez2  \n')
%fname = fullfile(rootZ, 'rez2.mat');
%save(fname, 'rez', '-v7.3');
