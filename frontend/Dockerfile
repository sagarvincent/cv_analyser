FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --ignore-scripts

COPY . .

# Override .env.production so VITE_API_BASE_URL points to the nginx proxy path
ARG VITE_API_BASE_URL=/api
RUN printf "VITE_APP_MODE=production\nVITE_API_BASE_URL=%s\n" "$VITE_API_BASE_URL" > .env.production

RUN npm run build

FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
