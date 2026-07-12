"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, History } from "lucide-react";

const routes = [
  {
    href: "/dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    href: "/history",
    label: "History",
    icon: History,
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="hidden md:flex h-[calc(100vh-3.5rem)] w-56 flex-col border-r border-border/40 bg-background/50 backdrop-blur-xl sticky top-14">
      <div className="flex-1 overflow-auto py-6">
        <nav className="grid items-start px-4 text-sm font-medium">
          {routes.map((route) => {
            const Icon = route.icon;
            return (
              <Link
                key={route.href}
                href={route.href}
                className={`flex items-center gap-3 rounded-lg px-3 py-2.5 transition-all hover:text-primary ${
                  pathname === route.href
                    ? "bg-muted text-primary"
                    : "text-muted-foreground hover:bg-muted"
                }`}
              >
                <Icon className="h-4 w-4" />
                {route.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
}
