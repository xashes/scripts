#! /usr/bin/env racket
#lang racket

(module+ test
  (require rackunit))

(define dict-directory (build-path (find-system-path 'home-dir) ".spacemacs.d" "dict"))
(define dcache-file (build-path dict-directory "dcache-dict.pyim"))
(define personal-file (build-path dict-directory "personal-dict.pyim"))
(define test-file (build-path dict-directory "test.pyim"))
;; 读取目标文件,把各行保存入集合
;; 集合中只保存 wubi/\b
;; 读取 dcache 文件，逐行检查，对于不在集合中的编码，则追加到目标文件末尾
;; To fix
;; 完成不同的行追加到末尾，导致同样编码，但更新的不同顺序的，不能覆盖旧有顺序，而是作为新的条目加在最后
;; 实际无法起到作用
(define (read-file fp)
  (when (not (file-exists? fp))
      (call-with-output-file fp
        (lambda (out)
          (displayln ";;; -*- coding: utf-8-unix -*-"
                     out))))
  (call-with-input-file fp
    (lambda (in)
      (for/set ([line (in-lines in)])
        line
        )))
  )

(define (merge-file src target)
  (define target-set (read-file target))
  (call-with-output-file target
    #:exists 'append
    (lambda (out)
      (call-with-input-file src
        (lambda (in)
          (for ([line (in-lines in)]
                #:unless (set-member? target-set line)
                #:when (string-prefix? line "wubi"))
            (displayln line out)
            ))))))
(module+ main
  (merge-file dcache-file personal-file)
  )
