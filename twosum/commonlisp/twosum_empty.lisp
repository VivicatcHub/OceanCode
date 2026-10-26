#!/usr/bin/env -S sbcl --script
;;;; Two Sum : trouver deux indices i < j tels que nums[i] + nums[j] = target.

(defparameter *usage* "usage: twosum <target>   (nombres lus sur stdin)")
(defparameter *limit* (expt 10 18))

(defun two-sum (nums target)
  "NUMS est un vecteur d'entiers. Renvoie (values i j) avec i < j et
(aref nums i) + (aref nums j) = TARGET, ou NIL s'il n'y a pas de solution.
S'il y a plusieurs solutions : le plus petit j, puis le plus petit i.
Doit être en O(n)."
  (declare (ignore nums target))
  ;; TODO
  (error "TODO: two-sum"))

(defun die (msg)
  (format *error-output* "error: ~a~%~a~%" msg *usage*)
  (sb-ext:exit :code 1 :abort t))

(defun parse-int (s)
  (let ((digits (if (and (plusp (length s)) (char= (char s 0) #\-))
                    (subseq s 1)
                    s)))
    (unless (and (plusp (length digits))
                 (every (lambda (c) (char<= #\0 c #\9)) digits))
      (die (format nil "invalid number '~a'" s)))
    (let ((n (parse-integer s)))
      (when (> (abs n) *limit*)
        (die (format nil "number out of range '~a'" s)))
      n)))

(defun blankp (c)
  (member c '(#\Space #\Tab #\Newline #\Return #\Page)))

(defun read-numbers (stream)
  "Lit tous les nombres séparés par des blancs sur STREAM, renvoie un vecteur."
  (let ((nums (make-array 0 :adjustable t :fill-pointer 0))
        (tok (make-string-output-stream)))
    (flet ((flush ()
             (let ((s (get-output-stream-string tok)))
               (when (plusp (length s))
                 (vector-push-extend (parse-int s) nums)))))
      (loop for c = (read-char stream nil nil)
            while c
            do (if (blankp c) (flush) (write-char c tok)))
      (flush))
    nums))

(defun main (args)
  (unless (= (length args) 1)
    (die "wrong number of arguments"))
  (let* ((target (parse-int (first args)))
         (nums (read-numbers *standard-input*)))
    (multiple-value-bind (i j) (two-sum nums target)
      (if i
          (format t "~d ~d~%" i j)
          (format t "none~%")))
    (finish-output)))

(handler-case (main (rest sb-ext:*posix-argv*))
  (sb-sys:interactive-interrupt () (sb-ext:exit :code 130 :abort t))
  (error (e) (die (princ-to-string e))))
