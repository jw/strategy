1. Some oo work:

A Piece should not know its location.
An Empty class should not have a name.
A Lake class should not have a name.

2. Make the board follow the chess board arrangement

 Same piece for:

     board[0, 0] => 0, 0
     board["a", 10] => 0, 0
     board["a10"] => 0, 0

     board["A", 1] => 0, 9

```
     0  1  2  3  4  5  5  7  8  9
     a  b  c  d  e  f  g  h  i  j
10 (0,0)            |         (9,0) 0
 9                  |           |   1
 8                  |           |   2
 7                  |           |   3
 6           f6 = (5,4)         |   4
 5                              |   5
 4                              |   6
 3                              |   7
 2                              |   8
 1----------------------------(9,9) 9
```
