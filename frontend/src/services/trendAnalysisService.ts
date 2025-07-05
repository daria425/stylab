import { TrendAnalysisResponse } from "@/types";
import api from "@/lib/apiConfig";

class TrendAnalysisService {
  async getTrendAnalysis(): Promise<TrendAnalysisResponse> {
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
