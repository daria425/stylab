import { TrendAnalysisResponse } from "@/types";
import api from "@/lib/apiConfig";
import mockTrendAnalysisData from "@/data/mockTrendAnalysisData.json";
class TrendAnalysisService {
  async getTrendAnalysis(): Promise<TrendAnalysisResponse> {
    if (process.env.NODE_ENV === "development") {
      // For development, return mock data
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(mockTrendAnalysisData as any); // Cast to any to avoid type issues
        }, 1000); // Simulate network delay
      });
    }
    try {
      const response = await api.get<TrendAnalysisResponse>(
        "/api/trend-analysis"
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching trend analysis:", error);
      throw error;
    }
  }
}

const trendAnalysisService = new TrendAnalysisService();
export default trendAnalysisService;
