"use client";

import Link from "next/link";
import { ThemeToggle } from "./ThemeToggle";
import { Sparkles } from "lucide-react";

export function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-50 transition-all duration-300 bg-background/80 backdrop-blur-md border-b border-border/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex-shrink-0">
            <Link href="/" className="flex items-center gap-2">
              <div className="p-1.5 rounded-lg bg-gradient-to-br from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)]">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-xl tracking-tight">AdmitFlow</span>
            </Link>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-8">
              <Link href="#features" className="hover:text-brand-blue px-3 py-2 rounded-md text-sm font-medium transition-colors">Features</Link>
              <Link href="#workflow" className="hover:text-brand-blue px-3 py-2 rounded-md text-sm font-medium transition-colors">Workflow</Link>
              <Link href="#pricing" className="hover:text-brand-blue px-3 py-2 rounded-md text-sm font-medium transition-colors">Pricing</Link>
            </div>
          </div>
          <div className="flex flex-row items-center gap-4">
            <ThemeToggle />
            <Link href="/login" className="hidden sm:flex px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] rounded-full hover:shadow-lg hover:shadow-brand-blue/30 transition-all duration-300">
              Get Started
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
