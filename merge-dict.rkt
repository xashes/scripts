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
;; FIXME
;; 完全不同的行追加到末尾，导致同样编码，但更新的不同顺序的，不能覆盖旧有顺序，而是作为新的条目加在最后
;; 实际无法起到作用
;; 可以追加完之后，把重复编码的行删掉
;; TODO
;; 显示编码重复的行，看下目前的效果是什么样
(define (get-code line)
  ;; like "wubi/yyg 文"
  ;; return "wubi/yyg"
  (car (string-split line " "))
  )
(module+ test
  (check-equal? (get-code "wubi/yy 方")
                "wubi/yy")
  )
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
                #:when (string-prefix? line "wubi")
                #:unless (set-member? target-set line))
            (displayln line out)
            ))))))

;; display duplicated code in the file
;; 去重的规律并不好找啊，是不是因为前面没保持排序
;; "wubi/adw 亓 其"
;; "wubi/adw 其 亓"
;; "wubi/c 以 能 又"
;; "wubi/c 能 又 以"
(define (duplicated-code dict-file)
  (define table (make-hash))
  (call-with-input-file dict-file
    (lambda (in)
      (for ([line (in-lines in)])
        (let* ([lst (string-split line)]
               [code (car lst)])
          (hash-set! table code (add1 (hash-ref table code 0))
                     )))))
  (define duplicated-keys (for/list ([(key value) (in-hash table)]
                                     #:when (> value 1)
                                     )
                            key))
  (call-with-input-file dict-file
    (lambda (in)
      (sort (for/list ([line (in-lines in)]
                       #:when (set-member? duplicated-keys (get-code line))
                       )
              line)
            #:key get-code string<?
            ))))

(module+ main
  (merge-file dcache-file personal-file)
  ;; (take (set->list (read-file personal-file)) 5)
  ;; (duplicated-code personal-file)
  )
