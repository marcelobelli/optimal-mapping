# Optimal Mapping
## Recruitment process for Loadsmart


### About the project
* Python 3.8.0
* Used isort and black for code formatting


### How To

Using a terminal from the project root folder run the command `make deps`. This will install all the dependencies of the project.

 Then you have two options:
 
 1) Using a terminal from the project root folder run `make run`. This will execute the algorithm with the **cargo.csv** and **trucks.csv** provided by the test.
 
 2) At the project root folder open a python shell. After that execute the commands:

```
In [1]: from optimal_mapping import map_best_combinations

In [2]: cargos_csv = <PATH_TO_CARGOS_CSV>

In [3]: trucks_csv = <PATH_TO_TRUCKS_CSV>

In [4]: map_best_combinations(cargos_csv, trucks_csv)
```

In both options the output will be something like this:

```
* Viking Products Of Austin Incustin is the truck chosen to get Light bulbs from Sikeston, MO
* Ricardo Juradoacramento is the truck chosen to get Recyclables from Christiansburg, VA
* Kjellberg'S Carpet Oneuffalo is the truck chosen to get Apples from Columbus, OH
* Wisebuys Stores Incouverneur is the truck chosen to get Wood from Hebron, KY
* Paul J Krez Companyorton Grove is the truck chosen to get Cell phones from Hickory, NC
* Gary Lee Wilcoxpencer is the truck chosen to get Wood from Northfield, MN
* Fish-Bones Towingew York is the truck chosen to get Oranges from Fort Madison, IA
```

Enjoy!