import type { Metadata } from "next";
import Providers from "@/lib/providers";
import "./globals.css";
import Header from "@/components/layouts/header";
export const metadata: Metadata = {
  title: "Social Style Scan",
  description:
    "A tool to analyze and visualize fashion trends from social media",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Header />
          {children}
        </Providers>
      </body>
    </html>
  );
}
