FROM node:16.15.0

RUN yarn global add @vue/cli @vue/cli-service

WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . .
EXPOSE 80
CMD ["yarn", "dev"]