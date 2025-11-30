# Introduction

+++ {"part": "abstract"}
Why this jupyter notebook exists: learning atmospheric science using Python.
+++

I am a computational notebook about Fundamental of Atomospheric Sicence. Pennsylvania State University has [an awesome open course](https://www.e-education.psu.edu/meteo300/): hover over the link for more information.

% An admonition containing a note
:::{note}
The PSU course uses Math to understand atmospheric science... But this notebook uses _Python_!
:::

If you use Math to study atomospheric science, you'd see physical equation [](#eq:book). 
Instead, if you use Python, you'd see code like:

```python
pressure * volume = num_moles * GAS_CONST * temperature
```
Looks more informative, right? 
We will see more benefits later.

% Ideal gas law equation
:::{math}
:name: eq:book

PV = nRT
:::

Let's end the introduction with a beautiful picture showing the atmosphere environment we will study in this book in [](#fig:atmosphere)!

% A figure of a photograph of some atmosphere, followed by a caption
:::{figure} https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Top_of_Atmosphere.jpg/1200px-Top_of_Atmosphere.jpg
:label: fig:atmosphere

A photograph of some beautiful atmosphere from Wikipedia to look at whilst reading.
:::