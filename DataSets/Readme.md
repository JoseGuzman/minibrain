# Datasets

## organoID.csv
Every measurement contains a unique prefix with two letters + three digits number + that follows a 2-alphanumeric identifier for the individual experiment (e.g. VT014_9F). This code servers as a unique identifier (uid) in the datasets. To know which kind of organoid correspond to every recording, load t the table below.

```python
import pandas as pd
organoid = pd.read_csv('OrganoID.csv', index_col = 'uid')
```
To see the description of the organoid, check the table below.

| organoid    | prefix | Description |
|-------------|------- |------------ |
| TSCp5_30s   | TC     | -- |
| TSCp5_32s   | TC     | -- |
| DLX_Cheriff | VT     | -- |
| DLX_H9      | FH     | -- |
| DLX_bluered | FS     | -- |


## spikes.csv

Contains kinetic measurements for normalized spikes. 

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | unique idenfier for the spike (e.g., use it as a pandas index) |
| half_width | ms     | width of spike at half-maximal amplitude (relates to rates of depolarization/repolarisation)                  |
| asymmetry  | --     | ratio between the second and the first maxima (relates to rate of fall of action potential repolarization)    |
| latency    | ms     | trought to right peak latency (relates to repolariation of an action potential)                   |
| rise       | ms     | rise-time of the spike (relates to max. number of Sodium channels active during an action potential)                          |
| organoid   | --     | organoid type (as described in organoID.csv)                                |
| n_spikes   | --     |number of extrallular spikes detected in a session            |
| fr         | Hz     |average frequency of spike firing                 |
| ISI.median | Hz     |median frequency of the inter-spike interval      |
| age        | months | after embryonic body formation                   |


To load it:
```python
import pandas as pd
spikes = pd.read_csv('waveforms.csv', index_col = 'uid')
spikes.info()
```
## waveforms.csv

Contains normalized spike waveforms. 

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | unique idenfier for the spike (e.g., use it as a pandas index) |
| 0-120      | --     | voltage sample (33.3 uS) normalized to the trought of the spike. Total time is 4 ms |

To load it:

```python
import pandas as pd
waveforms = pd.read_csv('waveforms.csv', index_col = 'uid')
waveforms.info()
waveforms.iloc[0, :].plot() # plot the first waveform
```
After it, you can merge the organoid dataset:
```python
organoid = pd.read_csv('OrganoID.csv', index_col = 'uid')
waveforms.merge( organoid, left_index=True, right_on = 'organoid')
```

## bursts.csv

Contains properties of burst.

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | unique idenfier for the organoid (e.g., use it as a pandas index) |
| age        | months | after embryonic body formation                   |
| EB         | date   | date of embryonic body formation (relates to organoid batch |
| Burst dur  | sec    | duration of the burst |
| IBI        | sec    | average of inter-burst-interval in organoid |
| organoid   | --     | organoid type (as described in organoID.csv)                                   |
