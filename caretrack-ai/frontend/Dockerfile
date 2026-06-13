# Build stage
FROM node:18-alpine AS build

WORKDIR /app

COPY package.json ./
RUN npm install --legacy-peer-deps

COPY . .

ARG REACT_APP_API_URL=http://localhost:8000/api/v1
ENV REACT_APP_API_URL=$REACT_APP_API_URL

RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

# nginx config for React Router (SPA)
RUN echo 'server { \
  listen 80; \
  root /usr/share/nginx/html; \
  index index.html; \
  location / { try_files $uri $uri/ /index.html; } \
  location /api { proxy_pass http://backend:8000; } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s \
  CMD wget -q -O- http://localhost:80/ > /dev/null || exit 1

CMD ["nginx", "-g", "daemon off;"]
