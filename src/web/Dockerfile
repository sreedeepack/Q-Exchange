FROM node:13.12.0-alpine as build

# Set the working directory.
WORKDIR /usr/src/web
ENV PATH /usr/src/web/node_modules/.bin:$PATH
# Copy the file from your host to your current location.
COPY package.json ./
COPY package-lock.json ./

RUN npm install

COPY . ./
RUN npm run build

# production environment
FROM nginx:stable-alpine
COPY --from=build /usr/src/web/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

#docker run --rm -it -p 8000:80 web
