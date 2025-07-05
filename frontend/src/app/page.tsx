"use client";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/apiConfig";

const getTrendAnalysis = async () => {
  const response = await api.get("/api/trend-analysis");
  return response.data;
};
export default function Home() {
  const { data, error, isLoading } = useQuery({
    queryKey: ["trendAnalysis"],
    queryFn: getTrendAnalysis,
  });
  console.log(data, error, isLoading);
  return <div>Hello</div>;
}
