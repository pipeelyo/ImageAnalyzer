import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Loader2, File, Scan, RefreshCw } from 'lucide-react';
import { analyzeImage } from '@/services/api';

interface UploadImageProps {
  onResult: (resultImageUrl: string, originalImageUrl?: string) => void;
  onReset?: () => void;
}

export function UploadImage({ onResult, onReset }: UploadImageProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.name.endsWith('.tif') || selectedFile.name.endsWith('.tiff')) {
        setFile(selectedFile);
        setError(null);
      } else {
        setError('Por favor, selecciona un archivo .tif o .tiff');
        setFile(null);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      setError('Por favor, selecciona un archivo');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await analyzeImage(file);
      console.log('Resultado recibido:', result);
      onResult(result.result_image_url, result.original_image_url);
    } catch (err) {
      console.error('Error al analizar:', err);
      setError(err instanceof Error ? err.message : 'Error al analizar la imagen');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className={`w-auto max-w-2xl mx-auto !bg-background/20 backdrop-blur-lg !border-border/20 transition-all duration-300 ease-in-out ${file ? 'scale-105 shadow-lg' : 'scale-100'} relative`}>
      <CardHeader className="relative pr-20">
        {onReset && (
          <Button
            type="button"
            onClick={onReset}
            variant="ghost"
            size="icon"
            className="absolute top-4 right-4 bg-black/50 hover:bg-black/70 text-[#55f3ff] hover:text-[#55f3ff] border border-[#55f3ff]/30 rounded-full h-10 w-10 transition-all duration-300"
          >
            <RefreshCw className="h-5 w-5" />
          </Button>
        )}
        <CardTitle className="text-[#55f3ff] text-center">Cargar Imagen</CardTitle>
        <CardDescription className="text-white">
          Sube una imagen satelital en formato .tif para analizar
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4 min-w-[400px] md:min-w-0 md:w-auto">
          <div className="space-y-2">
            <div className="relative">
              <File className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground pointer-events-none transition-colors duration-200" />
              <Input
                type="file"
                accept=".tif,.tiff"
                onChange={handleFileChange}
                disabled={loading}
                className="cursor-pointer text-black file:text-black pl-10 transition-all duration-200 hover:bg-gray-100 hover:border-primary hover:shadow-md hover:scale-[1.02] focus:scale-[1.02]"
              />
            </div>
            {file && (
              <div className="text-sm text-white">
                <p className="font-medium mb-1">Archivo seleccionado:</p>
                <p className="break-words break-all">{file.name}</p>
              </div>
            )}
          </div>

          {error && (
            <div className="p-3 text-sm text-white bg-destructive/20 rounded-md border border-destructive/30">
              <strong>Error:</strong> {error}
            </div>
          )}

          {file && (
            <div className="transition-all duration-300 ease-in-out opacity-0 animate-[fadeIn_0.3s_ease-in-out_forwards]">
              <Button 
                type="submit" 
                disabled={loading} 
                className="w-full bg-black hover:bg-black/80 text-[#55f3ff] text-lg font-semibold"
              >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Analizando...
                </>
              ) : (
                <>
                  <Scan className="mr-2 h-5 w-5" />
                  Analizar
                </>
              )}
              </Button>
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
}

