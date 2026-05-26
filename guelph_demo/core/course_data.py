# Course data: concepts, quiz questions, materials, and demo responses.

# Knowledge graph nodes

CONCEPTS = [
    "Variables",
    "Data Types",
    "Conditionals",
    "Loops",
    "Functions",
    "Lists",
    "Dictionaries",
    "OOP",
    "Recursion",
    "Algorithms",
]

# prerequisite → dependent
PREREQUISITE_EDGES = [
    ("Variables", "Data Types"),
    ("Data Types", "Conditionals"),
    ("Conditionals", "Loops"),
    ("Loops", "Functions"),
    ("Variables", "Lists"),
    ("Lists", "Dictionaries"),
    ("Functions", "OOP"),
    ("Loops", "OOP"),
    ("Dictionaries", "OOP"),
    ("Functions", "Recursion"),
    ("Recursion", "Algorithms"),
    ("OOP", "Algorithms"),
]

CONCEPT_DESCRIPTIONS = {
    "Variables":    "Storing and naming data values",
    "Data Types":   "int, float, str, bool",
    "Conditionals": "if / elif / else branching",
    "Loops":        "for and while iteration",
    "Functions":    "Defining reusable code blocks",
    "Lists":        "Ordered mutable sequences",
    "Dictionaries": "Key-value data structures",
    "OOP":          "Classes, objects, inheritance",
    "Recursion":    "Functions that call themselves",
    "Algorithms":   "Sorting, searching, complexity",
}

LEARNING_GOALS = [
    "OOP",
    "Recursion",
    "Algorithms",
    "Dictionaries",
    "Functions",
]

# BKT parameters

BKT_DEFAULTS = {
    concept: {"L0": 0.1, "T": 0.2, "G": 0.25, "S": 0.1}
    for concept in CONCEPTS
}

# Quiz questions

QUIZ_QUESTIONS = [
    {
        "concept": "Variables",
        "question": "What is the value of `x` after: `x = 5; x = x + 3`?",
        "options": ["5", "3", "8", "15"],
        "answer": "8",
    },
    {
        "concept": "Conditionals",
        "question": "Which keyword introduces an alternative condition in Python?",
        "options": ["else if", "elsif", "elif", "otherwise"],
        "answer": "elif",
    },
    {
        "concept": "Loops",
        "question": "How many times does `for i in range(3)` execute its body?",
        "options": ["2", "3", "4", "0"],
        "answer": "3",
    },
    {
        "concept": "Functions",
        "question": "Which keyword is used to send a value back from a function?",
        "options": ["send", "output", "return", "yield"],
        "answer": "return",
    },
    {
        "concept": "Lists",
        "question": "What does `my_list[-1]` return?",
        "options": ["An error", "The first element", "The last element", "-1"],
        "answer": "The last element",
    },
    {
        "concept": "Dictionaries",
        "question": "How do you access the value for key `'name'` in `d = {'name': 'Alice'}`?",
        "options": ["d.name", "d['name']", "d->name", "d.get.name"],
        "answer": "d['name']",
    },
    {
        "concept": "OOP",
        "question": "What method is automatically called when an object is created?",
        "options": ["__start__", "__new__", "__init__", "__create__"],
        "answer": "__init__",
    },
    {
        "concept": "Recursion",
        "question": "Every recursive function must have a _____ to stop infinite recursion.",
        "options": ["loop", "base case", "return type", "class"],
        "answer": "base case",
    },
]

# Course material excerpts

COURSE_MATERIALS = {
    "Variables & Data Types": """
## Chapter 1: Variables and Data Types

A **variable** is a named storage location in memory. In Python you create a
variable by assigning a value to a name:

```python
age = 21
name = "Alice"
gpa  = 3.85
is_enrolled = True
```

Python is *dynamically typed*, meaning the interpreter infers the type from
the value. Core types include:

| Type    | Example         |
|---------|-----------------|
| `int`   | `42`            |
| `float` | `3.14`          |
| `str`   | `"hello"`       |
| `bool`  | `True`, `False` |

Use `type()` to inspect a variable: `type(age)` returns `<class 'int'>`.

> **Key concept**: Variables hold *references* to objects, not the objects
> themselves. Reassigning a variable changes which object it points to.
""",

    "Functions": """
## Chapter 3: Functions

A **function** is a named, reusable block of code that performs a specific task.

```python
def greet(name):
    \"\"\"Return a personalised greeting.\"\"\"
    return f"Hello, {name}!"

message = greet("Alice")
print(message)   # Hello, Alice!
```

### Parameters vs Arguments
- **Parameter**: the variable listed in the function definition (`name` above).
- **Argument**: the actual value passed when calling the function (`"Alice"`).

### Default Parameters
```python
def power(base, exponent=2):
    return base ** exponent

power(3)      # 9  — exponent defaults to 2
power(3, 3)   # 27
```

> **Key concept**: Functions are *first-class objects* in Python — they can be
> stored in variables, passed as arguments, and returned from other functions.
""",

    "OOP": """
## Chapter 6: Object-Oriented Programming

OOP organises code around **objects** — bundles of data (*attributes*) and
behaviour (*methods*).

```python
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa  = gpa

    def is_honours(self):
        return self.gpa >= 3.5

    def __repr__(self):
        return f"Student({self.name}, GPA={self.gpa})"

alice = Student("Alice", 3.8)
print(alice.is_honours())   # True
```

### The Four Pillars
| Pillar          | Meaning |
|-----------------|---------|
| Encapsulation   | Bundle data + methods; hide internals |
| Abstraction     | Expose only necessary interface |
| Inheritance     | Child class reuses parent behaviour |
| Polymorphism    | Same interface, different implementations |

### Inheritance
```python
class GradStudent(Student):
    def __init__(self, name, gpa, thesis):
        super().__init__(name, gpa)
        self.thesis = thesis
```

> **Key concept**: `self` refers to the *current instance*. Every instance
> method receives it as its first parameter automatically.
""",
}

COURSE_MODULE_NAMES = list(COURSE_MATERIALS.keys())

# Demo mode responses (used when no API key is set)

DEMO_TUTOR_RESPONSES = {
    "beginner": (
        "Great question! Let's break this down step by step.\n\n"
        "**Hint first**: Think about what value is stored in each variable "
        "before the operation runs.\n\n"
        "In Python, the right-hand side of `=` is always evaluated first, "
        "then the result is stored in the variable on the left. So if you "
        "see `x = x + 1`, Python first reads the current value of `x`, adds "
        "1 to it, and then writes the new value back into `x`.\n\n"
        "Try tracing through your code line-by-line on paper — it's one of "
        "the most effective debugging techniques!"
    ),
    "intermediate": (
        "Good question. The core issue here is **variable scope**.\n\n"
        "In Python, a variable defined inside a function is *local* to that "
        "function unless you explicitly declare it `global`. Your code is "
        "likely creating a new local variable rather than modifying the one "
        "in the outer scope.\n\n"
        "**Fix**: Either pass the value as a parameter and `return` the "
        "result, or use `global x` (though returning is the cleaner pattern)."
    ),
    "advanced": (
        "The behaviour you're seeing is a result of Python's **late binding** "
        "in closures. Lambda expressions (and nested functions) capture "
        "variables by *reference*, not by value. By the time the lambda is "
        "called, the loop variable has already reached its final value.\n\n"
        "**Fix**: Use a default-argument hack to capture the current value:\n"
        "```python\n"
        "funcs = [lambda x, i=i: x + i for i in range(5)]\n"
        "```\n"
        "This forces `i` to be evaluated *at definition time*."
    ),
}

DEMO_COMPANION_RESPONSE = (
    "Based on the course material provided:\n\n"
    "The concept you're asking about is covered in the excerpt above. "
    "In Python, the key idea is that everything is an *object*, and "
    "variables are simply *names* that reference those objects. "
    "When you assign `a = b`, both `a` and `b` point to the same object "
    "in memory — they do not create a copy.\n\n"
    "**From the textbook (Section above)**: \"Variables hold references to "
    "objects, not the objects themselves.\"\n\n"
    "Try running `id(a) == id(b)` in the Python REPL after assignment to "
    "verify this yourself."
)

# Grounding refusal example

DEMO_COMPANION_REFUSAL = (
    "That topic is **not covered** in the selected course material.\n\n"
    "I can only answer questions based on the excerpt shown on the left. "
    "This is the key feature of this tool — it stays grounded in your actual "
    "course content and will not invent answers from outside it.\n\n"
    "Try asking something from the material, like: "
    "*\"What are the four pillars of OOP?\"* or *\"How do default parameters work?\"*"
)

# Same question answered at two different skill levels

DEMO_COMPARISON_QUESTION = "How does a for loop work in Python?"

DEMO_COMPARISON_RESPONSES = {
    "beginner": (
        "**Think of it like a checklist.**\n\n"
        "A `for` loop goes through a list of items one by one and does "
        "something with each item:\n\n"
        "```python\n"
        "fruits = [\"apple\", \"banana\", \"cherry\"]\n"
        "for fruit in fruits:\n"
        "    print(fruit)\n"
        "```\n\n"
        "This prints:\n"
        "```\napple\nbanana\ncherry\n```\n\n"
        "The loop stops automatically when it runs out of items. "
        "You don't need to tell it when to stop — Python handles that for you."
    ),
    "advanced": (
        "A `for` loop is syntactic sugar over Python's **iterator protocol**.\n\n"
        "Under the hood, `for x in obj` calls `iter(obj)` to get an iterator, "
        "then repeatedly calls `next()` on it until `StopIteration` is raised:\n\n"
        "```python\n"
        "_it = iter(fruits)\n"
        "while True:\n"
        "    try:\n"
        "        fruit = next(_it)\n"
        "        print(fruit)\n"
        "    except StopIteration:\n"
        "        break\n"
        "```\n\n"
        "Any object implementing `__iter__` + `__next__` works — lists, "
        "generators, file handles, custom classes. This is why `for` works "
        "over lazy infinite sequences without materialising them in memory."
    ),
}

# Learning resources per concept

CONCEPT_RESOURCES = {
    "Variables": ("Python Docs — Variables", "https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator"),
    "Data Types": ("Python Docs — Built-in Types", "https://docs.python.org/3/library/stdtypes.html"),
    "Conditionals": ("Python Docs — Control Flow", "https://docs.python.org/3/tutorial/controlflow.html"),
    "Loops": ("Python Docs — for Statements", "https://docs.python.org/3/tutorial/controlflow.html#for-statements"),
    "Functions": ("Python Docs — Defining Functions", "https://docs.python.org/3/tutorial/controlflow.html#defining-functions"),
    "Lists": ("Python Docs — Lists", "https://docs.python.org/3/tutorial/introduction.html#lists"),
    "Dictionaries": ("Python Docs — Dictionaries", "https://docs.python.org/3/tutorial/datastructures.html#dictionaries"),
    "OOP": ("Python Docs — Classes", "https://docs.python.org/3/tutorial/classes.html"),
    "Recursion": ("Real Python — Recursion", "https://realpython.com/python-recursion/"),
    "Algorithms": ("Real Python — Sorting Algorithms", "https://realpython.com/sorting-algorithms-python/"),
}

# Preset mastery snapshot for quick demo

QUICK_DEMO_MASTERY = {
    "Variables": 0.90,
    "Data Types": 0.85,
    "Conditionals": 0.80,
    "Loops": 0.78,
    "Lists": 0.75,
    "Functions": 0.50,
    "Dictionaries": 0.35,
    "OOP": 0.10,
    "Recursion": 0.10,
    "Algorithms": 0.10,
}
