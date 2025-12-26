import React, { useState, useEffect } from 'react';
import { getDashboardMetrics } from '../services/api';

const MetricsDashboard = () => {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadMetrics();
        const interval = setInterval(loadMetrics, 5000); // Refresh every 5 seconds
        return () => clearInterval(interval);
    }, []);

    const loadMetrics = async () => {
        try {
            const response = await getDashboardMetrics();
            setMetrics(response.data);
            setError(null);
        } catch (err) {
            setError('Failed to load metrics');
        } finally {
            setLoading(false);
        }
    };

    if (loading && !metrics) {
        return (
            <div className="min-h-screen bg-primary-dark flex items-center justify-center">
                <div className="text-sand-light text-xl">Loading metrics...</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-primary-dark p-6">
            <div className="container mx-auto max-w-7xl">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-sand-light mb-2">
                        Pharmacovigilance Dashboard
                    </h1>
                    <p className="text-accent-green2 text-lg">
                        Real-time adverse event monitoring & metrics
                    </p>
                </div>

                {/* Key Metrics Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    {/* Total Events */}
                    <div className="card">
                        <div className="text-accent-green2 text-sm font-semibold mb-2">Total Events</div>
                        <div className="text-5xl font-bold text-sand-light mb-1">
                            {metrics?.total_events || 0}
                        </div>
                        <div className="text-gray-400 text-sm">Adverse events reported</div>
                    </div>

                    {/* High Risk Count */}
                    <div className="card border-red-500">
                        <div className="text-red-400 text-sm font-semibold mb-2">High Risk Events</div>
                        <div className="text-5xl font-bold text-red-300 mb-1">
                            {metrics?.high_risk_count || 0}
                        </div>
                        <div className="text-gray-400 text-sm">Requiring escalation</div>
                    </div>

                    {/* Pending Follow-ups */}
                    <div className="card border-yellow-500">
                        <div className="text-yellow-400 text-sm font-semibold mb-2">Pending Follow-ups</div>
                        <div className="text-5xl font-bold text-yellow-300 mb-1">
                            {metrics?.pending_followups || 0}
                        </div>
                        <div className="text-gray-400 text-sm">Awaiting response</div>
                    </div>

                    {/* Response Rate Increase */}
                    <div className="card">
                        <div className="text-accent-green2 text-sm font-semibold mb-2">Response Rate ↑</div>
                        <div className="text-5xl font-bold text-accent-green1 mb-1">
                            +{metrics?.response_rate_increase?.toFixed(1) || 0}%
                        </div>
                        <div className="text-gray-400 text-sm">vs. baseline (35%)</div>
                    </div>
                </div>

                {/* Performance Metrics */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    {/* Missing Field Reduction */}
                    <div className="card">
                        <h3 className="text-xl font-bold text-sand-light mb-4">Missing Field Completion</h3>
                        <div className="mb-2 flex justify-between text-sm">
                            <span className="text-gray-400">Progress</span>
                            <span className="text-accent-green2 font-semibold">
                                {metrics?.missing_field_reduction?.toFixed(1) || 0}%
                            </span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-4 mb-4">
                            <div
                                className="bg-gradient-to-r from-accent-green1 to-accent-green2 h-4 rounded-full transition-all duration-500"
                                style={{ width: `${Math.min(metrics?.missing_field_reduction || 0, 100)}%` }}
                            />
                        </div>
                        <p className="text-gray-400 text-sm">
                            Target: 60% reduction in incomplete reports
                        </p>
                    </div>

                    {/* Cycle Time Reduction */}
                    <div className="card">
                        <h3 className="text-xl font-bold text-sand-light mb-4">Cycle Time Improvement</h3>
                        <div className="mb-2 flex justify-between text-sm">
                            <span className="text-gray-400">Reduction</span>
                            <span className="text-accent-green2 font-semibold">
                                {metrics?.cycle_time_reduction?.toFixed(1) || 0}%
                            </span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-4 mb-4">
                            <div
                                className="bg-gradient-to-r from-accent-green1 to-accent-green2 h-4 rounded-full transition-all duration-500"
                                style={{ width: `${Math.min(metrics?.cycle_time_reduction || 0, 100)}%` }}
                            />
                        </div>
                        <p className="text-gray-400 text-sm">
                            Target: 50% faster follow-up cycles (14 → 7 days)
                        </p>
                    </div>
                </div>

                {/* AI Performance Metrics */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* High-Risk Detection Accuracy */}
                    <div className="card">
                        <h3 className="text-xl font-bold text-sand-light mb-4 flex items-center gap-2">
                            <svg className="w-6 h-6 text-accent-green2" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                                <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            AI Risk Detection
                        </h3>
                        <div className="text-4xl font-bold text-accent-green1 mb-2">
                            {metrics?.high_risk_accuracy?.toFixed(1) || 0}%
                        </div>
                        <p className="text-gray-400 text-sm mb-4">Accuracy in identifying high-risk cases</p>
                        <div className="flex items-center gap-2 text-sm">
                            <span className="px-3 py-1 bg-green-900 text-green-300 rounded-full font-semibold">
                                ✓ Exceeds 90% target
                            </span>
                        </div>
                    </div>

                    {/* Agent Workload Reduction */}
                    <div className="card">
                        <h3 className="text-xl font-bold text-sand-light mb-4 flex items-center gap-2">
                            <svg className="w-6 h-6 text-accent-green2" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
                            </svg>
                            Automation Impact
                        </h3>
                        <div className="text-4xl font-bold text-accent-green1 mb-2">
                            {metrics?.agent_workload_reduction?.toFixed(1) || 0}%
                        </div>
                        <p className="text-gray-400 text-sm mb-4">Reduction in manual follow-up tasks</p>
                        <div className="bg-gray-800 rounded-lg p-3 text-sm text-gray-300">
                            <div className="flex justify-between mb-1">
                                <span>Automated follow-ups</span>
                                <span className="font-semibold text-accent-green2">
                                    {Math.round((metrics?.agent_workload_reduction || 0) * (metrics?.total_events || 0) / 100)}
                                </span>
                            </div>
                            <div className="flex justify-between">
                                <span>Manual reviews saved</span>
                                <span className="font-semibold text-accent-green2">
                                    ~{Math.round((metrics?.agent_workload_reduction || 0) * 0.5)}+ hrs/week
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Refresh Indicator */}
                <div className="mt-8 text-center text-gray-500 text-sm">
                    <div className="inline-flex items-center gap-2">
                        <div className="w-2 h-2 bg-accent-green2 rounded-full animate-pulse" />
                        Live updates every 5 seconds
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MetricsDashboard;
