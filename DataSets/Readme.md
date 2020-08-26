# Datasets

## spikes.csv

Contains kinetic measurements for normalized spikes. 

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | unique idenfier (e.g., use it as a pandas index) |
| half_width | ms     | width of spike at half-maximal amplitude (relates to rates of depolarization/repolarisation)                  |
| asymmetry  | --     | ratio between the second and the first maxima (relates to rate of fall of action potential repolarization)    |
| latency    | ms     | trought to right peak latency (relates to repolariation of an action potential)                   |
| rise       | ms     | rise-time of the spike (relates to max. number of Sodium channels active during an action potential)                          |
| organoid   | --     | organoid type *                                   |
| n_spikes   | --     |number of extrallular spikes detected in a session            |
| fr         | Hz     |average frequency of spike firing                 |
| ISI.median | Hz     |median frequency of the inter-spike interval      |
| age        | months | after embryonic body formation                   |


## waveforms.csv

| key        | units  | Description |
|------------|--------|------------ |
| uid        | --     | unique idenfier (e.g., use it as a pandas index) |
| 0-120      | --     | voltage sample (33.3 uS) normalized to the trought of the spike. Total time is 4 ms |

## burst.csv
