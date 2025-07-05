"use client";
import { useQuery } from "@tanstack/react-query";
import trendAnalysisService from "@/services/trendAnalysisService";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { TrendAnalysisItem, TrendAnalysisResponse } from "@/types";

function TrendAnalysisClassificationCard({
  trendAnalysisItem,
}: {
  trendAnalysisItem: TrendAnalysisItem;
}) {
  const { classification } = trendAnalysisItem;
  const categories = Object.entries(classification);

  // Map to get just the data you need
  const categoryData = categories.map(([categoryName, categoryInfo]) => ({
    name: categoryName,
    topLabel: categoryInfo.top_label,
    confidence: categoryInfo.confidence,
    allResults: categoryInfo.label_results,
  }));
  console.log("Category data to render:", categoryData);
  return null;
}
export default function Home() {
  const { data, error, isLoading } = useQuery({
    queryKey: ["trendAnalysis"],
    queryFn: async () => {
      const response = await trendAnalysisService.getTrendAnalysis();
      return response;
    },
  });

  if (isLoading || !data) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  const { images, trend_analysis, trend_summary } = data;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Trend Analysis</h2>
      <p>{trend_summary}</p>
      {trend_analysis.map((item, index) => (
        <TrendAnalysisClassificationCard trendAnalysisItem={item} key={index} />
      ))}
    </div>
  );
}
