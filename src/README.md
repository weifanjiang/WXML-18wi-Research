# Example Usage

For Washington:
```
python3 RedistrictingModel.py --adjacency data/Washington/adjacency.csv --border data/Washington/border_precincts.csv --pop data/Washington/population.csv --district_num 10 --initial data/Washington/initial_map.csv --iter 1000 --param_func basic
```

For Iowa:
```
python3 RedistrictingModel.py --adjacency data/Iowa/adjacency.csv --border data/Iowa/border_precincts.csv --pop data/Iowa/population.csv --district_num 4 --initial data/Iowa/initial_map.csv --iter 1000 --param_func basic
```

# How to rapidly visualize

## Step 1: Pick or generate a seed map

Generate your own map [here](https://gis.pengra.io/new/). Make sure you select "Drop the non-precincts after creating an adjacency graph and bridge the gaps." Name it something you'll remember. DO NOT SUBMIT MORE THAN ONCE. The page will seem like nothing happened. Go to the home page (click wxml in the top right hand corner) and locate your map there. You can see it build your map via the progress bar. 

## Step 2: Run scripts made by Weifan and answer the questions

The script will ask for an id of what you want to run. For instance,

```
Please select a map by ID: (type the number in the brackets)
[0] Title: Test Map 1, Districts: 10
[1] Title: Test Map 2, Districts: 49
[2] Title: Test Map 3, Districts: 7
Choice:
```

You are to type the number in the brackets. The title is the same as the one you named it on the site.
Please don't use the existing ones, it'll break the server.

## Step 3: Run.

Let it do it's thing. It'll download a ton of files and then it'll start running. Visualizations are available from clicking on the detail view of the page.
