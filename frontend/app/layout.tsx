import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LARP Detector",
  description: "Analyze technical claims for credibility and authenticity",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
