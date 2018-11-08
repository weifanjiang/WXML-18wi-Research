# Usage

For Washington:
```
python3 RedistrictingModel.py --adjacency data/Washington/adjacency.csv --border data/Washington/border_precincts.csv --pop data/Washington/population.csv --district_num 10 --initial data/Washington/initial_map.csv --iter 1000 --param_func basic
```

For Iowa:
```
python3 RedistrictingModel.py --adjacency data/Iowa/adjacency.csv --border data/Iowa/border_precincts.csv --pop data/Iowa/population.csv --district_num 4 --initial data/Iowa/initial_map.csv --iter 1000 --param_func basic
```