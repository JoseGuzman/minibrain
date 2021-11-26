%=========================================================================
% MinibrainConfig.m
% 
% Authors:
% Jose Guzman, jose.guzman<at>guzman-lab.com
% Created: Mon 15 Mar 2021 11:29:36 AM CET
%
% this is the config file for sorting spikes files with KiloSort3
% for recordings in brain organoids
% use a filed called main_kilosort3.m to run it. 
%=========================================================================

% sample rate
ops.fs = 30000;  

% frequency for high pass filtering (150)
ops.fshigh = 150;  % default 150

% minimum firing rate on a "good" channel (0 to skip)
% set to zero to see  all channels in Phy
ops.minfr_goodchannels = 0; % default 0.1

% threshold on projections 
% threshold for the optimization 10
% threshold for the extraction 4 (lower)
%ops.Th = [10 4]; if smaller pick up smaller spikes! 
%ops.Th = [10 4];  % default [10 4]
% main parameter changes from Kilosort2.5 to 3.0
ops.Th = [9 9];
 
% how important is the amplitude penalty 0 means not used, 10 is average,
% 50 is a lot. How the amplitude are biased towards the mean of a cluster
ops.lam = 20; % default is 10

% splitting a cluster at the end requires at least this much isolation 
% for each sub-cluster (max = 1)
ops.AUCsplit = 0.9; % default is 0.9

% minimum spike rate (Hz), if a cluster falls below 
% this for too long it gets removed
ops.minFR = 1/600; % (600, 10 min) default 1/50

% number of samples to average over (annealed from first to second value)
% number of spike detection counts.
% it shouldn't be necessary to adjust
% (https://github.com/MouseLand/Kilosort2/issues/156)
ops.momentum = [20 400]; % default [20 400]


% spatial constant in um for computing residual variance of spike6
% range of detectins spikes based on summed power of PCA projections
% has no effect on template shape. 
% (https://github.com/MouseLa6nd/Kilosort2/issues/156
ops.sigmaMask = 30; 

% threshold crossings for pre-clustering (in PCA projection space)
ops.ThPre = 8; % default 8

% kcoords is used to forcefully restrict templates to channels in the same
% channel group. An option can be set in the master_file to allow a fraction 
% of all templates to span more channel groups, so that they can capture shared 
% noise across all channels. This option is

%ops.criterionNoiseChannels = 0.2; 

% main parameter changes from Kilosort2 to v2.5 now in configfile
ops.sig        = 20;  % spatial smoothness constant for registration
%ops.fshigh     = 150; % high-pass more aggresively
ops.nblocks    = 1; % blocks for registration. 0 turns it off, 1 does rigid registration. Replaces "datashift" option. 

%% danger, changing these settings can lead to fatal errors
% options for determining PCs
ops.spkTh           = -6;      % spike threshold in standard deviations (-6)
ops.reorder         = 1;       % whether to reorder batches for drift correction. 
ops.nskip           = 25;  % how many batches to skip for determining spike PCs (default 25)

ops.GPU                 = 1; % has to be 1, no CPU version yet, sorry
% ops.Nfilt               = 1024; % max number of clusters
ops.nfilt_factor        = 4; % max number of clusters per good channel (even temporary ones)
ops.ntbuff              = 64;    % samples of symmetrical buffer for whitening and spike detection
%ops.NT                 = 64*1024+ ops.ntbuff; see https://github.com/MouseLand/Kilosort2/issues/204
ops.NT                  = 10*64*1024+ ops.ntbuff; % must be multiple of 32 + ntbuff.Batch duration in samples (try decreasing if out of memory). 
ops.whiteningRange      = 32; % number of channels to use for whitening each channel
ops.nSkipCov            = 25; % compute whitening matrix from every N-th batch
ops.scaleproc           = 200;   % int16 scaling of whitened data
ops.nPCs                = 3; % how many PCs to project the spikes into
ops.useRAM              = 0; % not yet available
