type ClassificationCategory = {
  top_label: string | null;
  confidence: number | null;
  label_results: { [key: string]: number }; // Dynamic keys with number values
};

type Classification = { [key: string]: ClassificationCategory }; // Dynamic category names

export type TrendAnalysisItem = {
  title: string;
  url: string;
  img: string;
  classification: Classification;
};

type TrendImages = {
  prompt: string;
  image_data_url: string;
};

export type TrendAnalysisResponse = {
  trend_summary: string;
  images: TrendImages[];
  trend_analysis: TrendAnalysisItem[];
};
