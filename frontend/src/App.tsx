import { useState, useEffect } from 'react';
import { UploadImage } from './components/UploadImage';
import { ResultView } from './components/ResultView';
import { DitherBackground } from './components/DitherBackground';

function App() {
  const [resultImageUrl, setResultImageUrl] = useState<string | null>(null);
  const [originalImageUrl, setOriginalImageUrl] = useState<string | null>(null);
  const [isResetting, setIsResetting] = useState(false);
  const [isShowing, setIsShowing] = useState(false);

  useEffect(() => {
    if (resultImageUrl && !isResetting) {
      // Pequeño delay para activar la animación de entrada
      const timer = setTimeout(() => {
        setIsShowing(true);
      }, 10);
      return () => clearTimeout(timer);
    }
  }, [resultImageUrl, isResetting]);

  const handleResult = (resultUrl: string, originalUrl?: string) => {
    console.log('handleResult llamado:', { resultUrl, originalUrl });
    setIsShowing(false);
    setResultImageUrl(resultUrl);
    setOriginalImageUrl(originalUrl || null);
    setIsResetting(false);
  };

  const handleBack = () => {
    setIsResetting(true);
    setIsShowing(false);
    setTimeout(() => {
      setResultImageUrl(null);
      setOriginalImageUrl(null);
      setIsResetting(false);
    }, 300);
  };

  return (
    <div className="h-screen flex flex-col items-center p-4 relative overflow-hidden">
      <DitherBackground
        waveColor={[0.5, 0.5, 0.5]}
        disableAnimation={false}
        enableMouseInteraction={true}
        mouseRadius={1}
        colorNum={4}
        pixelSize={2}
        waveAmplitude={0.3}
        waveFrequency={3}
        waveSpeed={0.05}
      />
      <div className="absolute top-8 left-8 z-20">
        <img 
          src="/LogoHydroVision.png" 
          alt="HydroVision Logo" 
          className="h-32 w-auto"
        />
      </div>
      <div className="relative z-10 w-full h-full flex flex-col items-center pt-8 pb-4">
        <div className="flex-shrink-0">
          <UploadImage onResult={handleResult} onReset={resultImageUrl ? handleBack : undefined} />
        </div>
        {resultImageUrl && (
          <div className={`flex-1 flex items-center justify-center w-full min-h-0 mt-4 transition-all duration-300 ease-in-out ${isResetting ? 'opacity-0 scale-95 translate-y-4' : isShowing ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-95 translate-y-4'}`}>
            <ResultView resultImageUrl={resultImageUrl} originalImageUrl={originalImageUrl || undefined} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
