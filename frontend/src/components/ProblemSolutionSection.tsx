"use client";

import { motion } from "framer-motion";
import { XCircle, CheckCircle2 } from "lucide-react";

const problems = [
  "Hiring callers is expensive (₹15k–25k each)",
  "They quit, get sick, or skip leads",
  "Zero call tracking or transparency",
  "Inconsistent follow-ups — lost admissions",
];

const solutions = [
  "AI handles 1000s of calls per day",
  "Works 24/7, never misses a lead",
  "Full transcripts, recordings, analytics",
  "Smart follow-ups → 3x conversions",
];

export function ProblemSolutionSection() {
  return (
    <section className="py-24 bg-slate-50 dark:bg-slate-900/50 relative overflow-hidden" id="product">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Tele-calling is <span className="text-slate-500">broken.</span> We <span className="text-[var(--color-brand-blue)]">fixed it.</span>
          </h2>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Problem Card */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 shadow-sm"
          >
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 dark:bg-red-900/30 text-red-600 mb-6">
              <span className="text-2xl font-bold">😢</span>
            </div>
            <p className="text-sm font-bold text-red-500 uppercase tracking-wider mb-2">THE PROBLEM</p>
            <h3 className="text-2xl font-semibold mb-6">Hiring humans</h3>
            <ul className="space-y-4">
              {problems.map((problem, idx) => (
                <li key={idx} className="flex items-start gap-3 text-slate-600 dark:text-slate-400 font-medium">
                  <XCircle className="w-6 h-6 text-red-500 shrink-0" />
                  <span>{problem}</span>
                </li>
              ))}
            </ul>
          </motion.div>

          {/* Solution Card */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="bg-gradient-to-b from-white to-slate-50 dark:from-slate-800 dark:to-slate-900 border-2 border-[var(--color-brand-blue)] rounded-3xl p-8 shadow-xl relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 -mr-8 -mt-8 w-32 h-32 bg-[var(--color-brand-blue)] opacity-10 rounded-full blur-2xl pointer-events-none" />
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-[var(--color-brand-blue)]/10 text-[var(--color-brand-blue)] mb-6">
              <span className="text-2xl font-bold">🤖</span>
            </div>
            <p className="text-sm font-bold text-[var(--color-brand-blue)] uppercase tracking-wider mb-2">THE SOLUTION</p>
            <h3 className="text-2xl font-semibold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-brand-blue)] to-[var(--color-brand-cyan)]">AdmitFlow AI</h3>
            <ul className="space-y-4">
              {solutions.map((solution, idx) => (
                <li key={idx} className="flex items-start gap-3 font-medium text-slate-800 dark:text-slate-200">
                  <CheckCircle2 className="w-6 h-6 text-[var(--color-brand-cyan)] shrink-0" />
                  <span>{solution}</span>
                </li>
              ))}
            </ul>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
