
(cl:in-package :asdf)

(defsystem "lab1-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ComplexNumber" :depends-on ("_package_ComplexNumber"))
    (:file "_package_ComplexNumber" :depends-on ("_package"))
  ))