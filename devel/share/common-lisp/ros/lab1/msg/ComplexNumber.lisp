; Auto-generated. Do not edit!


(cl:in-package lab1-msg)


;//! \htmlinclude ComplexNumber.msg.html

(cl:defclass <ComplexNumber> (roslisp-msg-protocol:ros-message)
  ((real
    :reader real
    :initarg :real
    :type cl:float
    :initform 0.0)
   (imaginary
    :reader imaginary
    :initarg :imaginary
    :type cl:float
    :initform 0.0))
)

(cl:defclass ComplexNumber (<ComplexNumber>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ComplexNumber>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ComplexNumber)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lab1-msg:<ComplexNumber> is deprecated: use lab1-msg:ComplexNumber instead.")))

(cl:ensure-generic-function 'real-val :lambda-list '(m))
(cl:defmethod real-val ((m <ComplexNumber>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lab1-msg:real-val is deprecated.  Use lab1-msg:real instead.")
  (real m))

(cl:ensure-generic-function 'imaginary-val :lambda-list '(m))
(cl:defmethod imaginary-val ((m <ComplexNumber>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lab1-msg:imaginary-val is deprecated.  Use lab1-msg:imaginary instead.")
  (imaginary m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ComplexNumber>) ostream)
  "Serializes a message object of type '<ComplexNumber>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'real))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'imaginary))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ComplexNumber>) istream)
  "Deserializes a message object of type '<ComplexNumber>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'real) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'imaginary) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ComplexNumber>)))
  "Returns string type for a message object of type '<ComplexNumber>"
  "lab1/ComplexNumber")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ComplexNumber)))
  "Returns string type for a message object of type 'ComplexNumber"
  "lab1/ComplexNumber")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ComplexNumber>)))
  "Returns md5sum for a message object of type '<ComplexNumber>"
  "54da470dccf15d60bd273ab751e1c0a1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ComplexNumber)))
  "Returns md5sum for a message object of type 'ComplexNumber"
  "54da470dccf15d60bd273ab751e1c0a1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ComplexNumber>)))
  "Returns full string definition for message of type '<ComplexNumber>"
  (cl:format cl:nil "float32 real~%float32 imaginary~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ComplexNumber)))
  "Returns full string definition for message of type 'ComplexNumber"
  (cl:format cl:nil "float32 real~%float32 imaginary~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ComplexNumber>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ComplexNumber>))
  "Converts a ROS message object to a list"
  (cl:list 'ComplexNumber
    (cl:cons ':real (real msg))
    (cl:cons ':imaginary (imaginary msg))
))
