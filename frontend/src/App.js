import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SecureIdentityBanner from './components/SecureIdentityBanner';
import MetricsDashboard from './components/MetricsDashboard';
import DemoPage from './pages/DemoPage';
import AnswerPage from './pages/AnswerPage';

function App() {
    return (
        <Router>
            <div className="App">
                <SecureIdentityBanner />
                <Routes>
                    <Route path="/" element={<DemoPage />} />
                    <Route path="/dashboard" element={<MetricsDashboard />} />
                    <Route path="/answer" element={<AnswerPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
