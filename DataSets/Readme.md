# Datasets

The dataset contains a total of 630 spikes in 105 samples.


## organoID.csv

Every measurement contains a unique experiment identifier (uid). The identifier unique prefix with two letters + three digits number + that follows a 3-number + 1 alphanumeric identifier for the individual experiment. For example, the uid VT014_009F, has a VT prefix, meaning it is an experiment in a DLX_Cheriff type of organoid. These code servers as a unique identifier of the recording in a dataset. You can see which kind of organoid corresponds to every recording in the 'organoid' column.

To see a description of the organoid, check this table.
| Organoid type    | Experiment prefix | Description |
|-------------|------- |------------ |
| TSCp5_30s   | TC     | TSC2(+/+) iPSC |
| TSCp5_32s   | TC     | TSC2(-/+) iPSC |
| DLX_Cheriff | VT     | Ventral only iPSC |
| DLX_H9      | FH     | Ventral-dorsal H9/iPSC |
| DLX_bluered | FS     | Ventral-dorsal iPSC |
| DLX_H9_H9   | FW     | -- |
| AP_ctrl     | AP     | H9 apolar |
| AP_drug     | AP     | H9 FGF8 |
| DS_Chrimson | DS     | -- |


## spikes.csv

Contains kinetic measurements for normalized spikes. Implementation details are [here]( https://github.com/JoseGuzman/minibrain/blob/7a5c6d4f8413b39490bfa370a13cff7c25c2a8f9/minibrain/loader.py#L30)

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | Unique idenfier for the spike (e.g., VT014_009F). Use it as a pandas index |
| half_width | miliseconds     | Width of spike at half-maximal amplitude (relates to rates of depolarization/repolarisation)                  |
| asymmetry  | --     | Ratio between the second and the first maxima (relates to rate of fall of action potential repolarization)    |
| latency    | miliseconds     | Trought-to-right peak latency (relates to speed of depolariation of an action potential)                   |
| rise       | miliseconds     | 10-90% rise-time of the spike  |
| repo_duration    | miliseconds     | Duration of repolarization 
| frequency  | Herz     |Average frequency of spike firing                 |
| n_spikes   | --     |Number of extrallular spikes detected in a session            |
| ISI.median | Herz     |Median frequency of the inter-spike interval      |
| age        | months | Age after embryonic body formation                   |
| organoid   | --     | Organoid type (described in [organoID.csv](https://github.com/JoseGuzman/minibrain/blob/master/DataSets/organoID.csv), see the table above)                                |


To load it:
```python
import pandas as pd
spikes = pd.read_csv('spikes.csv', index_col = 'uid')
spikes.info()
spikes.organoid.value_counts()
```
## waveforms.csv

Contains normalized spike waveforms. 

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | Unique idenfier for the spike (e.g., VT014_009F). Use it as a pandas index |
| 0-150      | --     | Voltage sample (33.3 uS) normalized to the trought of the spike. Total time is 5 ms |
| organoid   | --     | Organoid type (described in [organoID.csv](https://github.com/JoseGuzman/minibrain/blob/master/DataSets/organoID.csv), see the table above)                             |

To load it:

```python
import pandas as pd
waveforms = pd.read_csv('waveforms.csv', index_col = 'uid')
waveforms.info()
waveforms.iloc[0, :-1,].plot() # plot the first waveform (last column is organoid)

```
After it, you see which organoids types we have:
```python
waveforms.organoid.value_counts()
```

## trains.csv

Contain properties of spike trains upon optogenetic stimulation. Properies are derived from [this function](https://github.com/JoseGuzman/minibrain/blob/753458042d0a2e9ff52592f3578cdc0d32b77be9/minibrain/spikes.py#L118)

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | Unique idenfier for the organoid (e.g.,AP009_002A). Use it as a pandas index) |
| age        | months | After embryonic body formation                   |
| latency    | miliseconds     | Mean time until the beginning of the stimulation |
| duration   | miliseconds     | Mean time between the first and last spike upon photo-stimulation|
| isi        | miliseconds     | Average inter-spike-interval upon the stimulation |
| prop_zeros | proportion  | Proportion of failures |
| prop_ones  | proportion  | Proportion of single spikes |
| prop_more  | proportion  | Proportion of multiple spikes |
| frequency  | Herz     | Average spike frequency upon stimulation |
| organoid   | --     | Organoid type (described in [organoID.csv](https://github.com/JoseGuzman/minibrain/blob/master/DataSets/organoID.csv), see the table above)                                    |

To load it:
```python
import pandas as pd
trains = pd.read_csv('trains.csv', index_col = 'uid')
trains.info()
trains.organoid.value_counts()
```


## bursts.csv

Contains properties of burst.

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | Unique idenfier for the organoid (e.g., X). Use it as a pandas index |
| age        | months | Age after embryonic body formation                   |
| EB         | date   | Date of embryonic body formation (relates to organoid batch |
| duration   | seconds    | Duration of the burst |
| IBI        | seconds    | Average of inter-burst-interval in organoid |
| organoid   | --     | Organoid type (described in [organoID.csv](https://github.com/JoseGuzman/minibrain/blob/master/DataSets/organoID.csv), see the table above)                                   |

To load it:
```python
import pandas as pd
bursts = pd.read_csv('bursts.csv', index_col = 'uid')
bursts.info()
bursts.organoid.value_counts()
```
