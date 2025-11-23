import { ComparisonSlider, ComparisonBefore, ComparisonAfter } from '@/components/ui/comparison-slider';

interface ResultViewProps {
  resultImageUrl: string;
  originalImageUrl?: string;
}

export function ResultView({ resultImageUrl, originalImageUrl }: ResultViewProps) {
  console.log('ResultView renderizado:', { resultImageUrl, originalImageUrl });
  
  // Si no hay imagen original, mostrar solo el resultado
  if (!originalImageUrl) {
    return (
      <div className="w-full max-w-5xl mx-auto h-full flex items-center justify-center">
        <img
          src={resultImageUrl}
          alt="Resultado de Clasificación"
          className="max-w-full max-h-full w-auto h-auto object-contain rounded-lg border-2 border-[#55f3ff]/30 shadow-2xl transition-all duration-300 ease-in-out"
        />
      </div>
    );
  }

  return (
    <div className="w-full max-w-5xl mx-auto h-full flex items-center justify-center p-4">
      <div className="h-full max-h-full flex items-center justify-center">
        <div className="h-full max-h-full relative inline-block">
          {/* Imagen invisible para establecer el ancho del contenedor */}
          <img
            src={originalImageUrl}
            alt=""
            className="h-full max-h-full w-auto object-contain opacity-0 pointer-events-none"
            aria-hidden="true"
          />
          <ComparisonSlider className="absolute inset-0 h-full">
            <ComparisonBefore>
              <img
                src={originalImageUrl}
                alt="Imagen Original"
                className="h-full max-h-full w-auto object-contain rounded-lg select-none block"
                draggable={false}
                onLoad={() => console.log('Imagen original cargada')}
                onError={(e) => console.error('Error cargando imagen original:', e)}
              />
            </ComparisonBefore>
            <ComparisonAfter>
              <img
                src={resultImageUrl}
                alt="Resultado de Clasificación"
                className="h-full max-h-full w-auto object-contain rounded-lg select-none block"
                draggable={false}
                onLoad={() => console.log('Imagen resultado cargada')}
                onError={(e) => console.error('Error cargando imagen resultado:', e)}
              />
            </ComparisonAfter>
          </ComparisonSlider>
        </div>
      </div>
    </div>
  );
}

