%=========================================================================
% main_kilosortCA3.m
%
% For in vivo patch-clamp CA3 recordings together with extracellular probes
% 
% Magdalena Picher, magdalena.picher<at>ist.ac.at
% Alois Schloegl, alois.schloegl@ist.ac.at
% Jose Guzman, jose.guzman<at>guzman-lab.com
% Created: Mon 15 Mar 2021 11:29:36 AM CET
%
% this script will execute Kilosort3 by first reading a configFile called
% 'CA3Config.m' and the probe created with 'CreateCA3_Probes.m'
% 
% Sorting results will be saved in a subdirectory called 'sorting3'
%=========================================================================

addpath(genpath('~/git/Kilosort/')) % path to KiloSort3 folder
addpath('~/git/npy-matlab/npy-matlab/') % npy-matlab for converting to Phy
rootZ = './'; % the raw data binary file is in current directory
rootH = '/data/tmp/'; % path to temporary binary file ( on fast SSD)
pathToYourConfigFile = '~/git/minibrain/Matlab/Kilosort3/configFiles'; 
chanMapFile = '41_CA3probe.mat';
%chanMapFile = 'MP_WTM220_15w_1_201002.gdf.chanMap.mat'

ops.trange    = [0 inf]; % time range to sort (in sec.)
ops.NchanTOT  = 41; % total number of channels in your recording

run(fullfile(pathToYourConfigFile, 'CA3Config.m'))

ops.fproc   = fullfile(rootH, 'temp_wh.dat'); % proc file on a fast SSD
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

rez                = preprocessDataSub(ops);
rez                = datashift2(rez, 1);

[rez, st3, tF]     = extract_spikes(rez);

rez                = template_learning(rez, tF, st3);

[rez, st3, tF]     = trackAndSort(rez);

rez                = final_clustering(rez, tF, st3);

rez                = find_merges(rez, 1);

% Save results
rootZ = fullfile(rootZ, 'sorting3');
mkdir(rootZ)
rezToPhy2(rez, rootZ);

