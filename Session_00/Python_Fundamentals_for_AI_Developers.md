
# 🐍 Python Fundamentals for AI Developers
*A Beginner-Friendly Python Guide Inspired by W3Schools, Tailored for AI Students*

---

## 📘 Overview

This guide is designed for beginners who want to learn Python — especially those preparing for **Generative AI & Agentic AI Programming**.  
By the end of this tutorial, you’ll be able to read, write, and run Python code confidently, handle data, and work with APIs and JSON.

---

## 🧩 Module 1 — Introduction to Python

### Topics
- What is Python and why it’s popular in AI
- Installing Python, Jupyter, or VS Code
- Writing your first Python script:  
  ```python
  print("Hello, AI World!")
  ```
- Variables, indentation, and comments

### Exercises
1. Print your name, batch, and favorite AI topic.
2. Fix syntax and indentation errors in sample snippets.

---

## 🧮 Module 2 — Data Types & Variables

### Topics
- Strings, Integers, Floats, Booleans
- Type casting with `int()`, `float()`, `str()`
- String operations, slicing, and f-strings

### Example
```python
name = "John"
batch = "Oct2025"
print(f"Welcome {name} to the {batch} Generative AI Training!")
```

### Exercises
- Create variables for student details and format a message using f-strings.
- Slice a string to extract only part of it.

---

## ⚙️ Module 3 — Operators & Expressions

### Topics
- Arithmetic, comparison, logical, and assignment operators
- Operator precedence

### Example
```python
x, y = 10, 5
print(x + y, x * y, x / y, x > y)
```

### Mini Project
Create a calculator that asks the user for two numbers and prints addition, subtraction, and multiplication results.

---

## 🧺 Module 4 — Lists, Tuples, Sets, and Dictionaries

### Topics
- Creating and iterating over collections
- Modifying list and dictionary values

### Example
```python
student = {"name": "John", "batch": "Oct2025", "course": "AI"}
for key, value in student.items():
    print(f"{key}: {value}")
```

### Exercises
- Create a list of your 3 favorite AI frameworks.
- Build a dictionary of course topics and durations.

---

## 🔁 Module 5 — Conditionals & Loops

### Topics
- Using `if`, `elif`, and `else`
- For and While loops

### Example
```python
for i in range(1, 6):
    print(f"Iteration {i}")
```

### Challenge
Build a **number guessing game** that keeps looping until the user guesses correctly.

---

## 🧮 Module 6 — Functions & Modules

### Topics
- Defining and calling functions
- Using return values
- Importing built-in modules like `math`, `datetime`, `random`

### Example
```python
def square_number(n):
    return n ** 2

print(square_number(4))
```

---

## 📂 Module 7 — Files, JSON, and APIs

### Topics
- Reading and writing files
- Working with JSON data
- Making simple API requests

### Example
```python
import json, requests

response = requests.get("https://api.quotable.io/random")
quote = response.json()
with open("quote.json", "w") as f:
    json.dump(quote, f, indent=2)
print("Saved a random quote to quote.json!")
```

---

## 📊 Module 8 — Numpy, Pandas, and Visualization

### Topics
- Intro to `numpy` arrays
- Using `pandas` DataFrames
- Simple plots with `matplotlib`

### Example
```python
import pandas as pd
import matplotlib.pyplot as plt

data = {"Session": [1, 2, 3], "Students": [10, 14, 20]}
df = pd.DataFrame(data)
df.plot(x="Session", y="Students", kind="bar", title="Attendance Trend")
plt.show()
```

---

## 🎯 Final Mini Project — Student Performance Dashboard

### Requirements
1. Input a list of student scores.
2. Compute average, grade, and rank.
3. Visualize results using a bar chart.
4. Save data to CSV and JSON.

---

## 🎓 Learning Outcomes

✅ Understand Python syntax, data types, loops, and functions  
✅ Read/write files and call APIs  
✅ Handle JSON and data using pandas  
✅ Build basic automation and data workflows for AI apps
