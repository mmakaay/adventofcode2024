Part 1 could be resolved using brute force checking of all possible paths,
fanning out at intermediate robots when multiple paths could be found.
This (of course) hugely flunked for part 2. Therefore some more analysis
was required. Below are my insights that I used for part 2.

**Robots always return to position A**

We use the remote-controlled robot arm to bring the robots .. eh finger
over the key that we want to press. After that, we always have to press
A on the controller for that robot to move it forward and press the key.
After that, the robot arm must be brought to A and pressed, to let the
robot that it controls press the active key.
Because of this logic, we always end up a A for all robots, except the
one controlling the numeric keypad.

This greatly limits the complexity of the problem, since we don't have to
track robot state throughout the whole process.

**Caching is feasible**

Since the chunks of operations are always terminated at A, we do not have
to find optimal paths for all steps. Instead, we can memoize steps that we
have computed, so we only have to compute them once.

**All we need to report is size, not the complete key input string**

Not 100% sure if this will be useful to make the problem easier, but the
problem description asks for the number of button presses, not for the exact
key presses to use. This means that we don't have to keep track of keys, but
only of numbers.

**Not all shortest routes are created equal**

Paths that use repeated characters are better than paths that don't.
Here's an example where `<` has to be pressed on the controlled robot:

 - `v<<A` requires input `v<A<AA>>^A` for the controlling robot
 - `<v<A` requires input `v<<A>A<A>>^A` for the controlling robot

One generalized way of taking care of this could be to run generated key press
sequences through the key mapping again, to see which on yiels the lowest number
of key presses.

We can also see if applying some heuristics on the result data works. We can
score the results that we found. The rule from above can be used for scoring
based on the number of repeated characters for example.

**update**: the above rule was implemented for scoring sequences, but that did
not yet yield the correct result though. So some more investigation was done
to find rules for finding the best sequence out of a list of shortest sequences.
In the table below, cases are listed that were found to cause too long sequences
for parent controlling robots down ... no up ... the line.

| seq    | parent 1 | parent 2       | parent 3                      | conclusion           |
+--------+----------+----------------+-------------------------------+----------------------+
| `<`    | `v<<A`   | `v<A<AA>>^A`   |     ???                       | repeats good         |
|        | `<v<A`   | `v<<A>A<A>>^A` |   ???                         |                      |
|        | `<<vA`   | `v<<AA>A>^A`   | ???                           |                      |
+--------+----------+----------------+-------------------------------+----------------------+
| `v`    | `v<A`    | `v<A<A>>^A`    | `v<A<A>>^Av<<A>>^AvAA^<A>A`   | `v<` bad             |
|        | `<vA`    | `v<<A>A>^A`    | `v<A<AA>>^AvA^AvA^<A>A`       |                      |
+--------+----------+----------------+-------------------------------+----------------------+
| `>^A`  | `>^A`    | `vA^<A>A`      | `vA^A<A<vA>>^AvA^A`           |                      |
|        |          | `vA<^A>A`      | `vA^Av<<A>^A>AvA^A`           |                      |
|        | `^>A`    | `<Av>A^A`      | `v<<A>>^A<vA>A^A<A>A`         | `^>` bad             |
+--------+----------+----------------+-------------------------------+----------------------+
| `>^^A` | `^^>A`   | `<AA>vA^A`     | `v<<A>>^AAvA^A<A>A`           | `^>>` bad            |
|        | `>^^A`   | `vA^<AA>A`     | `<vA>^A<A<vA>>^AAvA^A`        |                      |
|        | `^>^A`   | `<A>vA<^A>A`   | `v<<A>>^A<vA>^Av<<A>^A>AvA^A` | repeats good         |
+--------+----------+----------------+-------------------------------+----------------------+
| `v>A`  | `v>A`    | `v<A>A^A`      | `v<A<A>>^AvA^A<A>A`           |                      |
|        | `v>A`    | `<vA>A^A`      | `v<<A>A>^AvA^A<A>A`           |                      |
|        | `>vA`    | `vA<A>^A`      | `<vA>^Av<<A>>^AvA^<A>A`       | `>v` bad             |
+--------+----------+----------------+-------------------------------+----------------------+
| `<^`   | `<^`     | `v<<A>^A`      | `v<A<AA>>^AvA^<A`             | interesting...       |
| `<^`   | `^<`     | `<Av<A`        | `v<<A>>^Av<A<A>>^A`           | different best at 2/3|
+--------+----------+----------------+-------------------------------+----------------------+
| `^>>A` | `^>>A`   | `<A>vAA^A`     | `v<<A>>^AvA<A>^AA<A>A`        | `^>>A` bad           |
|        | `>>^A`   | `vAA<^A>A`     | `<vA>^AAv<<A>^A>AvA`          |                      |
+--------+----------+----------------+-------------------------------+----------------------+

This grows into a larger and larger list of interesting facts. I dont immediately
see the underlying logic for why some of the sequences are bad and others are not.
So I'll see if I can automate this process to see what sequences are usable.
Maybe I can check a few levels up from a controlling sequence to see what what
sequences yield the shortest sequences eventually.



