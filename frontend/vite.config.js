import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,          // visible desde el celular en la misma red
    allowedHosts: true,  // acepta enlaces públicos temporales (túneles)
    // Todo lo que empiece con /api se reenvía al backend de Django.
    // Así el navegador (o el celular) solo habla con UN enlace.
    proxy: {
      "/api": { target: "http://127.0.0.1:8000", changeOrigin: true },
    },
  },
});
