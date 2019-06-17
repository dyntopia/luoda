;;; luoda-org-export.el --- exporter -*- lexical-binding: t; -*-

(require 'ox-html)

(setq org-export-time-stamp-file nil
      org-export-with-toc nil
      org-export-with-section-numbers nil
      org-html-head-include-default-style nil
      org-html-html5-fancy t
      org-html-htmlize-output-type nil
      org-html-head-include-scripts nil
      org-html-validation-link nil
      org-html-xml-declaration nil)

(defun luoda-org-export (_switch)
  (let ((filename (pop command-line-args-left))
        (user-full-name ""))
    (when filename
      (with-temp-buffer
        (insert-file-contents-literally filename)
        (org-html-export-as-html)
        (princ (format "%s" (buffer-string))))))
  (kill-emacs))

(add-to-list 'command-switch-alist '("--luoda-org-export" . luoda-org-export))
