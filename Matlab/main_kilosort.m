%=========================================================================
% main_kilosort.m
%
% For recording AP018_merged
% Jose Guzman, jose.guzman<at>guzman-lab.com
% Created: Thu Nov  5 15:10:25 CET 2020
%
% this script will execute Kilosort2 by first reading a configFile called
% 'OptoConfig.m' and the probe created with 'CreateF_Probes.m'
%=========================================================================
%
addpath(genpath('~/git/Kilosort2')) % path to KiloSort2 folder
addpath('~/git/npy-matlab/npy-matlab/') % for converting to python
rootZ = './'; % the raw data binary file is in current directory
outDir = './sorting'; % output directory
rootH = '/data/tmp'; % path to temporary binary file ( on fast SSD)
pathToYourConfigFile = '~/SiliconProbes/Kilosort2/configFiles'; 

chanMapFile = '64F_7021.mat';

ops.trange = [0 inf]; % time range to sort
ops.NchanTOT = 134; % total number of channels in your recording

run(fullfile(pathToYourConfigFile, 'OptoConfig.m'))
%ops.spkTh           = -7;
%ops.fshigh = 300;  % default 150
%ops.nskip = 10;
%ops.Th = [8 4];  % default [10 4]

ops.fproc       = fullfile(rootH, 'temp_wh.dat'); % proc file on a fast SSD
ops.chanMap = fullfile(pathToYourConfigFile, chanMapFile);

%% this block runs all the steps of the algorithmO
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

% NEW STEP TO DO DATA REGISTRATION
rez = datashift2(rez, 1); % last input is for shifting data

% ORDER OF BATCHES IS NOW RANDOM, controlled by random number generator
iseed = 1;
                 
% main tracking and template matching algorithm
rez = learnAndSolve8b(rez, iseed);

% OPTIONAL: remove double-counted spikes - solves issue in which individual spikes are assigned to multiple templates.
% See issue 29: https://github.com/MouseLand/Kilosort/issues/29
%rez = remove_ks2_duplicate_spikes(rez);

% final merges
rez = find_merges(rez, 1);

% final splits by SVD
rez = splitAllClusters(rez, 1);

% decide on cutoff
rez = set_cutoff(rez);
% eliminate widely spread waveforms (likely noise)
rez.good = get_good_units(rez);

fprintf('found %d good units \n', sum(rez.good>0))

% write to Phy
%rezToPhy(rez, rootZ);
fprintf('Saving results to Phy \n')
rezToPhy(rez, outDir);

%% if you want to save the results to a Matlab file...

% discard features in final rez file (too slow to save)
rez.cProj = [];
rez.cProjPC = [];

% final time sorting of spikes, for apps that use st3 directly
[~, isort]   = sortrows(rez.st3);
rez.st3      = rez.st3(isort, :);

% Ensure all GPU arrays are transferred to CPU side before saving to .mat
rez_fields = fieldnames(rez);
for i = 1:numel(rez_fields)
    field_name = rez_fields{i};
    if(isa(rez.(field_name), 'gpuArray'))
        rez.(field_name) = gather(rez.(field_name));
    end
end

% save final results as rez2
fprintf('Saving final results in rez2  \n')
%fname = fullfile(rootZ, 'rez2.mat');
fname = fullfile(outDir, 'rez2.mat');
save(fname, 'rez', '-v7.3');
