# Optimal Mapping
## Recruitment process for Loadsmart

## How To

After download the project, first install the dependencies:

```
pip install -r requirements.txt
```

Then, at the root of the project run the python shell. After that run the commands:

```
In [1]: from optimal_mapping import map_best_combinations

In [2]: cargos_csv = <PATH_TO_CARGOS_CSV>

In [3]: trucks_csv = <PATH_TO_TRUCKS_CSV>

In [4]: map_best_combinations(cargos_csv, trucks_csv)
```

The output will be something like this:

```
Viking Products Of Austin Incustin is the truck chosen to get Light bulbs from Sikeston, MO
Ricardo Juradoacramento is the truck chosen to get Recyclables from Christiansburg, VA
Kjellberg'S Carpet Oneuffalo is the truck chosen to get Apples from Columbus, OH
Wisebuys Stores Incouverneur is the truck chosen to get Wood from Hebron, KY
Paul J Krez Companyorton Grove is the truck chosen to get Cell phones from Hickory, NC
Gary Lee Wilcoxpencer is the truck chosen to get Wood from Northfield, MN
Fish-Bones Towingew York is the truck chosen to get Oranges from Fort Madison, IA
```

At files folder there is two csv with data to play with the project.

Enjoy!