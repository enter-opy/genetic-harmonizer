# Genetic harmonizer

Chord generation uing genetic algorithms

![GIF](jOSE86.gif)

## Instructions

**Install dependencies:**

```bash
pip install -r requirements.txt
```

>**Adjust weights in `main.py` file (line 99) to tweak the fitness function**

```python
weights = {
    "chord_melody_congruence": 0.5,
    "chord_variety": 0.6,
    "harmonic_flow": 0.3,
    "functional_harmony": 0.6,
    "tension": 0.8,
    "parallel_fifths": 0.4,
}
```

**Run the program:**

```bash
python main.py
```
