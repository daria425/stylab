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
      <body className="h-screen grid grid-rows-[auto_minmax(0,1fr)]">
        <Providers>
          <Header />
          <main className="container mx-auto px-4 py-6 max-h-full overflow-auto text-sm">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
