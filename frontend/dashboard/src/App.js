import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Joyride, STATUS } from 'react-joyride';
import './App.css';


const COLORS = ['#6366f1', '#475569', '#94a3b8', '#8b5cf6'];

function App() {
  const [summaryData, setSummaryData] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [activeSegment, setActiveSegment] = useState('🟢 Champions');
  const [isUploading, setIsUploading] = useState(false);
  

  // --- ONBOARDING TOUR STATE ---
  const [runTour, setRunTour] = useState(true); 
const steps = [
    {
      target: 'body', // Targets the whole screen
      placement: 'center', // Pops up exactly in the middle!
      content: 'Welcome to the Retail Behavior Engine! Let us give you a quick tour of your new SaaS dashboard.',
      disableBeacon: true,
    },
    {
      target: '.tour-step-2',
      content: 'Start here by uploading your raw E-commerce data (CSV or Excel). Our Machine Learning engine will process it in seconds.',
      disableBeacon: true, // Disabling the beacon here too for a cleaner flow
    },
    {
      target: '.tour-step-3',
      content: 'This chart maps your customers into 4 distinct groups using K-Means clustering. Click any slice to filter the data below!',
      disableBeacon: true,
    },
    {
      target: '.tour-step-4',
      content: 'Here you can view the top customers in your selected segment, ranked by their total lifetime spend.',
      disableBeacon: true,
    },
    {
      target: '.tour-step-5',
      content: 'Ready to launch a marketing campaign? Click here to export this specific list directly to your CRM or email tool.',
      disableBeacon: true,
    }
  ];

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/summary')
      .then(res => res.json())
      .then(data => setSummaryData(data))
      .catch(err => console.error("Error:", err));
  }, []);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/customers?segment=${activeSegment}`)
      .then(res => res.json())
      .then(data => setTableData(data))
      .catch(err => console.error("Error:", err));
  }, [activeSegment]);

  const handleThemeToggle = () => setIsDarkMode(!isDarkMode);
  const onPieClick = (data) => setActiveSegment(data.name);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setIsUploading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/upload', {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();
      
      const summaryRes = await fetch('http://127.0.0.1:8000/api/summary');
      setSummaryData(await summaryRes.json());

      const tableRes = await fetch(`http://127.0.0.1:8000/api/customers?segment=${activeSegment}`);
      setTableData(await tableRes.json());

      alert(`Success! ${result.message}`);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Error uploading file.");
    } finally {
      setIsUploading(false);
    }
  };

  // --- CSV EXPORT LOGIC ---
  const exportToCSV = () => {
    if (tableData.length === 0) return;
    
    const headers = Object.keys(tableData[0]).join(',');
    const rows = tableData.map(obj => Object.values(obj).join(',')).join('\n');
    const csvContent = `${headers}\n${rows}`;
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${cleanTitle}_Customers.csv`;
    a.click();
  };

  const handleJoyrideCallback = (data) => {
    const { status } = data;
    if ([STATUS.FINISHED, STATUS.SKIPPED].includes(status)) {
      setRunTour(false);
    }
  };

  const cleanTitle = activeSegment.replace(/[🟢🔵🟡🔴]/g, '').trim();

  return (
    <div className={`app-wrapper ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      
      <Joyride
        steps={steps}
        run={runTour}
        continuous={true}
        showProgress={true}
        showSkipButton={true}
        callback={handleJoyrideCallback}
        styles={{
          options: {
            primaryColor: '#6366f1',
            backgroundColor: isDarkMode ? '#1e293b' : '#ffffff',
            textColor: isDarkMode ? '#f8fafc' : '#0f172a',
            arrowColor: isDarkMode ? '#1e293b' : '#ffffff',
          }
        }}
      />

      <div className="dashboard-container">
        
        {/* CLEAN, FIXED HEADER SECTION */}
        <div className="header-container">
          <h1 className="tour-step-1" style={{ width: 'fit-content', margin: 0 }}>
            Retail Behavior Engine
          </h1>
          
          <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
            <label className="theme-toggle tour-step-2" style={{ 
              cursor: 'pointer', backgroundColor: 'var(--accent)', color: '#fff', borderColor: 'var(--accent)' 
            }}>
               {isUploading ? '⏳ Uploading...' : '📁 Upload Dataset'}
               <input type="file" accept=".csv" style={{ display: 'none' }} onChange={handleFileUpload} disabled={isUploading}/>
            </label>

            <button className="theme-toggle" onClick={handleThemeToggle}>
              {isDarkMode ? 'Light Mode' : 'Dark Mode'}
            </button>
            
            <button className="theme-toggle" onClick={() => setRunTour(true)} style={{fontSize: '0.75rem'}}>
              Restart Tour 🔄
            </button>
          </div>
        </div>

        <div className="bento-grid">
          
          <div className="bento-box tour-step-3">
            <h3>Segment Distribution</h3>
            <div style={{ height: '350px', cursor: 'pointer' }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={summaryData} dataKey="value" nameKey="name" cx="50%" cy="50%"
                    innerRadius={80} outerRadius={110} paddingAngle={2} onClick={onPieClick} 
                  >
                    {summaryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} opacity={activeSegment === entry.name ? 1 : 0.6} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: isDarkMode ? '#1e293b' : '#ffffff', borderColor: isDarkMode ? '#334155' : '#e2e8f0', color: isDarkMode ? '#f8fafc' : '#0f172a', borderRadius: '8px' }}/>
                  <Legend verticalAlign="bottom" height={36} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bento-box tour-step-4">
            <h3 style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>Top 10: {cleanTitle}</span>
              
              <button className="export-btn tour-step-5" onClick={exportToCSV}>
                Download CSV ⬇️
              </button>
            </h3>

            <table className="cyber-table">
              <thead>
                <tr>
                  <th>Customer ID</th>
                  <th>Recency (Days)</th>
                  <th>Frequency (Orders)</th>
                  <th>Total Spend</th>
                </tr>
              </thead>
              <tbody>
                {tableData.slice(0, 10).map((customer) => (
                  <tr key={customer.CustomerID}>
                    <td>#{customer.CustomerID}</td>
                    <td>{customer.Recency}</td>
                    <td>{customer.Frequency}</td>
                    <td className="highlight-spend">
                      ${customer.Monetary.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>
      </div>
      
    </div>
  );
}

export default App;