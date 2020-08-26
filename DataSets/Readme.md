# Datasets

## spikes.csv

Contains kinetic measurements for normalized spikes. 

+------------------------------------------------------------------------+
| Data dictionary                                                        |
+============+===========================================================+
| key        | units  | Description                                      |
+============+===========================================================+
| uid        | --     | unique idenfier (e.g., use it as a pandas index) |
| half_width | ms     | width at half-maximal amplitude                  |
| asymmetry  | --     | ratio between the first and the second maxima    |
| latency    | ms     | trought to right peak latency                    |
| rise       | ms     | rise-time of the spike                           |
| organoid   | --     | organoid type                                    |
| n_spikes   | --     |number of spikes detected in a session            |
| fr         | Hz     |average frequency of spike firing                 |
| ISI.median | Hz     |median frequency of the inter-spike interval      |
| age        | months | after embryonic body formation                   |
+------------+-----------------------------------------------------------+

## waveforms.csv

+------------------------------------------------------------------------+
| Data dictionary                                                        |
+============+===========================================================+
| key        | units  | Description                                      |
+============+===========================================================+
| uid        | --     | unique idenfier (e.g., use it as a pandas index) |
| 0-120      | --     | 120 samples (4 ms) of voltages norm to the peak  |
+------------+-----------------------------------------------------------+

## burst.csv
