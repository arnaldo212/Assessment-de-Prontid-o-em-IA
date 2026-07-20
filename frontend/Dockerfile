# syntax=docker/dockerfile:1
FROM node:20-slim AS base
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .

# ---------- dev: vite dev server com hot reload ----------
FROM base AS dev
EXPOSE 5173
CMD ["npm", "run", "dev"]

# ---------- build: gera o bundle estático ----------
FROM base AS build
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

# ---------- prod: Nginx servindo o bundle ----------
FROM nginx:1.27-alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
