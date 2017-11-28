### Lispy : A lisp interpreter in python

Inspired by Peter Norvig's Lispy [http://norvig.com/lispy.html](http://norvig.com/lispy.html)

## Features

#Supported types :

integers, floats and booleans (#f, #t keywords)

# Supported keywords :
- define
- lambda
- set!
- run  : (run test.lisp) runs the file in the current environment
- (defun (f x) (expr)) : shortcut to (define f (lambda (x) (expr)))

# Other supported things :
- Closures : try `(define add (lambda (x) (lambda (y) (+ x y))))`
- comments with syntax (* comment.. *)


# TODO
- remove the necessary "begin" that surrounds all code in a file
- Read data stream
- define function keyword (defun), or simplified (define f x (expr))
- support string type

