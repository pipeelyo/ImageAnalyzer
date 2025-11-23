# Frontend - ImageAnalyzer

Frontend de ImageAnalyzer construido con React, TypeScript, Vite y shadcn/ui.

## Tecnologías

- **React 19** - Biblioteca de UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool y dev server
- **shadcn/ui** - Componentes UI
- **Tailwind CSS** - Estilos
- **Lucide React** - Iconos

## Instalación

```bash
cd frontend
npm install
```

## Desarrollo

Inicia el servidor de desarrollo:

```bash
npm run dev
```

O usa nodemon para reiniciar automáticamente cuando cambien archivos de configuración:

```bash
npm run dev:watch
```

La aplicación estará disponible en `http://localhost:3000`

**Nota:** Asegúrate de que el servidor Django esté corriendo en `http://localhost:8000` para que las llamadas a la API funcionen.

**Nota sobre nodemon:** Vite ya incluye Hot Module Replacement (HMR) que recarga automáticamente los cambios en el código. El script `dev:watch` con nodemon es útil principalmente cuando cambian archivos de configuración como `vite.config.ts` o `tailwind.config.js`.

## Build

Para crear una build de producción:

```bash
npm run build
```

Los archivos estáticos se generarán en la carpeta `dist/`.

## Estructura

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/          # Componentes de shadcn/ui
│   │   ├── UploadImage.tsx
│   │   └── ResultView.tsx
│   ├── services/
│   │   └── api.ts        # Servicio de API
│   ├── lib/
│   │   └── utils.ts      # Utilidades
│   ├── App.tsx
│   └── main.tsx
├── public/
└── package.json
```

## Componentes

### UploadImage
Componente para cargar y analizar imágenes satelitales.

### ResultView
Componente para mostrar los resultados del análisis.

## API

El frontend se comunica con el backend Django a través de:

- `POST /api/analyze-api/` - Analizar una imagen

El proxy está configurado en `vite.config.ts` para redirigir las peticiones `/api` a `http://localhost:8000`.
