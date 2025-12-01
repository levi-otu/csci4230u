FROM node:20-alpine AS build

WORKDIR /app

# Copy dependency manifests and install deps
COPY package.json package-lock.json* ./
RUN npm ci

# Copy the rest of the app source
COPY . .

# Accept build argument for API URL
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Build for production (Vite/CRA/etc)
RUN npm run build

# ---- Runtime image ----
FROM node:20-alpine AS runtime

WORKDIR /app

RUN npm install -g serve

# If your build output is "dist" (Vite), this is correct.
# If it's "build" (CRA), change both "dist" occurrences to "build".
COPY --from=build /app/dist ./dist

ENV PORT=8080

CMD ["sh", "-c", "serve -s dist -l ${PORT}"]
