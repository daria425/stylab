"use client";
import { useQuery } from "@tanstack/react-query";
import trendAnalysisService from "@/services/trendAnalysisService";
import { formatCategoryName } from "@/lib/utils";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Image from "next/image";
import type { TrendAnalysisItem, TrendAnalysisResponse } from "@/types";

function TrendAnalysisClassificationCard({
  trendAnalysisItem,
}: {
  trendAnalysisItem: TrendAnalysisItem;
}) {
  const { classification, images } = trendAnalysisItem;
  const categories = Object.entries(classification);
  const categoryData = categories.map(([categoryName, categoryInfo]) => ({
    category: categoryName,
    topLabel: categoryInfo.top_label,
    confidence: categoryInfo.confidence,
    allResults: categoryInfo.label_results,
  }));
  return (
    <Card>
      <CardTitle>{trendAnalysisItem.title}</CardTitle>
      <div className="relative h-48 w-full bg-gray-100 flex">
        {images.map((imageUrl, index) => (
          <Image
            key={index}
            src={imageUrl}
            alt={trendAnalysisItem.title}
            className="object-cover w-1/3 h-full"
          />
        ))}
      </div>
      <ul>
        {categoryData.map((category, index) => (
          <li key={index}>
            {category.topLabel && (
              <div>
                <h6 className="text-lg font-semibold">
                  {formatCategoryName(category.category)}
                </h6>
                <p>{category.topLabel}</p>
              </div>
            )}
          </li>
        ))}
      </ul>
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
  const { generated_images, trend_analysis, trend_summary } = data;

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
