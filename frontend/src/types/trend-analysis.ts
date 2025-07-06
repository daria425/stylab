type ClassificationCategory = {
  top_label: string | null;
  confidence: number | null;
  label_results: { [key: string]: number }; // Dynamic keys with number values
};

type Classification = { [key: string]: ClassificationCategory }; // Dynamic category names

export type TrendAnalysisItem = {
  title: string;
  url: string;
  images: Array<string>;
  classification: Classification;
};

type GeneratedImages = {
  prompt: string;
  image_data_url: string;
};

export type TrendAnalysisResponse = {
  trend_summary: string;
  generated_images: GeneratedImages[];
  trend_analysis: TrendAnalysisItem[];
};
