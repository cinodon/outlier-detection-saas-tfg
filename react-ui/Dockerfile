# Utilizar una imagen ligera de Node
FROM node:16-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar las dependencias
RUN npm install

# Copiar el resto del código fuente
COPY . .

# Construir la aplicación
RUN npm run build

# Utilizar un servidor web para servir la aplicación en producción
RUN npm install -g serve
CMD ["serve", "-s", "build"]

# Exponer el puerto
EXPOSE 3000
