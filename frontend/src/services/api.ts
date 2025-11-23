const API_BASE_URL = '/api';

export interface AnalyzeResponse {
  result_image_url: string;
  original_image_url?: string;
  uploaded_file_url: string;
  message?: string;
}

export const analyzeImage = async (file: File): Promise<AnalyzeResponse> => {
  const formData = new FormData();
  formData.append('image', file);

  const response = await fetch(`${API_BASE_URL}/analyze-api/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Error al analizar la imagen' }));
    throw new Error(errorData.error || 'Error al analizar la imagen');
  }

  const data: AnalyzeResponse = await response.json();
  return data;
};

