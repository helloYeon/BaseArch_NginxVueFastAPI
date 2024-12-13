# ----------------------
# Nginx Stage
# ----------------------
FROM nginx:1.23.2-alpine

WORKDIR /app/public

COPY ./docker-aws/nginx/config/nginx.conf /etc/nginx/nginx.conf
COPY ./public /app/public

# ----------------------
# Vue Build Stage
# ----------------------
FROM node:18.18.0 AS vue-build

WORKDIR /app

COPY ./frontend /app

RUN npm install

ARG APP_ENV
RUN npm run build

# ----------------------
# Final Stage
# ----------------------
FROM nginx AS final

COPY --from=vue-build /app/dist/ /app/public/

EXPOSE 80 443
