import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "i.pinimg.com",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "*.pinimg.com", // Covers subdomains
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;
//
