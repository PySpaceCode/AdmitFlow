"use client";

import { motion } from "framer-motion";
import { Mic, MessageSquare, LayoutDashboard, FileText, CalendarCheck, BarChart3 } from "lucide-react";

const features = [
  {
    title: "AI Calling Agent",
    description: "Human-like AI voice calls every lead within 60 seconds — in Hindi, English, and regional languages.",
    icon: Mic,
  },
  {
    title: "WhatsApp Follow-ups",
    description: "Automated multi-step WhatsApp sequences that nudge leads to enroll.",
    icon: MessageSquare,
  },
  {
    title: "Lead Dashboard",
    description: "See every lead, status, and next action in one beautiful, real-time dashboard.",
    icon: LayoutDashboard,
  },
  {
    title: "Transcripts & Recordings",
    description: "Full call recordings + AI-generated transcripts and sentiment analysis.",
    icon: FileText,
  },
  {
    title: "Smart Booking",
    description: "AI books counselling sessions and admission slots directly into your calendar.",
    icon: CalendarCheck,
  },
  {
    title: "KPI Analytics",
    description: "Track calls, conversions, agent performance, and ROI with deep analytics.",
    icon: BarChart3,
  }
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

export function FeaturesSection() {
  return (
    <section className="py-24 relative" id="features">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <p className="text-[var(--color-brand-blue)] font-bold tracking-wider uppercase text-sm mb-4">Features</p>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Everything your <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-brand-purple)] to-[var(--color-brand-blue)]">admissions team</span> does — automated.</h2>
        </div>

        <motion.div 
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-100px" }}
          className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {features.map((feat, idx) => (
            <motion.div 
              key={idx}
              variants={item}
              className="group relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 hover:border-[var(--color-brand-blue)]/50 transition-colors duration-300"
            >
              {/* Hover gradient glow */}
              <div className="absolute inset-x-0 -bottom-px h-px bg-gradient-to-r from-transparent via-[var(--color-brand-blue)] to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
              
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-800 text-[var(--color-brand-purple)] group-hover:scale-110 transition-transform duration-300 mb-6">
                <feat.icon className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-semibold mb-3">{feat.title}</h3>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed">{feat.description}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
