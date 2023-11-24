openssl genrsa -out rs256_jwt.pem 2048
openssl rsa -in rs256_jwt.pem -pubout > rs256_jwt.pub