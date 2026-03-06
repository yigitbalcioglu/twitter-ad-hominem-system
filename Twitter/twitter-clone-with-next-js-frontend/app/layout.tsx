import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import AppShell from "../components/layout/AppShell";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Twitter Clone",
  description: "A Next.js Twitter-style social app",
};

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <html lang="tr">
      <body className={`${inter.className} min-h-screen bg-black text-white`}>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
};

export default Layout;