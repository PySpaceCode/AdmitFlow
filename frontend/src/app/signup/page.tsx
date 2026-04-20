"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import Image from "next/image";
import { Sparkles, ArrowRight, ArrowLeft } from "lucide-react";
import { useState } from "react";
import { ThemeToggle } from "@/components/ThemeToggle"; 

export default function SignupPage() {
  const [isLoading, setIsLoading] = useState(false);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Simulate signup request
    setTimeout(() => {
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen w-full flex bg-background text-foreground transition-colors duration-300 relative">
      {/* Floating Theme Toggle */}
      <div className="absolute top-6 right-6 z-50">
        <ThemeToggle />
      </div>

      {/* Back to home */}
      <div className="absolute top-6 left-6 z-50 lg:hidden">
        <Link href="/" className="flex items-center text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Link>
      </div>

      {/* Left Section - Graphic / Copy */}
      <div className="hidden lg:flex w-1/2 flex-col justify-center relative items-center p-12 overflow-hidden bg-background border-r border-border/50">
        <div className="absolute inset-0 z-0">
          <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] rounded-full bg-gradient-to-br from-[var(--color-brand-blue)]/10 to-[var(--color-brand-cyan)]/10 blur-[130px]" />
          <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-[var(--color-brand-purple)]/10 blur-[100px]" />
        </div>
        
        <div className="z-10 flex flex-col items-center justify-center max-w-lg text-center">
          <motion.div 
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, type: "spring" }}
            className="relative"
          >
            {/* Pulsing rings behind mascot */}
            <motion.div 
              animate={{ scale: [1, 1.05, 1], opacity: [0.3, 0.5, 0.3] }}
              transition={{ repeat: Infinity, duration: 4, ease: "easeInOut", delay: 0.5 }}
              className="absolute inset-0 rounded-full bg-gradient-to-tl from-[var(--color-brand-purple)] to-[var(--color-brand-cyan)] blur-2xl -z-20 opacity-30 dark:opacity-40"
            />

            <motion.div 
              animate={{ y: [0, -12, 0] }}
              transition={{ repeat: Infinity, duration: 5, ease: "easeInOut", delay: 0.2 }}
              className="relative w-80 h-80 mb-10 rounded-full p-2 bg-gradient-to-b from-[var(--color-brand-cyan)]/30 to-transparent shadow-[0_0_80px_rgba(47,107,255,0.15)] border border-[var(--color-brand-cyan)]/40 backdrop-blur-xl overflow-hidden flex items-center justify-center"
            >
              <div className="absolute inset-0 rounded-full bg-card/60 dark:bg-black/40 backdrop-blur-2xl -z-10" />
              <div className="relative w-72 h-72">
                <Image
                  src="/admitflow_mascot.png"
                  alt="AdmitFlow Robot Mascot"
                  fill
                  className="object-cover rounded-full"
                  priority
                />
              </div>
            </motion.div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <h1 className="text-4xl lg:text-5xl font-bold tracking-tight bg-gradient-to-r from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] bg-clip-text text-transparent mt-4 pb-2">
              The secret weapon of<br />modern admission teams
            </h1>
            <p className="mt-6 text-muted-foreground text-lg max-w-md mx-auto">
              Join thousands of institutions already streamlining their entire enrollment workflow with AdmitFlow.
            </p>
          </motion.div>
        </div>
      </div>

      {/* Right Section - Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-background lg:bg-card/30 relative overflow-hidden">
        {/* Subtle light/dark background element for form side */}
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] rounded-full bg-[var(--color-brand-blue)]/5 blur-[120px] pointer-events-none" />

        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-md relative z-10"
        >
          {/* Logo */}
          <div className="flex items-center justify-center gap-3 mb-8">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="p-2 rounded-xl bg-gradient-to-br from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] shadow-lg shadow-brand-blue/20 group-hover:shadow-brand-blue/40 transition-all duration-300">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-3xl tracking-tight text-foreground">AdmitFlow.</span>
            </Link>
          </div>

          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold tracking-tight mb-2">Create Account</h2>
            <p className="text-sm text-muted-foreground">Set up your institution in seconds</p>
          </div>

          <div className="bg-card/80 backdrop-blur-xl p-8 rounded-3xl border border-border/60 shadow-2xl relative overflow-hidden">
             {/* Subtle inner card glow */}
             <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-[var(--color-brand-cyan)]/10 to-transparent -z-10" />

            <form onSubmit={handleSignup} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground/80 pl-1 block">Full Name</label>
                <input
                  type="text"
                  placeholder="Jane Doe"
                  className="w-full px-4 py-3 bg-background/50 border border-input text-foreground rounded-xl focus:ring-2 focus:ring-[var(--color-brand-blue)]/50 focus:border-[var(--color-brand-blue)] outline-none transition-all placeholder:text-muted-foreground shadow-sm"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground/80 pl-1 block">Institute Name</label>
                <input
                  type="text"
                  placeholder="E.g. Harvard University"
                  className="w-full px-4 py-3 bg-background/50 border border-input text-foreground rounded-xl focus:ring-2 focus:ring-[var(--color-brand-blue)]/50 focus:border-[var(--color-brand-blue)] outline-none transition-all placeholder:text-muted-foreground shadow-sm"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground/80 pl-1 block">Email</label>
                <input
                  type="email"
                  placeholder="name@institute.edu"
                  className="w-full px-4 py-3 bg-background/50 border border-input text-foreground rounded-xl focus:ring-2 focus:ring-[var(--color-brand-blue)]/50 focus:border-[var(--color-brand-blue)] outline-none transition-all placeholder:text-muted-foreground shadow-sm"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground/80 pl-1 block">Password</label>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full px-4 py-3 bg-background/50 border border-input text-foreground rounded-xl focus:ring-2 focus:ring-[var(--color-brand-blue)]/50 focus:border-[var(--color-brand-blue)] outline-none transition-all placeholder:text-muted-foreground shadow-sm"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full mt-8 py-3.5 px-4 bg-gradient-to-r from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] hover:opacity-90 text-white font-semibold rounded-xl transition-all shadow-[0_4px_20px_rgba(47,107,255,0.25)] hover:shadow-[0_8px_30px_rgba(47,107,255,0.4)] flex items-center justify-center disabled:opacity-70 disabled:cursor-not-allowed group"
              >
                {isLoading ? (
                  <span className="inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    Continue
                    <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </form>

            <div className="mt-8 pt-6 border-t border-border/60 text-center">
              <p className="text-sm text-muted-foreground">
                Already have an account?{" "}
                <Link href="/login" className="text-[var(--color-brand-blue)] hover:text-[var(--color-brand-cyan)] font-semibold transition-colors">
                  Sign In
                </Link>
              </p>
            </div>
          </div>
          
          <div className="mt-6 text-center px-4">
            <p className="text-xs text-muted-foreground/80">
              By creating an account, you agree to the{" "}
              <Link href="#" className="underline hover:text-foreground">Terms of Service</Link> and{" "}
               <Link href="#" className="underline hover:text-foreground">Privacy Policy</Link>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
