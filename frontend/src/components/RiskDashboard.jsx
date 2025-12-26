import React, { useState } from 'react';

const RiskDashboard = ({ event }) => {
    if (!event) return null;

    const getRiskColor = (riskClass) => {
        switch (riskClass?.toLowerCase()) {
            case 'low':
                return 'text-green-400 border-green-500';
            case 'medium':
                return 'text-yellow-400 border-yellow-500';
            case 'high':
                return 'text-orange-400 border-orange-500';
            case 'critical':
                return 'text-red-400 border-red-500  animate-pulse';
            default:
                return 'text-gray-400 border-gray-500';
        }
    };

    const getRiskBgColor = (riskClass) => {
        switch (riskClass?.toLowerCase()) {
            case 'low':
                return 'bg-green-900';
            case 'medium':
                return 'bg-yellow-900';
            case 'high':
                return 'bg-orange-900';
            case 'critical':
                return 'bg-red-900';
            default:
                return 'bg-gray-900';
        }
    };

    const riskPercentage = event.risk_score || 0;
    const hospitalizationRisk = (event.hospitalization_risk || 0) * 100;
    const mortalityRisk = (event.mortality_risk || 0) * 100;

    return (
        <div className={`card ${getRiskColor(event.risk_class)}`}>
            {/* Header */}
            <div className="flex justify-between items-start mb-6">
                <div>
                    <h3 className="text-2xl font-bold text-sand-light mb-1">Risk Assessment</h3>
                    <p className="text-gray-400 text-sm">Event ID: {event.id}</p>
                </div>
                <div className={`${getRiskBgColor(event.risk_class)} px-4 py-2 rounded-full ${getRiskColor(event.risk_class)} font-bold text-sm uppercase`}>
                    {event.risk_class || 'Unknown'}
                </div>
            </div>

            {/* Overall Risk Score */}
            <div className="mb-6">
                <div className="flex justify-between items-end mb-2">
                    <span className="text-gray-400 text-sm font-semibold">Overall Risk Score</span>
                    <span className={`text-3xl font-bold ${getRiskColor(event.risk_class)}`}>
                        {riskPercentage.toFixed(0)}/100
                    </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-6 overflow-hidden">
                    <div
                        className={`h-6 rounded-full transition-all duration-1000 flex items-center justify-end px-3 ${event.risk_class === 'critical' ? 'bg-gradient-to-r from-red-700 to-red-500' :
                                event.risk_class === 'high' ? 'bg-gradient-to-r from-orange-700 to-orange-500' :
                                    event.risk_class === 'medium' ? 'bg-gradient-to-r from-yellow-700 to-yellow-500' :
                                        'bg-gradient-to-r from-green-700 to-green-500'
                            }`}
                        style={{ width: `${riskPercentage}%` }}
                    >
                        {riskPercentage > 15 && (
                            <span className="text-white text-xs font-bold">{riskPercentage.toFixed(0)}%</span>
                        )}
                    </div>
                </div>
            </div>

            {/* Risk Indicators */}
            <div className="grid grid-cols-2 gap-4 mb-6">
                {/* Hospitalization Risk */}
                <div className="bg-gray-800 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                        <svg className="w-5 h-5 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V16h2a1 1 0 110 2H7a1 1 0 110-2h2V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1z" clipRule="evenodd" />
                        </svg>
                        <span className="text-gray-300 text-sm font-semibold">Hospitalization</span>
                    </div>
                    <div className="text-2xl font-bold text-orange-300">{hospitalizationRisk.toFixed(1)}%</div>
                    <div className="text-xs text-gray-500 mt-1">likelihood</div>
                </div>

                {/* Mortality Risk */}
                <div className="bg-gray-800 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                        <svg className="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                        <span className="text-gray-300 text-sm font-semibold">Mortality</span>
                    </div>
                    <div className="text-2xl font-bold text-red-300">{mortalityRisk.toFixed(1)}%</div>
                    <div className="text-xs text-gray-500 mt-1">probability</div>
                </div>
            </div>

            {/* Event Details */}
            <div className="bg-gray-800 rounded-lg p-4 text-sm">
                <div className="grid grid-cols-2 gap-y-3">
                    <div>
                        <span className="text-gray-500">Drug:</span>
                        <div className="text-sand-light font-semibold">{event.suspected_drug || 'N/A'}</div>
                    </div>
                    <div>
                        <span className="text-gray-500">Adverse Effect:</span>
                        <div className="text-sand-light font-semibold">{event.adverse_effect || 'N/A'}</div>
                    </div>
                    <div>
                        <span className="text-gray-500">Seriousness:</span>
                        <div className={`font-semibold ${event.seriousness === 'serious' ? 'text-red-400' : 'text-green-400'}`}>
                            {event.seriousness || 'Unknown'}
                        </div>
                    </div>
                    <div>
                        <span className="text-gray-500">Follow-up Status:</span>
                        <div className="text-sand-light font-semibold capitalize">{event.followup_status || 'N/A'}</div>
                    </div>
                </div>
            </div>

            {/* High Risk Alert */}
            {(event.risk_class === 'high' || event.risk_class === 'critical') && (
                <div className="mt-4 bg-red-900 border-l-4 border-red-500 p-4 rounded">
                    <div className="flex items-start">
                        <svg className="w-6 h-6 text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                        <div className="ml-3">
                            <h4 className="text-red-200 font-bold">Escalation Required</h4>
                            <p className="text-red-300 text-sm mt-1">
                                This case has been flagged for immediate pharmacovigilance officer review.
                            </p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default RiskDashboard;
