"use client";
import { useQuery } from "@tanstack/react-query";
import trendAnalysisService from "@/services/trendAnalysisService";
import { formatCategoryName } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { TrendAnalysisItem } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Sparkles } from "lucide-react";

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
      <CardHeader>
        <CardTitle>{trendAnalysisItem.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-48 overflow-x-auto overflow-y-hidden">
          <div className="flex h-full gap-2 min-w-max">
            {images?.map((imageUrl, index) => (
              <div key={index} className="relative h-full w-32 flex-shrink-0">
                <img
                  src={imageUrl}
                  alt={`${trendAnalysisItem.title} - image ${index + 1}`}
                  className="w-full h-full object-cover rounded"
                  loading="lazy"
                />
              </div>
            ))}
          </div>
        </div>

        <ul>
          {categoryData.map((category, index) => (
            <li key={index}>
              {category.topLabel && (
                <div className="flex items-center mt-2 justify-between">
                  <div className="flex items-center gap-2">
                    <Sparkles className="h-3 w-3" />
                    <p className="text-sm font-semibold">
                      {formatCategoryName(category.category)}
                    </p>
                  </div>
                  <Badge variant="outline">{category.topLabel}</Badge>
                </div>
              )}
            </li>
          ))}
        </ul>
      </CardContent>
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
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {trend_analysis.map((item, index) => (
          <TrendAnalysisClassificationCard
            trendAnalysisItem={item}
            key={index}
          />
        ))}
      </div>
    </div>
  );
}
