"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Users, PhoneCall, CheckCircle, Search, Bell, Settings, MoreVertical, LogOut, User, MessageSquare, CreditCard, Key, HelpCircle } from "lucide-react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import Link from "next/link";
import { ThemeToggle } from "@/components/ThemeToggle";

const data = [
  { name: "Mon", calls: 4000, conversions: 2400 },
  { name: "Tue", calls: 3000, conversions: 1398 },
  { name: "Wed", calls: 2000, conversions: 9800 },
  { name: "Thu", calls: 2780, conversions: 3908 },
  { name: "Fri", calls: 1890, conversions: 4800 },
  { name: "Sat", calls: 2390, conversions: 3800 },
  { name: "Sun", calls: 3490, conversions: 4300 },
];

const leads = [
  { id: 1, name: "Rahul Sharma", course: "B.Tech Computer Science", status: "Hot", lastContact: "2 hours ago", aiScore: 92 },
  { id: 2, name: "Priya Singh", course: "MBA Marketing", status: "Follow up", lastContact: "5 hours ago", aiScore: 78 },
  { id: 3, name: "Amit Patel", course: "B.Sc Data Science", status: "Converted", lastContact: "1 day ago", aiScore: 99 },
  { id: 4, name: "Sneha Gupta", course: "B.A. Economics", status: "Cold", lastContact: "2 days ago", aiScore: 45 },
];

export default function DashboardPage() {
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#020617] flex font-[family-name:var(--font-sans)]">
      
      {/* Sidebar */}
      <aside className="w-64 bg-white dark:bg-[#0f172a] border-r border-slate-200 dark:border-slate-800 hidden lg:flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-slate-200 dark:border-slate-800">
          <Link href="/" className="font-bold text-xl tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-brand-purple)] to-[var(--color-brand-cyan)]">AdmitFlow</Link>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          <a href="#" className="flex items-center gap-3 px-3 py-2 bg-[var(--color-brand-blue)]/10 text-[var(--color-brand-blue)] rounded-lg font-medium">
            <Settings className="w-5 h-5" /> Dashboard
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50 rounded-lg font-medium transition-colors">
            <Users className="w-5 h-5" /> Leads
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50 rounded-lg font-medium transition-colors">
            <PhoneCall className="w-5 h-5" /> Call Logs
          </a>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        
        {/* Topbar */}
        <header className="h-16 bg-white dark:bg-[#0f172a] border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-6 shrink-0">
          <div className="flex items-center gap-4 flex-1">
            <div className="relative w-full max-w-md hidden sm:block">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input 
                type="text" 
                placeholder="Search leads, transcripts..." 
                className="w-full pl-10 pr-4 py-2 bg-slate-100 dark:bg-slate-800 border-none rounded-full text-sm focus:ring-2 focus:ring-[var(--color-brand-blue)] outline-none"
              />
            </div>
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <button className="relative p-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full" />
            </button>
            <div className="relative">
              <button 
                onClick={() => setIsProfileOpen(!isProfileOpen)}
                className="w-8 h-8 flex rounded-full bg-gradient-to-r from-[var(--color-brand-purple)] to-[var(--color-brand-cyan)] border-2 border-white dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-blue)] focus:ring-offset-2 dark:focus:ring-offset-[#0f172a] transition-all cursor-pointer shadow-sm hover:shadow-md"
                aria-label="User profile options"
              />
              <AnimatePresence>
                {isProfileOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: 10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 10, scale: 0.95 }}
                    transition={{ duration: 0.15 }}
                    className="absolute right-0 mt-3 w-56 origin-top-right bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-50 overflow-hidden"
                  >
                    <div className="p-3 border-b border-slate-200 dark:border-slate-800">
                      <p className="text-sm font-medium text-slate-900 dark:text-white">Admin User</p>
                      <p className="text-xs text-slate-500 dark:text-slate-400 truncate">admin@institute.edu</p>
                    </div>
                    <div className="p-1">
                      <a href="#" className="flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/60 rounded-lg transition-colors">
                        <User className="w-4 h-4 text-slate-500 dark:text-slate-400 text-opacity-80" /> Profile Update
                      </a>
                      <a href="#" className="flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/60 rounded-lg transition-colors">
                        <Settings className="w-4 h-4 text-slate-500 dark:text-slate-400 text-opacity-80" /> Account Settings
                      </a>
                      <a href="#" className="flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/60 rounded-lg transition-colors">
                        <MessageSquare className="w-4 h-4 text-[#25D366]" /> WhatsApp Integration
                      </a>
                      <a href="#" className="flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/60 rounded-lg transition-colors">
                        <CreditCard className="w-4 h-4 text-slate-500 dark:text-slate-400 text-opacity-80" /> Billing & Plans
                      </a>
                      <a href="#" className="flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/60 rounded-lg transition-colors">
                        <Key className="w-4 h-4 text-slate-500 dark:text-slate-400 text-opacity-80" /> API Keys
                      </a>
                      <a href="#" className="flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/60 rounded-lg transition-colors">
                        <HelpCircle className="w-4 h-4 text-slate-500 dark:text-slate-400 text-opacity-80" /> Help & Support
                      </a>
                    </div>
                    <div className="p-1 border-t border-slate-200 dark:border-slate-800">
                      <Link 
                        href="/login"
                        onClick={() => setIsProfileOpen(false)}
                        className="flex w-full items-center gap-2 px-3 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                      >
                        <LogOut className="w-4 h-4" /> Logout
                      </Link>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <div className="flex-1 overflow-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            
            <div className="flex justify-between items-end">
              <div>
                <h1 className="text-2xl font-bold mb-1">Overview</h1>
                <p className="text-slate-500 text-sm">Track your AI admission performance.</p>
              </div>
              <button className="hidden sm:block px-4 py-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 text-sm font-medium rounded-lg hover:opacity-90">
                Export Report
              </button>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                { title: "Total Leads", value: "12,450", trend: "+12%", icon: Users, color: "text-blue-500", bg: "bg-blue-500/10" },
                { title: "AI Calls Made", value: "8,234", trend: "+24%", icon: PhoneCall, color: "text-purple-500", bg: "bg-purple-500/10" },
                { title: "Admissions Converted", value: "1,102", trend: "+8%", icon: CheckCircle, color: "text-green-500", bg: "bg-green-500/10" }
              ].map((kpi, i) => (
                <motion.div key={i} initial={{opacity:0, y:20}} animate={{opacity:1, y:0}} transition={{delay: i*0.1}} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 flex flex-col justify-between shadow-sm">
                  <div className="flex justify-between items-start mb-4">
                    <div className={`p-3 rounded-xl ${kpi.bg}`}>
                      <kpi.icon className={`w-6 h-6 ${kpi.color}`} />
                    </div>
                    <span className="text-sm font-medium text-green-500 bg-green-500/10 px-2 py-1 rounded-md">{kpi.trend}</span>
                  </div>
                  <div>
                    <h3 className="text-3xl font-bold mb-1">{kpi.value}</h3>
                    <p className="text-sm text-slate-500 font-medium">{kpi.title}</p>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Chart Area */}
            <motion.div initial={{opacity:0, y:20}} animate={{opacity:1, y:0}} transition={{delay: 0.3}} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-bold mb-6">Call Performance vs Conversions</h3>
              <div className="h-[300px] w-full min-h-[300px]">
                <ResponsiveContainer width="100%" height="100%" minHeight={300}>
                  <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorCalls" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="var(--color-brand-blue)" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="var(--color-brand-blue)" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorConversions" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="var(--color-brand-cyan)" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="var(--color-brand-cyan)" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" opacity={0.2} />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} dy={10} />
                    <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} dx={-10} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px', color: '#fff' }}
                      itemStyle={{ color: '#fff' }}
                    />
                    <Area type="monotone" dataKey="calls" stroke="var(--color-brand-blue)" strokeWidth={2} fillOpacity={1} fill="url(#colorCalls)" />
                    <Area type="monotone" dataKey="conversions" stroke="var(--color-brand-cyan)" strokeWidth={2} fillOpacity={1} fill="url(#colorConversions)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </motion.div>

            {/* Table Area */}
            <motion.div initial={{opacity:0, y:20}} animate={{opacity:1, y:0}} transition={{delay: 0.4}} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm overflow-hidden">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-bold">Recent Leads Activity</h3>
                <button className="text-sm text-[var(--color-brand-blue)] font-medium">View All</button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm whitespace-nowrap">
                  <thead>
                    <tr className="text-slate-500 border-b border-slate-200 dark:border-slate-800">
                      <th className="pb-3 font-medium">Lead Name</th>
                      <th className="pb-3 font-medium">Course Interested</th>
                      <th className="pb-3 font-medium">Status</th>
                      <th className="pb-3 font-medium">AI Score</th>
                      <th className="pb-3 font-medium">Last Contact</th>
                      <th className="pb-3 font-medium"></th>
                    </tr>
                  </thead>
                  <tbody>
                    {leads.map((lead) => (
                      <tr key={lead.id} className="border-b border-slate-100 dark:border-slate-800/50 last:border-0 hover:bg-slate-50 dark:hover:bg-slate-800/20">
                        <td className="py-4 font-medium">{lead.name}</td>
                        <td className="py-4 text-slate-500">{lead.course}</td>
                        <td className="py-4">
                          <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                            lead.status === 'Hot' ? 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400' :
                            lead.status === 'Converted' ? 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400' :
                            lead.status === 'Follow up' ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' :
                            'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
                          }`}>
                            {lead.status}
                          </span>
                        </td>
                        <td className="py-4">
                          <div className="flex items-center gap-2">
                            <div className="w-16 h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                              <div className="h-full bg-[var(--color-brand-purple)] rounded-full" style={{width: `${lead.aiScore}%`}} />
                            </div>
                            <span className="font-medium text-xs">{lead.aiScore}</span>
                          </div>
                        </td>
                        <td className="py-4 text-slate-500">{lead.lastContact}</td>
                        <td className="py-4 text-right">
                          <button className="p-1 hover:bg-slate-100 dark:hover:bg-slate-800 rounded">
                            <MoreVertical className="w-4 h-4 text-slate-400" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </motion.div>

          </div>
        </div>
      </main>
    </div>
  );
}
