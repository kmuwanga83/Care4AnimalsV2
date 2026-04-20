import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Activity, BookOpen, Globe, Filter } from 'lucide-react';

const AdminDashboard = () => {
  const [rawStats, setRawStats] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [selectedLang, setSelectedLang] = useState('ALL');
  const [isOnline, setIsOnline] = useState(false);

  // Branding Constants
  const NAVY = "#2E5B96";
  const EMERALD = "#4CAF50";
  const AMBER = "#F59E0B";

  const COLORS: Record<string, string> = {
    EN: NAVY,
    LG: EMERALD,
    SW: AMBER,
    ALL: "#6366F1"
  };

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Achievement: Pointing to the unified analytics/summary endpoint
        const response = await fetch('http://localhost:8000/analytics/summary');
        const result = await response.json();
        
        setRawStats(result);
        
        // Transform full stats for the default view
        const chartMapped = Object.keys(result.language_stats).map(key => ({
          name: key.toUpperCase(),
          value: result.language_stats[key]
        }));
        
        setChartData(chartMapped);
        setIsOnline(true);
      } catch (error) {
        console.error("Backend unreachable", error);
        setIsOnline(false);
      }
    };

    fetchStats();
  }, []);

  // Achievement: Real-time filtering logic
  const handleFilterChange = (lang: string) => {
    setSelectedLang(lang);
    if (!rawStats) return;

    if (lang === 'ALL') {
      const allData = Object.keys(rawStats.language_stats).map(key => ({
        name: key.toUpperCase(),
        value: rawStats.language_stats[key]
      }));
      setChartData(allData);
    } else {
      const key = lang.toLowerCase();
      setChartData([{
        name: lang,
        value: rawStats.language_stats[key]
      }]);
    }
  };

  if (!rawStats && isOnline) return <div className="p-10 text-center font-bold">Initializing Dashboard...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      {/* HEADER */}
      <header className="flex flex-col md:flex-row justify-between items-center mb-8 bg-white p-4 rounded-xl shadow-sm border-b-4 border-[#4CAF50] gap-4">
        <div className="flex items-center gap-3">
          <img src="/bugema_logo.png" alt="Bugema University" className="h-10 w-auto" />
          <div className="h-8 w-px bg-gray-200 mx-2" />
          <img src="/wts_logo.png" alt="WTS" className="h-8 w-auto" />
        </div>

        {/* INTERACTIVE CONTROLS */}
        <div className="flex items-center gap-2 bg-gray-50 p-1.5 rounded-lg border border-gray-100">
          <Filter size={16} className="text-gray-400 ml-2" />
          {['ALL', 'EN', 'LG', 'SW'].map((lang) => (
            <button
              key={lang}
              onClick={() => handleFilterChange(lang)}
              className={`px-4 py-1.5 rounded-md text-xs font-bold transition-all ${
                selectedLang === lang 
                ? 'bg-white text-[#2E5B96] shadow-sm border border-gray-200' 
                : 'text-gray-500 hover:bg-gray-100'
              }`}
            >
              {lang}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-4">
          <div className={`h-3 w-3 rounded-full ${isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`} />
          <p className={`text-xs font-bold ${isOnline ? 'text-emerald-600' : 'text-red-500'}`}>
            {isOnline ? 'SYSTEM ACTIVE' : 'DISCONNECTED'}
          </p>
        </div>
      </header>

      {/* STAT CARDS - ACHIEVEMENT: Now dynamic based on filter */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-2xl shadow-sm border-l-8 border-[#2E5B96]">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-50 rounded-lg text-[#2E5B96]"><BookOpen /></div>
            <div>
              <p className="text-xs text-gray-500 font-bold uppercase tracking-wider">Lessons ({selectedLang})</p>
              <p className="text-3xl font-black text-gray-800">
                {selectedLang === 'ALL' ? rawStats?.metrics.total_lessons : rawStats?.language_stats[selectedLang.toLowerCase()]}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-2xl shadow-sm border-l-8 border-[#4CAF50]">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-50 rounded-lg text-[#4CAF50]"><Globe /></div>
            <div>
              <p className="text-xs text-gray-500 font-bold uppercase tracking-wider">Scope</p>
              <p className="text-3xl font-black text-gray-800">{selectedLang === 'ALL' ? 'Multilingual' : 'Regional'}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border-l-8 border-yellow-500">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-50 rounded-lg text-yellow-600"><Activity /></div>
            <div>
              <p className="text-xs text-gray-500 font-bold uppercase tracking-wider">Data Sync</p>
              <p className="text-3xl font-black text-gray-800">Verified</p>
            </div>
          </div>
        </div>
      </div>

      {/* CHART SECTION */}
      <div className="bg-white p-8 rounded-2xl shadow-sm">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-black text-[#2E5B96]">Curriculum Distribution</h3>
          <span className="text-xs font-bold px-3 py-1 bg-gray-100 rounded-full text-gray-600">
            Current Filter: {selectedLang}
          </span>
        </div>
        
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
              <XAxis 
                dataKey="name" 
                axisLine={false} 
                tickLine={false} 
                tick={{fill: '#9ca3af', fontSize: 12, fontWeight: 700}}
              />
              <YAxis 
                axisLine={false} 
                tickLine={false} 
                tick={{fill: '#9ca3af', fontSize: 12}}
              />
              <Tooltip 
                cursor={{fill: '#f9fafb'}} 
                contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)'}}
              />
              <Bar dataKey="value" radius={[6, 6, 0, 0]} barSize={selectedLang === 'ALL' ? 60 : 120}>
                {chartData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={COLORS[entry.name] || NAVY} 
                  />
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