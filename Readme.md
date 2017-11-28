Lispy : A lisp interpreter in python

Inspired by Peter Norvig's Lispy [http://norvig.com/lispy.html](http://norvig.com/lispy.html)

Features :

Supported types : 
integers, floats and booleans (#f, #t keywords)
Supported keywords :
- define
- lambda
- set!
- run  : (run test.lisp) runs the file in the current environment
- comments with syntax (* comment.. *)

Other supported things : 
- Closures : try `(define add (lambda (x) (lambda (y) (+ x y))))`


TODO
- 
