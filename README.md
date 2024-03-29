1. Description and purpose of the study

    Based on the use of genetic algorithms, this study aims to create the shortest route between 20 randomly selected locations by taking the coordinates of a specific city as input. In the project, genetic individuals representing the distances between the locations to be traveled will be created and the genetic algorithm will determine the most suitable and shortest route among these individuals. The basic steps of the genetic algorithm include crossover and mutation operations. The crossover process allows the genetic material of two different individuals to be combined, thus creating a new individual. Mutation allows individuals' genetic material to be randomly changed with a certain probability, which increases diversity and helps discover potentially better solutions. The aim of this study is to find the shortest route with genetic algorithm on the determined city coordinates and to evaluate the effectiveness of this method. The study will focus on understanding and applying genetic algorithms to optimization problems such as travel sales problems. The results obtained will show how successful genetic algorithms are in such problems and highlight the effectiveness of these algorithms in practical applications.

2. Information about the program used and the structure of the developed genetic algorithm
At the beginning of the project, the coordinates of the specified city are entered into the code on line 16 and a solution is produced for the travel salesman problem using genetic algorithms. In this process, a route is created over 20 randomly determined locations at the beginning.
The route begins and ends according to a color scale, starting from red and turning to blue.
API is used to retrieve data from Google Maps, thus providing a connection to Google Maps' database.
Moving on to the genetic algorithm part, the code snippet contains various functions.
The select_parents function selects the two best parents by evaluating the genetic material of individuals within a generation. This selection occurs based on individuals' fitness scores and plays an important role in determining the parents used in the crossover stage.
The route_total_distance function is used to calculate the total length of a route. Based on spatial data, this function evaluates the total distance on a given route.
The initial_population_create function is used to create the initial population of the genetic algorithm and returns a population of individuals containing a certain number of randomly ordered positions.
  The crossover function performs the crossover phase of the genetic algorithm. A random cutoff point is determined between the two parents and a new individual is created by combining the values before this point.
The mutation function implements the mutation phase of the genetic algorithm, increasing the diversity of the population by randomly changing two positions in individuals.
These functions come together to apply the crossover and mutation steps specific to the genetic algorithm, create the initial population and select the best parents. In this way, it is aimed to create an optimal travel route on the determined city coordinates.

3. Screenshots
![s1](https://github.com/Fadexboss/genetic_algorithm_with_best_short_route/assets/80221984/94d5d66f-d8a8-4c8d-a986-f1f52a9758c5)


![s2](https://github.com/Fadexboss/genetic_algorithm_with_best_short_route/assets/80221984/3efe1474-c36a-40ab-a1a1-3d9860c6ece1)



