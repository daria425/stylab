import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "*",
      },
      {
        protocol: "http",
        hostname: "*", // Allow all hostnames (if needed)
      },
    ],
  },
};

export default nextConfig;
//
