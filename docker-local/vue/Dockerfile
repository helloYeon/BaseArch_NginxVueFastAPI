FROM node:18.18.0

WORKDIR /app

RUN npm install @vue/cli

COPY frontend /app

RUN npm install

CMD ["npm", "run", "dev"]
