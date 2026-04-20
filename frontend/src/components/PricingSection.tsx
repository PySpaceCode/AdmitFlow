"use client";

import { motion } from "framer-motion";
import { Check } from "lucide-react";

const plans = [
  {
    name: "Starter Automation",
    badge: "🟢",
    price: "₹1,999",
    period: "/mo",
    description: "For institutes just starting AI",
    features: [
      "Basic dashboard",
      "CSV lead upload",
      "Limited AI calls",
      "Call recordings & transcripts"
    ],
    extra: "",
    highlight: false,
    cta: "Start Free Trial"
  },
  {
    name: "Growth Conversion Engine",
    badge: "🔵",
    price: "₹4,999",
    period: "/mo",
    description: "For institutes ready to scale",
    features: [
      "Full AI calling system",
      "WhatsApp integration",
      "Lead tracking + scoring",
      "Booking system",
      "Analytics dashboard"
    ],
    extra: "₹1k–5k per 700 AI call-like-real",
    highlight: true,
    cta: "Start Free Trial"
  },
  {
    name: "Scale AI System",
    badge: "🟣",
    price: "₹9,999+",
    period: "/mo",
    description: "For large institutes & chains",
    features: [
      "Unlimited leads",
      "Priority AI calling",
      "CRM integrations",
      "Dedicated support"
    ],
    extra: "",
    highlight: false,
    cta: "Talk to Sales"
  },
  {
    name: "Done-For-You AI Admissions",
    badge: "🔴",
    price: "₹9,999+",
    period: "/mo",
    description: "For institutes that want full autopilot",
    features: [
      "Fully automated AI pipeline",
      "AI handles full pipeline",
      "Custom call scripts",
      "Priority execution"
    ],
    extra: "",
    highlight: false,
    cta: "Book Strategy Call"
  }
];

export function PricingSection() {
  return (
    <section className="py-24 bg-slate-50 dark:bg-slate-900/50 relative" id="pricing">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <p className="text-[var(--color-brand-purple)] font-bold tracking-wider uppercase text-sm mb-4">Pricing</p>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Pay less than <span className="line-through text-slate-400">one</span> caller. Get a <span className="text-[var(--color-brand-blue)]">whole AI team.</span></h2>
          <p className="text-xl text-slate-600 dark:text-slate-400 mb-6">
            <span className="font-semibold text-slate-900 dark:text-white">Human caller: ₹15,000/mo · AdmitFlow Growth: ₹4,999/mo · Save 67% + get 3x results.</span>
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {plans.map((plan, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1 }}
              className={`relative bg-white dark:bg-slate-900 rounded-3xl p-8 flex flex-col ${
                plan.highlight 
                ? "border-2 border-[var(--color-brand-blue)] shadow-xl shadow-brand-blue/10 scale-105 z-10" 
                : "border border-slate-200 dark:border-slate-800 shadow-sm"
              }`}
            >
              {plan.highlight && (
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2">
                  <span className="bg-gradient-to-r from-[var(--color-brand-purple)] to-[var(--color-brand-blue)] text-white text-xs font-bold px-3 py-1 rounded-full flex items-center gap-1">
                    ⭐ MOST POPULAR
                  </span>
                </div>
              )}
              
              <div className="text-2xl mb-2">{plan.badge}</div>
              <h3 className="text-xl font-semibold mb-2">{plan.name}</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 mb-6 min-h-[40px]">{plan.description}</p>
              
              <div className="mb-6">
                <span className="text-4xl font-bold">{plan.price}</span>
                <span className="text-slate-500 dark:text-slate-400">{plan.period}</span>
              </div>
              
              <button className={`w-full py-3 rounded-full font-semibold transition-all mb-8 ${
                plan.highlight
                ? "bg-gradient-to-r from-[var(--color-brand-purple)] to-[var(--color-brand-blue)] text-white hover:shadow-lg hover:opacity-90"
                : "bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white hover:bg-slate-200 dark:hover:bg-slate-700"
              }`}>
                {plan.cta || "Get Started"}
              </button>
              
              <ul className="space-y-4 mb-8 flex-1">
                {plan.features.map((feature, fIdx) => (
                  <li key={fIdx} className="flex items-start gap-3 text-sm">
                    <Check className={`w-5 h-5 shrink-0 ${plan.highlight ? "text-[var(--color-brand-blue)]" : "text-green-500"}`} />
                    <span className="text-slate-700 dark:text-slate-300">{feature}</span>
                  </li>
                ))}
              </ul>
              
              <div className="pt-6 border-t border-slate-100 dark:border-slate-800 text-xs text-slate-500 dark:text-slate-400 font-medium">
                {plan.extra}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
