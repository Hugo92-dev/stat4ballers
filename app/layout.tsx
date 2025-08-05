import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: 'Stat4Ballers - Statistiques Ligue 1',
  description: 'Toutes les stats des joueurs de Ligue 1 : données offensives, défensives et créatives pour chaque joueur.',
  keywords: ['Statistiques Ligue 1', 'Stats joueurs football', 'xG', 'xA', 'Data football'],
  openGraph: {
    title: 'Stat4Ballers - Stats Ligue 1',
    description: 'Visualisez toutes les stats des joueurs de Ligue 1 en un coup d’œil.',
    url: 'https://stat4ballers.vercel.app',
    siteName: 'Stat4Ballers',
    type: 'website',
  },
  metadataBase: new URL('https://stat4ballers.vercel.app'),
  alternates: {
    canonical: '/',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
