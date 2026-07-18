"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, History, Sparkles, Menu, LogOut, LogIn } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet";

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

function getInitials(name: string | null | undefined, email: string | null | undefined) {
  if (name) {
    const parts = name.trim().split(" ");
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    return parts[0].substring(0, 2).toUpperCase();
  }
  if (email) {
    return email.substring(0, 2).toUpperCase();
  }
  return "U";
}

export function Navbar() {
  const pathname = usePathname();
  const { user, signOut } = useAuth();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center px-4">
        {/* Desktop Nav */}
        <div className="mr-4 hidden md:flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <Sparkles className="h-5 w-5 text-primary" />
            <span className="hidden font-bold sm:inline-block text-lg tracking-tight">
              LucentCV
            </span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            {routes.map((route) => (
              <Link
                key={route.href}
                href={route.href}
                className={`transition-colors hover:text-foreground/80 ${
                  pathname === route.href ? "text-foreground" : "text-foreground/60"
                }`}
              >
                {route.label}
              </Link>
            ))}
          </nav>
        </div>

        {/* Mobile Nav */}
        <div className="flex flex-1 items-center md:hidden">
          <Sheet>
            <SheetTrigger className="mr-2 inline-flex h-9 w-9 items-center justify-center rounded-md hover:bg-accent hover:text-accent-foreground">
              <Menu className="h-5 w-5" />
              <span className="sr-only">Toggle Menu</span>
            </SheetTrigger>
            <SheetContent side="left" className="pr-0">
              <Link href="/" className="flex items-center space-x-2 mb-8 mt-4">
                <Sparkles className="h-5 w-5 text-primary" />
                <span className="font-bold inline-block text-lg">LucentCV</span>
              </Link>
              <div className="flex flex-col space-y-3">
                {routes.map((route) => (
                  <Link
                    key={route.href}
                    href={route.href}
                    className={`text-sm ${
                      pathname === route.href ? "text-primary font-semibold" : "text-foreground/70"
                    }`}
                  >
                    {route.label}
                  </Link>
                ))}
              </div>
            </SheetContent>
          </Sheet>
          <Link href="/" className="mr-2 flex items-center space-x-2">
            <Sparkles className="h-5 w-5 text-primary" />
            <span className="font-bold inline-block text-lg tracking-tight">
              LucentCV
            </span>
          </Link>
        </div>

        {/* Right side actions */}
        <div className="flex flex-1 items-center justify-end space-x-4">
          {user ? (
            <div className="flex items-center space-x-4">
              <div className="flex items-center gap-2">
                <Avatar size="default" className="h-8 w-8">
                  <AvatarImage src={user.user_metadata?.avatar_url} alt={user.user_metadata?.full_name || user.email || ""} />
                  <AvatarFallback className="bg-primary/10 text-primary font-bold">
                    {getInitials(user.user_metadata?.full_name, user.email)}
                  </AvatarFallback>
                </Avatar>
                <span className="text-sm font-semibold hidden md:inline-block max-w-[150px] truncate">
                  {user.user_metadata?.full_name || user.email?.split("@")[0]}
                </span>
              </div>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={signOut}
                className="text-muted-foreground hover:text-foreground flex items-center gap-1.5"
              >
                <LogOut className="h-4 w-4" />
                <span className="hidden md:inline">Log out</span>
              </Button>
            </div>
          ) : (
            pathname !== "/login" && pathname !== "/register" && (
              <Link href="/login">
                <Button size="sm" className="flex items-center gap-1.5">
                  <LogIn className="h-4 w-4" />
                  Sign In
                </Button>
              </Link>
            )
          )}
        </div>
      </div>
    </header>
  );
}
