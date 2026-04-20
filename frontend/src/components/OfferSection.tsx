import { ArrowRight, Sparkles } from "lucide-react";
import Link from "next/link";

export function OfferSection() {
  return (
    <section className="py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] opacity-10 dark:opacity-20" />
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm border border-[var(--color-brand-blue)]/50 text-[var(--color-brand-blue)] text-sm font-bold mb-8">
          <Sparkles className="w-4 h-4" /> 🆓 Free Trial · No Credit Card · Pay Only For Results
        </div>
        
        <h2 className="text-4xl md:text-6xl font-bold mb-6">Ready to automate your admissions?</h2>
        <p className="text-xl md:text-2xl text-slate-700 dark:text-slate-300 mb-10 font-medium">
          Replace 1 employee with AI today. Live in 24 hours. Cancel anytime.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="#pricing"
            className="group relative px-8 py-4 bg-gradient-to-r from-[var(--color-brand-purple)] via-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] text-white rounded-full font-semibold text-lg overflow-hidden shadow-2xl hover:shadow-cyan/50 transition-all w-full sm:w-auto"
          >
            <div className="absolute inset-0 bg-white/20 group-hover:translate-x-full transition-transform duration-500 ease-out -skew-x-12 -ml-4 w-1/2" />
            <span className="relative flex items-center justify-center gap-2">
              Start Free Trial <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </span>
          </Link>
          <Link
            href="#demo"
            className="group px-8 py-4 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border-2 border-slate-300 dark:border-slate-700 hover:border-slate-400 dark:hover:border-slate-600 rounded-full font-semibold text-lg transition-colors w-full sm:w-auto"
          >
            Book Demo
          </Link>
        </div>
      </div>
    </section>
  );
}
