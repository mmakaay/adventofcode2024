Side counting hypothesis
========================

For each plot in the garden, we can look in all four diagonal directions
and check if the plot has corners in those directions. The total number
of sides for a region is the same as the number of corners.


Possible corner configurations
==============================

The following configurations are possible for each of the four directions,
with the (A) being the inspected plot.

```
 (A) A      No corner     

  A  A
 
 (A)|B      Not a connected corner (the corner belongs to the
    +--     A on the bottom left)
  A  A

 (A) A      CORNER!
    +--
  A |B

 (A) A      Not a connected corner (the corner belongs to the
 --+        A on the top right)
  B| A

 (A)|B      Not a corner
    | 
  A |B

 (A) A      Not a corner
 -----
  B  B

 (A)|B      CORNER! The bottom right is drawn as a wildcard *, because
 ---+       any plant type will do. Even when it is an A, this is a corner.
  B  *
```


Test the theory:
================

When following the above rules for the following grid:

```
 C F F F
 C C F A
 C F F F
```
the plots look like this:

```
 c-c f---------f
 |C| |F   F   F|
 | | f---f f---f
 | c---c | | a-a
 |C   C| |F| |A|
 | c---c | | a-a
 | | f---f f---f
 |C| |F   F   F|
 c-c f---------f
```

Small letters indicate the corers that are matched using the
proposed logic. If you count these, the outcome matches the number
of edges. The theory is correct!

Let's implement this in part2.py.

