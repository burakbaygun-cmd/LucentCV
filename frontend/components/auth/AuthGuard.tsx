"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter, usePathname } from "next/navigation";
import { useEffect } from "react";

const PUBLIC_ROUTES = ["/", "/login", "/register"];

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!loading) {
      const isPublicRoute = PUBLIC_ROUTES.includes(pathname);
      if (!user && !isPublicRoute) {
        router.push("/login");
      }
    }
  }, [user, loading, pathname, router]);

  // While checking auth, show spinner for protected routes
  const isPublicRoute = PUBLIC_ROUTES.includes(pathname);
  if (loading && !isPublicRoute) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-12rem)] space-y-4">
        <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        <p className="text-muted-foreground text-sm">Checking authentication...</p>
      </div>
    );
  }

  return <>{children}</>;
}
