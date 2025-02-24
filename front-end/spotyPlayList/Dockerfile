# 1. Usa una imagen de Node.js para construir la aplicación
FROM node:18 AS build

# 2. Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copia los archivos del front-end al contenedor
COPY package.json package-lock.json ./

# 4. Instala las dependencias
RUN npm install

# 5. Copia el resto del código
COPY . .

# 6. Compila la aplicación Angular
RUN npm run build --prod

# 7. Usa una imagen ligera para servir la aplicación en producción
FROM nginx:alpine AS production

# # 8. Copia los archivos compilados de Angular al servidor Nginx
COPY --from=build /app/../../static /usr/share/nginx/html

# 9. Copia la configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf


# 10. Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon on;"]
