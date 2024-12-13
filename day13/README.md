Work out the strategy
=====================

**Given this machine:**

```
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400
```
I think we're solving equations here.
The two buttons basically represent two lines.
We're looking for a situation where the lines are
in a configuration like this:

```
  |
 Y|                               *
  |                              B
  |                             B
  |                            B
  |                           B
  |                       AAAA
  |                   AAAA   .
  |               AAAA       .
  |           AAAA           .
  |       AAAA               . 
  |   AAAA                   . 
0 AAAA-----------------------.------
  0                          A    X
```

**Observations:**

It doesn't matter in what order A and B are pressed. We will end up at the
same endpoint. That makes that we can work with linear equations here.

When only one of the two buttons would have to be used, this would simply
result in the other button doing zero presses when following this idea. No
optimizations required for this.

We can make this into a linear equation problem by moving the starting point
of line B to the coordinates of the price. Then we can find the intersection
point between the original line A and the transposed line B to get the
number of presses.

A special case is when the slopt of A, B and the prize are the same. In that
case, the lines are colinear and equation would not make sense.
[update: while investigating this, it turns out that the input data does not
contain this case, so no special handling is required]

**Formula time:**

Our input:
```
Pa = number of presses on A
Pb = number of presses on B
Xp = X position price
Yp = Y position price
Dxa = X movement button A
Dya = Y movement button A
Dxb = X movement button B
Dyb = Y movement button B
```

The X and Y movements for button presses can be written as:
```
Xa = Pa * Dxa
Ya = Pa * Dya
Xb = Pb * Dxb
Yb = Pb * Dyb
```

Transposing the line for button B to the price coordinates:
```
Xb' = Xp - Pb * Dxb
Yb' = Yp - Pb * Dyb
```

By doing the transposition, we can now find the required number
of button presses by looking for the intersection beween the
line for button A and the transposed line for button B:
```
Xa = Xb'
Ya = Yb'
```

Substituting what we know:
```
(a) Pa * Dxa = Xp - Pb * Dxb
(b) Pa * Dya = Yp - Pb * Dyb
```

Doing some solving on these:
```
(a) Pa * Dxa - Xp = -1 * Pb * Dxb
    -1 * (Pa * Dxa - Xp) = Pb * Dxb
    (Xp - Pa * Dxa) = Pb * Dxb
    (Xp - pa * Dxa) / Dxb = Pb

(b) Pa * Dya - Yp = -1 * Pb * Dyb
    -1 * (Pa * Dya - Yp) = Pb * Dyb
    (Yp - Pa * Dya) = Pb * Dyb
    (Yp - Pa * Dya) / Dyb = Pb
```

So we have two computations to find Pb based on Pa:
```
Pb = (Xp - Pa * Dxa) / Dxb
Pb = (Yp - Pa * Dya) / Dyb
```

Filling in a known scenario from the example data:
```
Xp = 8400
Yp = 5400
Dxa = 94
Dya = 34
Dxb = 22
Dyb = 67

Pb = (8400 - Pa * 94) / 22
Pb = (5400 - Pa * 34) / 67
```

Pa = 80, Pb = 40, according to the assignment. Check it:
```
>>> (8400 - 80*94) / 22
40.0
>>> (5400 - 80 * 34) / 67
40.0
>>>
```

Nice! That checks out. So the formulas so far were correctly derived. Let's
move on and do some more solving steps.

```
Pb = (Xp - Pa * Dxa) / Dxb
Pb = (Yp - Pa * Dya) / Dyb
```
also means that:
```
(Yp - Pa * Dya) / Dyb = (Xp - Pa * Dxa) / Dxb
(Yp - Pa * Dya) * Dxb / Dyb = Xp - Pa * Dxa
(Pa * Dya - Yp) * Dxb / Dyb = Pa * Dxa - Xp
Pa * Dya * Dxb / Dyb - Yp * Dxb / Dyb = Pa * Dxa - Xp
Pa * Dya * Dxb / Dyb - Pa * Dxa - Yp * Dxb / Dyb = -Xp
Pa * Dya * Dxb / Dyb - Pa * Dxa = Yp * Dxb / Dyb - Xp
Pa * (Dya * Dxb / Dyb - Dxa) = Yp * Dxb / Dyb - Xp
Pa = (Yp * Dxb / Dyb - Xp) / (Dya * Dxb / Dyb - Dxa) 
```

That's nice! Let's fill it in and see if it's correct;
```
Xp = 8400
Yp = 5400
Dxa = 94
Dya = 34
Dxb = 22
Dyb = 67
Pa = (Yp * Dxb / Dyb - Xp) / (Dya * Dxb / Dyb - Dxa) 

>>> (5400 * 22 / 67 - 8400) / (34 * 22 / 67 - 94)
80.0
```
Bingo :-) So now let's get the formula for Pb, based on
the now known value of Pa:

```
Pb = (Xp - Pa * Dxa) / Dxb

>>> (8400 - 80 * 94) / 22
40.0
```

Nice!

**Special cases**

- The examples from the assignment result in fractional button presses. We
  have to land exactly on the price, so fractions must be rejected.

- From my own testcases, there is also the option that it is impossible to
  reach the price. In such cases, we can end up with negative button
  presses.

- A special edge case is where the angle of the button presses for A and B
  are the same. In that case, finding the intersection between two lines is
  not possible, since the lines are the same. This case does not turn up in
  the example or assignment data though. Apparently, the machines do not
  provide this specific configuration.

## Algorithm

Compute the number of button A presses. Base on the above, this is:

```
Da = Dya * Dxb / Dyb - Dxa
Pa = (Yp * Dxb / Dyb - Xp) / Da
```

`Da == 0` is a special case. This one does not turn up in the input though.
We can handle this one defensively by asserting that `Da != 0`.

To not be bothered by floating point arithmatics, the above can be converted
into pure integer arithmatics by multiplying the above with `Dyb`:

```
Da = Dya * Dxb - Dxa * Dyb
Pa = (Yp * Dxb - Xp * Dyb) / Da
```

Using the Pa found, Pb can be computed with:

Pb = (Xp - Pa * Dxa) // Dxb

We now have Pa and Pb, but we might not be right on the prize. To know if we
won, we'll have to see if the resulting position matches the prize. For
this, the claw's position (Gx, Gy) must be computed:

Xc = Pa * Dxa + Pb * Dxb
Yc = Pa * Dya + Pb * Dyb

After which a comparison can be made to check for success:

(Xc, Yc) == (Px, Py)

If we're right on the prize, then we have to additionally check:

  - If Pa and Pb are both >= 0 (negative presses aren't possible)
  - If Pa is <= 100 (as stated by the assignment)
  - If Pb is <= 100 (as stated by the assignment)

If all criteria are met, we have our prize and can compute the number of
tokens required.

