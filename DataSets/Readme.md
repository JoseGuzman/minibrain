# Datasets

The dataset contains a total of 345 spikes in 55 samples.

## organoID.csv

Every measurement contains a unique prefix with two letters + three digits number + that follows a 3-number  + 1 alphanumeric identifier for the individual experiment (e.g. VT014_009F, meaning a DLX_Cheriff organoid). This code servers as a unique identifier (uid) in the datasets. You can see which kind of organoid correspond to every recording in the 'organoid' column.

To see a description of the organoid, check the table below.

| organoid    | prefix | Description |
|-------------|------- |------------ |
| TSCp5_30s   | TC     | -- |
| TSCp5_32s   | TC     | -- |
| DLX_Cheriff | VT     | -- |
| DLX_H9      | FH     | -- |
| DLX_bluered | FS     | -- |
| DLX_H9_H9   | FW     | -- |
| AP_ctrl     | AP     | -- |
| AP_drug     | AP     | -- |
| DS_Chrimson | DS     | -- |


## spikes.csv

Contains kinetic measurements for normalized spikes. Implementation details are [here]( https://github.com/JoseGuzman/minibrain/blob/7a5c6d4f8413b39490bfa370a13cff7c25c2a8f9/minibrain/loader.py#L30)

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | unique idenfier for the spike (e.g., VT014_009F). Use it as a pandas index) |
| half_width | ms     | width of spike at half-maximal amplitude (relates to rates of depolarization/repolarisation)                  |
| asymmetry  | --     | ratio between the second and the first maxima (relates to rate of fall of action potential repolarization)    |
| latency    | ms     | trought-to-right peak latency (relates to speed of depolariation of an action potential)                   |
| rise       | ms     | rise-time of the spike (relates to max. number of Sodium channels active during an action potential)                          |
| frequency  | Hz     |average frequency of spike firing                 |
| n_spikes   | --     |number of extrallular spikes detected in a session            |
| ISI.median | Hz     |median frequency of the inter-spike interval      |
| age        | months | after embryonic body formation                   |
| organoid   | --     | organoid type (as described in the table above)                                |


To load it:
```python
import pandas as pd
spikes = pd.read_csv('waveforms.csv', index_col = 'uid')
spikes.info()
spikes.organoid.value_counts()
```
## waveforms.csv

Contains normalized spike waveforms. 

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | unique idenfier for the spike (e.g., VT014_009F). Use it as a pandas index) |
| 0-150      | --     | voltage sample (33.3 uS) normalized to the trought of the spike. Total time is 5 ms |
| organoid   | --     | organoid type (as described in the table above)                                |

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
| uid        | --     | unique idenfier for the organoid (e.g.,AP009_002A). Use it as a pandas index) |
| age        | months | after embryonic body formation                   |
| latency    | ms     | mean time until the beginning of the stimulation |
| duration   | ms     | mean time between the first and last spike upon photo-stimulation|
| isi        | ms     | average inter-spike-interval upon the stimulation |
| prop_zeros | prop.  | the proportion of failures |
| prop_ones  | prop.  | the proportion of single spikes |
| prop_more  | prop.  | the proportion of multiple spikes |
| frequency  | Hz     | average spike frequency upon stimulation |
| organoid   | --     | organoid type (as described in organoID.csv)                                   |



## bursts.csv

Contains properties of burst.

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | unique idenfier for the organoid (e.g., X). Use it as a pandas index |
| age        | months | after embryonic body formation                   |
| EB         | date   | date of embryonic body formation (relates to organoid batch |
| duration   | sec    | duration of the burst |
| IBI        | sec    | average of inter-burst-interval in organoid |
| organoid   | --     | organoid type (as described in organoID.csv)                                   |
