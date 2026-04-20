"use client";

import { motion } from "framer-motion";
import { Star } from "lucide-react";

const testimonials = [
  {
    quote: "We replaced 5 callers with AdmitFlow. Admissions went up 41% in one batch — and our cost dropped by ₹40k/month.",
    author: "Priya Mehra",
    role: "Director, Ananya Arts & Learning",
    metric: "-₹40k Costs"
  },
  {
    quote: "Our AI literally calls leads in 30 seconds. I used to lose 60% of leads to slow follow-ups. Not anymore.",
    author: "Rohit Singh",
    role: "Owner, Shiksha Institute Centre",
    metric: "30s Calling"
  },
  {
    quote: "The transcripts and analytics gave us insights we never had. We optimised our pitch and doubled conversions.",
    author: "Sanjay Kapoor",
    role: "Director, Techbridge Institute",
    metric: "2x Conversions"
  }
];

export function TestimonialsSection() {
  return (
    <section className="py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-slate-50 dark:bg-slate-900/50 -skew-y-3 origin-bottom-left -z-10" />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Loved by <span className="text-[var(--color-brand-blue)]">200+</span> institutes</h2>
          <p className="text-xl text-slate-600 dark:text-slate-400">Real results from automated admissions.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((test, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1 }}
              className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/50 rounded-3xl p-8 shadow-sm flex flex-col"
            >
              <div className="flex gap-1 text-yellow-400 mb-6">
                {[...Array(5)].map((_, i) => <Star key={i} className="w-5 h-5 fill-current" />)}
              </div>
              <p className="text-lg text-slate-700 dark:text-slate-300 mb-8 italic flex-1">"{test.quote}"</p>
              
              <div className="mb-6 inline-flex items-center justify-center px-4 py-2 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-full font-bold text-sm w-fit">
                {test.metric}
              </div>

              <div className="border-t border-slate-100 dark:border-slate-700 pt-6">
                <p className="font-bold text-slate-900 dark:text-white">{test.author}</p>
                <p className="text-sm text-slate-500 dark:text-slate-400">{test.role}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
