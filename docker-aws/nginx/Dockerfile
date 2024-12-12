FROM nginx:1.23.2-alpine

WORKDIR /app/public

COPY ./docker-aws/nginx/config/nginx.conf /etc/nginx/nginx.conf
COPY ./public /app/public
