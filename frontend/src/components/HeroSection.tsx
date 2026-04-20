"use client";

import { motion } from "framer-motion";
import { ArrowRight, Play } from "lucide-react";
import Link from "next/link";

export function HeroSection() {
  return (
    <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-br from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] opacity-20 dark:opacity-30 blur-[100px] rounded-full pointer-events-none" />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 text-sm font-medium mb-8"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[var(--color-brand-blue)] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[var(--color-brand-blue)]"></span>
            </span>
            🤖 AI Admission Team — Live in 24 hrs
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8"
          >
            Stop Hiring Callers. <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)]">
              Start Closing Admissions with AI.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-xl md:text-2xl text-slate-600 dark:text-slate-400 mb-10 max-w-2xl mx-auto"
          >
            AdmitFlow's AI calls every lead, follows up on WhatsApp, and hooks admissions — replacing your tele-calling team with a 24/7 conversion engine.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link
              href="#pricing"
              className="group relative px-8 py-4 bg-gradient-to-r from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] text-white rounded-full font-semibold text-lg overflow-hidden shadow-lg shadow-brand-blue/20 hover:shadow-cyan/40 transition-all w-full sm:w-auto"
            >
              <div className="absolute inset-0 bg-white/20 group-hover:translate-x-full transition-transform duration-500 ease-out -skew-x-12 -ml-4 w-1/2" />
              <span className="relative flex items-center justify-center gap-2">
                Start Free Trial <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </span>
            </Link>
            
            <Link
              href="#demo"
              className="px-8 py-4 bg-white dark:bg-slate-900 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-800 rounded-full font-semibold text-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors flex items-center justify-center gap-2 w-full sm:w-auto"
            >
              <Play className="w-5 h-5" /> Book Demo
            </Link>
          </motion.div>

          {/* Checkmarks */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="flex flex-wrap items-center justify-center gap-6 mt-8 text-sm font-medium text-slate-500 dark:text-slate-400"
          >
            <span className="flex items-center gap-1.5"><span className="text-green-500">✓</span> No credit card</span>
            <span className="flex items-center gap-1.5"><span className="text-green-500">✓</span> Live in 24 hours</span>
            <span className="flex items-center gap-1.5"><span className="text-green-500">✓</span> Pay for results</span>
          </motion.div>

          {/* Stats Dashboard (Live Preview Card) */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.5 }}
            className="mt-16 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-2xl text-left max-w-3xl mx-auto relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-gradient-to-br from-[var(--color-brand-blue)]/5 to-[var(--color-brand-cyan)]/5 rounded-full blur-3xl pointer-events-none -mr-40 -mt-40" />
            
            <div className="grid grid-cols-3 gap-4 mb-6 pb-6 border-b border-slate-100 dark:border-slate-800 relative z-10">
              <div className="text-center">
                <p className="text-sm text-slate-500 font-medium mb-1">Leads Today</p>
                <p className="text-3xl font-bold text-slate-900 dark:text-white">1,284</p>
              </div>
              <div className="text-center border-l border-r border-slate-100 dark:border-slate-800">
                <p className="text-sm text-slate-500 font-medium mb-1">AI Calls Made</p>
                <p className="text-3xl font-bold text-[var(--color-brand-blue)]">987</p>
              </div>
              <div className="text-center">
                <p className="text-sm text-slate-500 font-medium mb-1">Conversions</p>
                <p className="text-3xl font-bold text-green-500">143</p>
              </div>
            </div>
            <div className="relative z-10">
              <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                </span>
                Live AI Activity
              </p>
              <div className="space-y-3">
                <div className="flex items-start gap-3 bg-white dark:bg-slate-800 p-3 rounded-lg border border-slate-100 dark:border-slate-700 shadow-sm">
                  <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 shrink-0">🤖</div>
                  <p className="text-sm text-slate-600 dark:text-slate-300"><span className="font-semibold text-slate-900 dark:text-white">AI called Riya Sharma</span> — Interested in B.Tech</p>
                </div>
                <div className="flex items-start gap-3 bg-white dark:bg-slate-800 p-3 rounded-lg border border-slate-100 dark:border-slate-700 shadow-sm">
                  <div className="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center text-green-600 shrink-0">💬</div>
                  <p className="text-sm text-slate-600 dark:text-slate-300"><span className="font-semibold text-slate-900 dark:text-white">WhatsApp follow-up</span> sent in 14 secs</p>
                </div>
                <div className="flex items-start gap-3 bg-white dark:bg-slate-800 p-3 rounded-lg border border-slate-100 dark:border-slate-700 shadow-sm">
                  <div className="w-8 h-8 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center text-purple-600 shrink-0">📅</div>
                  <p className="text-sm text-slate-600 dark:text-slate-300"><span className="font-semibold text-slate-900 dark:text-white">Demo session:</span> Arjun Verma (MBA program)</p>
                </div>
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
}
