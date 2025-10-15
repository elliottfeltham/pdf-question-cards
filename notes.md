Example Response

0
:
{type: 'theory', prompt_md: 'What is the purpose of a function in programming?', solution_md: 'Functions promote modularity and reusability, brea…er, cohesive tasks with clear inputs and outputs.'}
1
:
{type: 'coding', prompt_md: 'How do you define a function in Python?', solution_md: 'Use the `def` keyword followed by the function nam…arameters. Include a docstring for documentation.', starter_code: 'def function_name(parameters):\n """Docstring explaining the function."""\n # Function body', solution_code: `def make_sequence(n):\n    """Prints an integer seq… x <= n:\n        print(x, end=' ')\n        x += 1`}
2
:
{type: 'theory', prompt_md: 'What is the difference between call by value and call by reference?', solution_md: 'Call by value passes a copy of the variable (chang…able (changes inside the function are permanent).'}
3
:
{type: 'coding', prompt_md: 'How do you return multiple values from a function in Python?', solution_md: 'Use a tuple or return multiple values separated by… the function, unpack the results into variables.', starter_code: 'def my_func():\n return a, b, c\n\n# Unpack the results', solution_code: 'def my_func():\n return 1, 2, 3\n\nx, y, z = my_func()'}
4
:
{type: 'theory', prompt_md: 'What are keyword arguments in Python functions?', solution_md: 'Keyword arguments allow specifying function argume…ult values. Positional arguments must come first.'}
5
:
{type: 'coding', prompt_md: 'How do you handle arbitrary arguments in a Python function?', solution_md: 'Use `*args` for arbitrary positional arguments and `**kwargs` for arbitrary keyword arguments.', starter_code: 'def my_func(*args, \*\*kwargs):\n # Function body', solution_code: 'def my_average(*args):\n sum = 0\n for num in …gs:\n sum += num\n return sum / len(args)'}
6
:
{type: 'theory', prompt_md: 'What is the purpose of a docstring in Python?', solution_md: 'A docstring provides documentation for a function,…d return values. It is enclosed in triple quotes.'}
7
:
{type: 'coding', prompt_md: 'How do you use list comprehensions in Python?', solution_md: 'List comprehensions provide a concise way to create lists using loops and optionally conditionals.', starter_code: 'month_indices = [month for month in range(12)]', solution_code: 'alternate_months = [month for month in range(12) if month % 2 == 0]'}
8
:
{type: 'theory', prompt_md: 'What is the difference between a function and a method in Python?', solution_md: 'A method is a function that belongs to a class. Fu…alone, while methods are associated with objects.'}
9
:
{type: 'coding', prompt_md: 'How do you emulate a do-while loop in Python?', solution_md: 'Use a `while True` loop with a `break` statement to terminate the loop when a condition is met.', starter_code: 'while True:\n # Loop body\n if condition:\n break', solution_code: 'table = 8\nx = 1\nwhile True:\n answer = x \* table…, answer)\n x += 1\n if x > 12:\n break'}
