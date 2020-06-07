Briefly on what each script does:

* `UdGraph.py`: ADT class for graph
* `WashingtonModel.py`: implementation of metropolis-hastings algorithm
* `launch.py`: this script reads the data source file and call the model, then print out the produced redistricting

Other csv/txt files are data source files.

Instructions on how to run the algorithm on Washington State: download everything inside this `redistricting` folder to the same directory, and execute the `launch.py` script with Python 3. The script will print out two columns: left column is precinct number, right column is the district that precinct belongs to. Since there are only 10 districts, the right column will be 0-9. If you set `randomWalkLength` variable large (more than 10000), then the model will be slow.