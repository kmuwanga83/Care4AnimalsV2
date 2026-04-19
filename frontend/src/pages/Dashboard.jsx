import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Users, Activity, Globe, MessageSquare, ArrowRight, ShieldCheck } from 'lucide-react';

const COLORS = ['#2E5B96', '#4CAF50', '#F2994A', '#EB5757'];

const Dashboard = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/analytics/summary')
      .then(res => res.json())
      .then(json => setData(json))
      .catch(err => console.error("Sync Error:", err));
  }, []);

  if (!data) return <div className="min-h-screen flex items-center justify-center bg-[#F4F7FA] font-bold text-[#2E5B96]">Loading Care4Animals Analytics...</div>;

  return (
    <div className="min-h-screen bg-[#F4F7FA] font-sans">
      {/* 1. BRANDED HEADER (Matches Mobile UI) */}
      <header className="bg-[#2E5B96] text-white px-8 py-6 shadow-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="bg-white p-2 rounded-full shadow-inner">
               <img src="/bugema_logo.png" alt="Logo" className="h-10 w-auto" />
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tight">CARE4ANIMALS</h1>
              <p className="text-xs font-medium opacity-80 uppercase tracking-[0.2em]">Management & Analytics Portal</p>
            </div>
          </div>
          <div className="flex items-center space-x-2 bg-white/10 px-4 py-2 rounded-xl border border-white/20">
            <ShieldCheck size={18} className="text-green-400" />
            <span className="text-sm font-bold uppercase">Admin Verified</span>
          </div>
        </div>
      </header>

      <main className="p-8 max-w-7xl mx-auto -mt-8">
        {/* 2. INTUITIVE COMMAND CARDS (Metaphor-based UI) */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
          <ActionCard title="SMS Traffic" value={data.metrics.total_interactions} icon={<MessageSquare />} color="blue" />
          <ActionCard title="Registered Farmers" value={data.metrics.active_users} icon={<Users />} color="green" />
          <ActionCard title="Lesson Requests" value={data.metrics.lesson_requests} icon={<Activity />} color="orange" />
          <ActionCard title="Languages" value={Object.keys(data.language_stats).length} icon={<Globe />} color="red" />
        </div>

        {/* 3. AESTHETIC ANALYTICS (Component-based Interface) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
            <div className="bg-slate-50 px-8 py-4 border-b border-slate-100 flex justify-between items-center">
              <h2 className="font-black text-slate-800 uppercase text-sm tracking-widest">Engagement Trends</h2>
              <span className="text-[10px] bg-blue-100 text-blue-700 px-2 py-1 rounded-md font-bold">LIVE DATA</span>
            </div>
            <div className="p-8 h-[350px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data.trends.length > 0 ? data.trends : [{date: '---', count: 0}]}>
                  <defs>
                    <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#2E5B96" stopOpacity={0.2}/>
                      <stop offset="95%" stopColor="#2E5B96" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                  <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{fontSize: 12, fontWeight: 600, fill: '#64748B'}} />
                  <YAxis axisLine={false} tickLine={false} tick={{fontSize: 12, fontWeight: 600, fill: '#64748B'}} />
                  <Tooltip contentStyle={{borderRadius: '15px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)'}} />
                  <Area type="monotone" dataKey="count" stroke="#2E5B96" strokeWidth={4} fillOpacity={1} fill="url(#colorCount)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
            <div className="bg-slate-50 px-8 py-4 border-b border-slate-100">
              <h2 className="font-black text-slate-800 uppercase text-sm tracking-widest">Language Split</h2>
            </div>
            <div className="p-8 h-[350px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie 
                    data={Object.keys(data.language_stats).map(k => ({name: k.toUpperCase(), value: data.language_stats[k]}))} 
                    innerRadius={70} outerRadius={100} paddingAngle={5} dataKey="value"
                  >
                    {COLORS.map((color, i) => <Cell key={i} fill={color} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="mt-4 flex justify-center space-x-4">
                 {/* Feedback: Legend for easy learning */}
                 <div className="flex items-center space-x-1"><div className="w-3 h-3 rounded-full bg-[#2E5B96]"/><span className="text-[10px] font-bold">EN</span></div>
                 <div className="flex items-center space-x-1"><div className="w-3 h-3 rounded-full bg-[#4CAF50]"/><span className="text-[10px] font-bold">LG</span></div>
                 <div className="flex items-center space-x-1"><div className="w-3 h-3 rounded-full bg-[#F2994A]"/><span className="text-[10px] font-bold">SW</span></div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

// Component-based card for Speed of Learning
const ActionCard = ({ title, value, icon, color }) => {
  const colorMap = {
    blue: "bg-[#2E5B96]",
    green: "bg-[#4CAF50]",
    orange: "bg-[#F2994A]",
    red: "bg-[#EB5757]"
  };

  return (
    <div className={`${colorMap[color]} p-6 rounded-3xl shadow-lg text-white flex flex-col justify-between h-40 transition-transform hover:scale-[1.03] cursor-default`}>
      <div className="flex justify-between items-start">
        <div className="bg-white/20 p-2 rounded-xl backdrop-blur-sm">
          {React.cloneElement(icon, { size: 24 })}
        </div>
        <ArrowRight size={16} className="opacity-40" />
      </div>
      <div>
        <p className="text-sm font-bold opacity-80 uppercase tracking-tighter mb-1">{title}</p>
        <p className="text-4xl font-black">{value}</p>
      </div>
    </div>
  );
};

export default Dashboard;