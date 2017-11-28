(begin

	(define l (list 1 2 3 5 4))

	(define count (lambda (l) 
		(if (empty? l)
			0 
			(+ 1 (count (tail l)))
		)
	))

	(count l)

)


