"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Sparkles, ArrowLeft, Send } from "lucide-react";
import { useState } from "react";
import { ThemeToggle } from "@/components/ThemeToggle";

export default function ForgotPasswordPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Simulate API request
    setTimeout(() => {
      setIsLoading(false);
      setEmailSent(true);
    }, 1500);
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-background text-foreground p-4 relative overflow-hidden transition-colors duration-300">
      {/* Floating Theme Toggle */}
      <div className="absolute top-6 right-6 z-50">
        <ThemeToggle />
      </div>

      {/* Decorative Orbs */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-gradient-to-bl from-[var(--color-brand-cyan)]/10 to-[var(--color-brand-blue)]/5 blur-[150px] rounded-full pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-gradient-to-tr from-[var(--color-brand-purple)]/10 to-[var(--color-brand-blue)]/5 blur-[150px] rounded-full pointer-events-none" />

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md relative z-10"
      >
        <div className="flex items-center justify-center gap-3 mb-8">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="p-2 rounded-xl bg-gradient-to-br from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] shadow-lg shadow-brand-blue/20 group-hover:shadow-brand-blue/40 transition-all duration-300">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-3xl tracking-tight text-foreground">AdmitFlow.</span>
          </Link>
        </div>

        <div className="bg-card/80 backdrop-blur-xl p-8 rounded-3xl border border-border/60 shadow-2xl relative overflow-hidden">
          {/* Subtle inner card glow */}
          <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-[var(--color-brand-blue)]/10 to-transparent -z-10" />

          <Link href="/login" className="inline-flex items-center text-sm font-medium text-muted-foreground hover:text-foreground mb-8 transition-colors group">
            <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" /> Back to login
          </Link>

          <h2 className="text-2xl font-bold tracking-tight mb-2">Reset Password</h2>
          <p className="text-muted-foreground text-sm mb-6">
            Enter your email address and we'll send you a secure link to reset your password.
          </p>

          {emailSent ? (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="p-5 bg-[var(--color-brand-cyan)]/10 border border-[var(--color-brand-cyan)]/20 rounded-2xl text-[var(--color-brand-blue)] dark:text-[var(--color-brand-cyan)] text-center text-sm font-medium shadow-inner"
            >
              Check your email for the reset link! You can safely close this window.
            </motion.div>
          ) : (
            <form onSubmit={handleReset} className="space-y-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground/80 pl-1 block">Email Address</label>
                <input
                  type="email"
                  placeholder="name@institute.edu"
                  className="w-full px-4 py-3 bg-background/50 border border-input text-foreground rounded-xl focus:ring-2 focus:ring-[var(--color-brand-blue)]/50 focus:border-[var(--color-brand-blue)] outline-none transition-all placeholder:text-muted-foreground shadow-sm"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3.5 px-4 bg-gradient-to-r from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] hover:opacity-90 text-white font-semibold rounded-xl transition-all shadow-[0_4px_20px_rgba(47,107,255,0.25)] hover:shadow-[0_8px_30px_rgba(47,107,255,0.4)] flex items-center justify-center disabled:opacity-70 disabled:cursor-not-allowed group"
              >
                {isLoading ? (
                  <span className="inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    Send Reset Link
                    <Send className="w-4 h-4 ml-2 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
                  </>
                )}
              </button>
            </form>
          )}
        </div>
      </motion.div>
    </div>
  );
}
