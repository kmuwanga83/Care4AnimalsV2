import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Activity, BookOpen, Globe, ShieldCheck } from 'lucide-react';

const AdminDashboard = () => {
  const [data, setData] = useState([]);
  const [isOnline, setIsOnline] = useState(false);

  // Constants for branding
  const NAVY = "#2E5B96";
  const EMERALD = "#4CAF50";

  useEffect(() => {
    // Fetch counts from your backend summary endpoint
    const fetchStats = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/lessons/summary');
        const result = await response.json();
        
        // Transform API data for Recharts
        // Expected result: { "en": 136, "lg": 136, "sw": 136 }
        const chartMapped = Object.keys(result).map(key => ({
          name: key.toUpperCase(),
          value: result[key]
        }));
        
        setData(chartMapped);
        setIsOnline(true);
      } catch (error) {
        console.error("Backend unreachable", error);
        setIsOnline(false);
      }
    };

    fetchStats();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      {/* HEADER WITH LOGOS */}
      <header className="flex justify-between items-center mb-8 bg-white p-4 rounded-xl shadow-sm border-b-4 border-[#4CAF50]">
        <div className="flex items-center gap-3">
          <img src="/bugema_logo.png" alt="Bugema University" className="h-12 w-auto" />
          <div className="h-8 w-px bg-gray-200 mx-2" />
          <img src="/wts_logo.png" alt="WTS" className="h-10 w-auto" />
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right hidden md:block">
            <p className="text-xs font-bold text-gray-500 uppercase">System Pulse</p>
            <p className={`text-sm font-medium ${isOnline ? 'text-emerald-600' : 'text-red-500'}`}>
              {isOnline ? 'BACKEND ONLINE' : 'DISCONNECTED'}
            </p>
          </div>
          <div className={`h-3 w-3 rounded-full ${isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`} />
        </div>
      </header>

      {/* STAT CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-2xl shadow-sm border-l-8 border-[#2E5B96]">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-50 rounded-lg text-[#2E5B96]"><BookOpen /></div>
            <div>
              <p className="text-sm text-gray-500 font-bold">TOTAL LESSONS</p>
              <p className="text-3xl font-black text-gray-800">408</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-2xl shadow-sm border-l-8 border-[#4CAF50]">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-50 rounded-lg text-[#4CAF50]"><Globe /></div>
            <div>
              <p className="text-sm text-gray-500 font-bold">LANGUAGES</p>
              <p className="text-3xl font-black text-gray-800">3</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border-l-8 border-yellow-500">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-50 rounded-lg text-yellow-600"><Activity /></div>
            <div>
              <p className="text-sm text-gray-500 font-bold">RECOVERY STATUS</p>
              <p className="text-3xl font-black text-gray-800">100%</p>
            </div>
          </div>
        </div>
      </div>

      {/* CHART SECTION */}
      <div className="bg-white p-6 rounded-2xl shadow-sm">
        <h3 className="text-xl font-bold mb-6 text-[#2E5B96]">Curriculum Distribution by Language</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" axisLine={false} tickLine={false} />
              <YAxis axisLine={false} tickLine={false} />
              <Tooltip cursor={{fill: '#f3f4f6'}} />
              <Bar dataKey="value" radius={[4, 4, 0, 0]} barSize={60}>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index % 2 === 0 ? NAVY : EMERALD} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;