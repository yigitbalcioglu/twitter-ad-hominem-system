"use client";

import React from "react";
import { usePathname } from "next/navigation";
import Sidebar from "./Sidebar";

interface AppShellProps {
  children: React.ReactNode;
}

const AUTH_ROUTES = new Set(["/login", "/register"]);

export default function AppShell({ children }: AppShellProps) {
  const pathname = usePathname();
  const isAuthRoute = pathname ? AUTH_ROUTES.has(pathname) : false;

  if (isAuthRoute) {
    return <div className="min-h-screen">{children}</div>;
  }

  return (
    <div className="min-h-screen">
      <div className="mx-auto flex min-h-screen w-full max-w-6xl lg:px-8">
        <div className="grid w-full grid-cols-1 lg:grid-cols-12">
          <div className="lg:col-span-3">
            <Sidebar />
          </div>
          <div className="border-x-0 border-neutral-800 pb-20 sm:border-x lg:col-span-9 lg:pb-0 xl:col-span-8">{children}</div>
        </div>
      </div>
    </div>
  );
}
