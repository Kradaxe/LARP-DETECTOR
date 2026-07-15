import type { Metadata } from "next";
import "./globals.css";
import Header from "../components/Header";

export const metadata: Metadata = {
  title: "LARP Detector",
  description: "Analyze technical claims, resumes, and GitHub profiles for credibility",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased text-slate-900">
        <Header />
        {children}
      </body>
    </html>
  );
}
