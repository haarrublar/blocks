# Master Building Equation Documentation

This guide provides the mathematical foundations and Python implementations for automated building logic in Minecraft. All calculations treat the provided position $(X, Y, Z)$ as the **inclusive anchor block** (the first block built).

## 1. The Master Table (Inclusive Quadrant Method)

| Category | Quadrant | Start $x_1 / z_1$ | End $x_2$ | End $z_2$ | Height $y_2$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rectangular** | **North-West** | $X, Z$ | $x_1 - (W - 1)$ | $z_1 - (L - 1)$ | $Y + (H - 1)$ |
| ($W \times L \times H$) | **North-East** | $X, Z$ | $x_1 + (W - 1)$ | $z_1 - (L - 1)$ | $Y + (H - 1)$ |
| | **South-West** | $X, Z$ | $x_1 - (W - 1)$ | $z_1 + (L - 1)$ | $Y + (H - 1)$ |
| | **South-East** | $X, Z$ | $x_1 + (W - 1)$ | $z_1 + (L - 1)$ | $Y + (H - 1)$ |
| **Cylindrical** | **All** | $X, Z$ (Center) | $dx^2 + dz^2 \le (R+0.5)^2$ | | $Y + (H - 1)$ |

---

## 2. Python Implementation

### Rectangular Function
Calculates coordinates where $(x, z)$ is the first corner of the building.

```python
def get_rectangular_coords(x, y, z, w, l, h, quad):
    """
    Variables: w (width), l (length), h (height), quad (NW, NE, SW, SE)
    Functionality: Returns start (x1, y1, z1) and end (x2, y2, z2) for a fill command.
    """
    # sx: East is positive, West is negative
    # sz: South is positive, North is negative
    sx = 1 if "E" in quad else -1
    sz = 1 if "S" in quad else -1
    
    x1, z1 = x, z  # Start exactly on the anchor
    x2 = x1 + (sx * (w - 1))
    z2 = z1 + (sz * (l - 1))
    y2 = y + (h - 1)
    
    return (x1, y, z1), (x2, y2, z2)

# Example: build_rect(-595, 70, 87, 3, 3, 3, "NE") -> (-595, 70, 87), (-593, 72, 85)
```

### Cylindrical Function
Generates a circle where $(x, z)$ is the dead center.

```python
def get_cylinder_points(x, y, z, r, h):
    """
    Variables: r (radius), h (height)
    Functionality: Returns points forming a solid cylinder centered on (x, z).
    """
    points = []
    threshold = (r + 0.5)**2
    
    for dy in range(h):
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if dx**2 + dz**2 <= threshold:
                    points.append((x + dx, y + dy, z + dz))
    return points

# Example: build_cyl(0, 70, 0, 3, 5) -> Center is 0,0. Diameter is 7 blocks.
```
---

## 3. Key Logic Rules

* **Dimensional Integrity:** $W$ is always $X$-axis, $L$ is always $Z$-axis.
* **The Inclusive Rule:** We never add $+1$ or $-1$ to the starting $(X, Z)$. The point provided is the first block of the structure.
* **Stackability:** To stack a roof or second floor, use the same $x_1, z_1$ and $y_1 = \text{previous } y_2 + 1$.
* **Adjacency:** To build a structure immediately to the right of an existing NE structure, the new $x_1 = x_{2\_old} + 1$.

