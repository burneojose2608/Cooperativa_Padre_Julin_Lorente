import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

// https://vite.dev/config/
export default defineConfig(({ mode, command }) => {
  const entorno = loadEnv(mode, process.cwd(), "");
  const https = mode !== "test" && (mode === "https" || entorno.VITE_HTTPS === "true");
  return {
    plugins: [react()],
    define: { "import.meta.env.VITE_HTTPS": JSON.stringify(https ? "true" : "false") },
    test: {
      environment: "jsdom",
      globals: true,
      setupFiles: ["./src/test/setup.js"],
      include: ["src/**/*.test.{js,jsx}"],
    },
    server: {
      https: https && command === "serve" ? {
        cert: readFileSync(entorno.TLS_CERT_FILE || resolve("../backend/.local-tls/localhost.crt")),
        key: readFileSync(entorno.TLS_KEY_FILE || resolve("../backend/.local-tls/localhost.key")),
      } : undefined,
      host: true,          // visible desde el celular en la misma red
      allowedHosts: true,  // acepta enlaces públicos temporales (túneles)
      // El navegador usa el mismo origen; el proxy sustituye el protocolo declarado.
      proxy: {
        "/api": {
          target: entorno.API_PROXY_TARGET || "http://127.0.0.1:8000", changeOrigin: true,
          headers: { "x-forwarded-proto": https ? "https" : "http" },
        },
      },
    },
  };
});
