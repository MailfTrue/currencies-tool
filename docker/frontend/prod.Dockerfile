# build environment
FROM node:16.15.0-alpine as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package*.json ./
RUN npm install --silent
RUN npm install @vue/cli@4.5.19 -g
COPY . /app
RUN npm run build

# production environment
FROM nginx:1.19.8
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]