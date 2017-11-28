# Lispy : A lisp interpreter in python

Inspired by Peter Norvig's Lispy [http://norvig.com/lispy.html](http://norvig.com/lispy.html)

## Usage

Run `main.py` to enter into the REPL.

You can also run `main.py file.lisp` to run the `file.lisp` file. It will run it in the current environment. One current limitation for files is that you have to surround your lisp instructions with (begin expr1 expr2 ...). See in examples/list.lisp.

## Features

#Supported types :

integers, floats and booleans (#f, #t keywords)

### Supported keywords :
- define
- lambda
- set!
- run  : (run test.lisp) runs the file in the current environment
- `(defun (f x) (expr))` : shortcut to `(define f (lambda (x) (expr)))`

### Other supported things :
- Closures : try `(define add (lambda (x) (lambda (y) (+ x y))))`
- comments with syntax `(* comment.. *)`


### TODO
- remove the necessary "begin" that surrounds all code in a file
- Read data stream
- simplified (define f (x) (expr)) instead of other keyword `defun`
- support string type

