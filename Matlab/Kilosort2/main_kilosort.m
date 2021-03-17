%=========================================================================
% main_kilosort.m
%
% For recording XXX
% Jose Guzman, jose.guzman<at>guzman-lab.com
% Created: Fri 05 Mar 2021 04:15:43 PM CET
%
% this script will execute Kilosort2.5 by first reading a configFile called
% 'OptoConfig.m' and the probe created with 'CreateE_Probes.m'
%=========================================================================

addpath(genpath('~/git/Kilosort-2.5')) % path to KiloSort2 folder
addpath('~/git/npy-matlab/npy-matlab/') % for converting to python
rootZ = './'; % the raw data binary file is in current directory
outDir = './sorting'; % output directory
rootH = '/data/tmp'; % path to temporary binary file ( on fast SSD)
pathToYourConfigFile = '~/SiliconProbes/Kilosort2/configFiles'; 

chanMapFile = '64P.mat';

ops.trange    = [0 Inf]; % time range to sort
ops.NchanTOT  = 67; % total number of channels in your recording

run(fullfile(pathToYourConfigFile, 'MinibrainConfig.m'))

ops.fproc       = fullfile(rootH, 'temp_wh.dat'); % proc file on a fast SSD
ops.chanMap = fullfile(pathToYourConfigFile, chanMapFile);

%% this block runs all the steps of the algorithm
fprintf('Looking for data inside %s \n', rootZ)

% main parameter changes from Kilosort2 to v2.5 are in OptoConfig.m
%ops.sig        = 20;  % spatial smoothness constant for registration
%ops.fshigh     = 300; % high-pass more aggresively
%ops.nblocks    = 5; % blocks for registration. 0 turns it off, 1 does rigid registration. Replaces "datashift" option. 

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

% ORDER OF BATCHES IS NOW RANDOM, controlled by random number generator
iseed = 1;
                 
% main tracking and template matching algorithm
rez = learnAndSolve8b(rez, iseed);

% OPTIONAL: remove double-counted spikes - solves issue in which individual spikes are assigned to multiple templates.
% See issue 29: https://github.com/MouseLand/Kilosort/issues/29
rez = remove_ks2_duplicate_spikes(rez);

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
%fprintf('Saving results to Phy  \n')
%rezToPhy(rez, rootZ);
fprintf('Saving results to Phy %s \n', outDir)
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
fprintf('Saving final results in rez2  \n', outDir)
fname = fullfile(outDir, 'rez2.mat');

save(fname, 'rez', '-v7.3');
