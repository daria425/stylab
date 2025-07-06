"use client";
import { useQuery } from "@tanstack/react-query";
import trendAnalysisService from "@/services/trendAnalysisService";
import { formatCategoryName, capitalize } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { TrendAnalysisItem } from "@/types";
import { Badge } from "@/components/ui/badge";
import {
  Carousel,
  CarouselNext,
  CarouselPrevious,
  CarouselContent,
  CarouselItem,
} from "@/components/ui/carousel";
import {
  Sparkles,
  Shirt,
  Columns3,
  Briefcase,
  Cone,
  Palette,
  ZoomIn,
  SwatchBook,
} from "lucide-react";

function getIconForCategory(category: string, height: string, width: string) {
  switch (category) {
    case "garments":
      return <Shirt height={height} width={width} />;
    case "print_or_pattern":
      return <Columns3 height={height} width={width} />;
    case "accessories":
      return <Briefcase height={height} width={width} />;
    case "silhouette":
      return <Cone height={height} width={width} />;
    case "color_palette":
      return <Palette height={height} width={width} />;
    case "aesthetics":
      return <Sparkles height={height} width={width} />;
    case "styling_details":
      return <ZoomIn height={height} width={width} />;
    case "fabrics":
      return <SwatchBook height={height} width={width} />;
    default:
      return <Sparkles height={height} width={width} />;
  }
}
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
                    {getIconForCategory(category.category, "1em", "1em")}
                    <p className="text-sm font-semibold">
                      {formatCategoryName(category.category)}
                    </p>
                  </div>
                  <Badge variant="outline">
                    {capitalize(category.topLabel)}
                  </Badge>
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
    <main className="grid grid-cols-1 sm:grid-cols-2">
      <section>
        <h2 className="text-2xl font-bold mb-4">Trend Analysis</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {trend_analysis.map((item, index) => (
            <TrendAnalysisClassificationCard
              trendAnalysisItem={item}
              key={index}
            />
          ))}
        </div>
      </section>
      <section>
        <h2 className="text-2xl font-bold mb-4">Concept Visuals</h2>
        <div className="relative px-16">
          <Carousel className="max-w-[300px] sm:max-w-sm mx-auto">
            <CarouselContent>
              {generated_images.map((image, index) => (
                <CarouselItem key={index}>
                  <div className="p-1">
                    <Card>
                      <CardContent className="flex aspect-square items-center justify-center p-6">
                        <img
                          src={image.image_data_url}
                          alt={`Generated image ${index + 1}: ${image.prompt}`}
                          className="w-full h-full object-contain rounded"
                        />
                      </CardContent>
                    </Card>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>
      </section>
    </main>
  );
}
