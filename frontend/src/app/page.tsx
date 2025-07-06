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
  const categoryData = categories.map(([categoryName, categoryInfo]) => ({
    category: categoryName,
    topLabel: categoryInfo.top_label,
    confidence: categoryInfo.confidence,
    allResults: categoryInfo.label_results,
  }));
  return (
    <Card>
      <CardTitle>Classification</CardTitle>
      <div>
        {categoryData.map((category, index) => (
          <div key={index}>
            <h3 className="text-lg font-semibold">{category.category}</h3>
            <p>Top Label: {category.topLabel || "N/A"}</p>
            <p>
              Confidence:{" "}
              {category.confidence !== null
                ? `${(category.confidence * 100).toFixed(2)}%`
                : "N/A"}
            </p>
            {/* <ul>
              {
                Object.entries(category.allResults).map(([label, score]) => (
                  <li key={label}>
                    {label}: {score}
                  </li>
                ))
              }
            </ul> */}
          </div>
        ))}
      </div>
    </Card>
  );
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
