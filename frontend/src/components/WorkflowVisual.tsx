"use client";

import { motion } from "framer-motion";
import { Users, Bot, MessageCircle, Send, GraduationCap, ChevronRight } from "lucide-react";

export function WorkflowVisual() {
  const steps = [
    { icon: Users, label: "Leads", desc: "Upload or auto-sync any leads" },
    { icon: Bot, label: "AI Call", desc: "AI calls & qualifies instantly" },
    { icon: MessageCircle, label: "Follow-up", desc: "WhatsApp/SMS follow-ups" },
    { icon: Send, label: "Booking", desc: "Counselling sessions booked" },
    { icon: GraduationCap, label: "Admission", desc: "Student admitted successfully" },
  ];

  return (
    <section className="py-24 relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center" id="workflow">
        <p className="text-[var(--color-brand-purple)] font-bold tracking-wider uppercase text-sm mb-4">How it works</p>
        <h2 className="text-3xl md:text-5xl font-bold mb-16">From lead to admission — <span className="text-[var(--color-brand-blue)]">on autopilot.</span></h2>
        
        <div className="relative max-w-5xl mx-auto">
          {/* Connecting Line */}
          <div className="hidden md:block absolute top-[40px] left-8 right-8 h-1 bg-slate-200 dark:bg-slate-800 -z-10" />
          
          <div className="flex flex-col md:flex-row justify-between items-center gap-8 md:gap-4 relative z-10">
            {steps.map((step, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.2 }}
                className="flex flex-col items-center relative"
              >
                <div className={`w-20 h-20 rounded-full flex items-center justify-center mb-4 transition-transform hover:scale-110 shadow-lg ${
                  idx === steps.length - 1 
                  ? "bg-gradient-to-r from-[var(--color-brand-blue)] to-[var(--color-brand-cyan)] text-white shadow-[var(--color-brand-cyan)]/30" 
                  : "bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 text-[var(--color-brand-purple)]"
                }`}>
                  <step.icon className={`w-8 h-8 ${idx === steps.length - 1 ? "text-white" : ""}`} />
                </div>
                
                <h4 className="font-bold text-lg mb-1">{step.label}</h4>
                <p className="text-sm text-slate-500 font-medium">{step.desc}</p>

                {/* Arrow for mobile, handled by flex-col gap above, but let's add an explicit one here or skip */}
                {idx < steps.length - 1 && (
                  <div className="md:hidden mt-6 text-slate-300 dark:text-slate-700">
                    <ChevronRight className="w-8 h-8 rotate-90" />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
