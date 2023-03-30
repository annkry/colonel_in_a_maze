# colonel_in_a_maze
I will consider a colonel who moves in a labyrinth (the labyrinth consists of square fields, forming a rectangle). There are the following types of fields:

Walls, marked with '#', which cannot be traversed,
Target points (marked 'G'), which must be reached to detonate a charge above the enemy's underground warehouses,
Starting points (marked 'S'), where the colonel can be located in the first turn,
Starting-target points (marked 'B'),
Other points, marked with a space.

The colonel can move in 4 directions (UDLR). Moving towards a wall does not change the state. The colonel is dropped at night and does not know exactly where the drop occurred (in which starting point), but he knows the map of the labyrinth. It will determine a sequence of moves that will definitely lead to a final state (i.e., our soldier executes his plan, which is a sequence of moves after which he can detonate the bomb, because regardless of where he was at the beginning of the journey, he will be in one of the target points at the end). I shall call such a plan a winning plan.
The program will solve the colonel's problem, i.e., for each test case, prints out the winning plan. The solution will have two phases implemented:
1) Performing random/greedy moves reducing uncertainty,
2) Performing BFS search.

Input file: zad_input.txt
Output file: zad_output.txt

To run all 11 tests: python validator.py zad4 python main.py
