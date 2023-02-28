#lang racket/gui
(require mrlib/path-dialog)
(require racket/file)

(define default-dir (build-path (expand-user-path "~/Pictures") "models"))
(define filename #f)

;; 创建界面控件
(define frame (new frame% [label "保存图片和注释"]))
(define select-file-button (new button% [parent frame] [label "选择图片"]))
(define comment-entry (new text-field% [parent frame] [label "注释"] [min-width 200]))
(define save-button (new button% [parent frame] [label "保存"]))
(define browse-dir-dialog (new path-dialog% [parent frame] [message "请选择保存路径"] [must-exist? #f]))

;; 设置字体
(define font (make-object font% "LXGW WenKai" 12))
(send select-file-button set-font font)
(send comment-entry set-font font)
(send save-button set-font font)

;; 弹出文件选择对话框
(define (select-file)
  (define dialog (new path-dialog% [parent frame] [message "请选择图片文件"] [path default-dir]))
  (define response (send dialog show #t))
  (when response
    (send select-file-button set-label (string-append "已选择：" (path->string response)))
    (set! filename response)))

;; 弹出文件夹选择对话框
(define (select-directory)
  (define response (send browse-dir-dialog show))
  (when response
    (let* ((folder-name (path->string (car response)))
           (folder-path (build-path folder-name (file-name-from-path (path->string filename)))))
      (make-directory folder-path)
      (with-output-to-file (build-path folder-path "comment.txt") (lambda () (display (send comment-entry get-value))))
      (copy-file filename (build-path folder-path (path->string filename)) #t)
      (send comment-entry set-value "")
      (message-box "提示" "保存成功！"))))

;; 检查文件和注释是否都存在
(define (save)
  (cond ((not filename) (message-box "错误" "请选择图片并添加注释"))
        ((string=? "" (send comment-entry get-value)) (message-box "错误" "请选择图片并添加注释"))
        (else (select-directory))))

;; 绑定按钮事件
(send select-file-button bind (λ (button event) (select-file)))
(send save-button bind (λ (button event) (save)))

;; 启动应用程序
(send frame show #t)
