import Link from "next/link";
import { Sparkles, Globe, Mail, MessageSquare } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-slate-50 dark:bg-slate-950 pt-16 pb-8 border-t border-slate-200 dark:border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-start gap-8 mb-12">
          
          {/* Brand */}
          <div className="max-w-sm">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <div className="p-1 rounded-md bg-gradient-to-br from-[var(--color-brand-purple)] to-[var(--color-brand-cyan)]">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <span className="font-bold text-xl tracking-tight">AdmitFlow</span>
            </Link>
            <p className="text-slate-500 dark:text-slate-400 mb-6">
              The AI admission team that calls, follows up, and converts students like you.
            </p>
            <div className="flex items-center gap-4 text-slate-400">
              <a href="#" className="hover:text-[var(--color-brand-blue)] transition-colors"><Globe className="w-5 h-5" /></a>
              <a href="#" className="hover:text-[var(--color-brand-blue)] transition-colors"><Mail className="w-5 h-5" /></a>
              <a href="#" className="hover:text-[var(--color-brand-blue)] transition-colors"><MessageSquare className="w-5 h-5" /></a>
            </div>
          </div>
          
          {/* Links */}
          <div className="md:mt-4">
            <ul className="flex flex-wrap gap-6 text-sm font-medium text-slate-600 dark:text-slate-400">
              <li><Link href="#features" className="hover:text-[var(--color-brand-blue)] transition-colors">Features</Link></li>
              <li><Link href="#pricing" className="hover:text-[var(--color-brand-blue)] transition-colors">Pricing</Link></li>
              <li><Link href="#workflow" className="hover:text-[var(--color-brand-blue)] transition-colors">Workflow</Link></li>
              <li><Link href="/dashboard" className="hover:text-[var(--color-brand-blue)] transition-colors">Dashboard</Link></li>
              <li><Link href="#" className="hover:text-[var(--color-brand-blue)] transition-colors">Integrations</Link></li>
            </ul>
          </div>
          
        </div>
        
        <div className="pt-8 border-t border-slate-200 dark:border-slate-800 text-center flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-slate-500">
          <p>© 2026 AdmitFlow. All rights reserved.</p>
          <p>Built with intelligence.</p>
        </div>
      </div>
    </footer>
  );
}
