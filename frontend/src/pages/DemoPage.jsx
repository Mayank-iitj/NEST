import React, { useState } from 'react';
import OTPModal from '../components/OTPModal';
import RiskDashboard from '../components/RiskDashboard';
import { createReporter, initializeReport, sendOTP, verifyOTP, sendFollowupQuestion } from '../services/api';

const DemoPage = () => {
    const [step, setStep] = useState(1);
    const [showOTP, setShowOTP] = useState(false);
    const [reporter, setReporter] = useState(null);
    const [event, setEvent] = useState(null);
    const [loading, setLoading] = useState(false);

    const [formData, setFormData] = useState({
        name: 'John Doe',
        phone: '+1234567890',
        email: 'john.doe@example.com',
        suspected_drug: 'Aspirin',
        adverse_effect: 'Severe headache and dizziness',
        seriousness: 'serious',
        hospitalization: true,
    });

    const handleCreateReport = async () => {
        setLoading(true);
        try {
            // Create reporter
            const reporterRes = await createReporter({
                reporter_type: 'patient',
                name: formData.name,
                phone: formData.phone,
                email: formData.email,
                language: 'en'
            });
            setReporter(reporterRes.data);

            // Send OTP
            await sendOTP(formData.phone, 'sms', reporterRes.data.id);
            setShowOTP(true);
        } catch (error) {
            alert('Error creating report: ' + (error.response?.data?.detail || error.message));
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyOTP = async (otp) => {
        try {
            await verifyOTP(formData.phone, otp);

            // Create event
            const eventRes = await initializeReport({
                reporter_id: reporter.id,
                suspected_drug: formData.suspected_drug,
                adverse_effect: formData.adverse_effect,
                seriousness: formData.seriousness,
                hospitalization: formData.hospitalization,
                consent: true
            });

            setEvent(eventRes.data);
            setStep(2);
        } catch (error) {
            throw error;
        }
    };

    const handleSendFollowup = async () => {
        setLoading(true);
        try {
            await sendFollowupQuestion(event.id);
            alert('Follow-up question sent successfully via SMS/WhatsApp!');
            setStep(3);
        } catch (error) {
            alert('Error sending follow-up: ' + (error.response?.data?.detail || error.message));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-primary-dark p-6">
            <div className="container mx-auto max-w-6xl">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-5xl font-bold text-sand-light mb-4">
                        Pharmacovigilance Demo
                    </h1>
                    <p className="text-accent-green2 text-xl">
                        Real-time, AI-powered adverse event follow-up system
                    </p>
                </div>

                {/* Step 1: Initial Report */}
                {step === 1 && (
                    <div className="grid md:grid-cols-2 gap-8">
                        <div className="card">
                            <h2 className="text-2xl font-bold text-sand-light mb-6">
                                📋 Submit Adverse Event Report
                            </h2>

                            <div className="space-y-4">
                                <div>
                                    <label className="block text-gray-400 text-sm mb-2">Patient Name</label>
                                    <input
                                        type="text"
                                        value={formData.name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        className="input-field"
                                    />
                                </div>

                                <div>
                                    <label className="block text-gray-400 text-sm mb-2">Phone Number</label>
                                    <input
                                        type="tel"
                                        value={formData.phone}
                                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                                        className="input-field"
                                    />
                                </div>

                                <div>
                                    <label className="block text-gray-400 text-sm mb-2">Suspected Drug</label>
                                    <input
                                        type="text"
                                        value={formData.suspected_drug}
                                        onChange={(e) => setFormData({ ...formData, suspected_drug: e.target.value })}
                                        className="input-field"
                                    />
                                </div>

                                <div>
                                    <label className="block text-gray-400 text-sm mb-2">Adverse Effect</label>
                                    <textarea
                                        value={formData.adverse_effect}
                                        onChange={(e) => setFormData({ ...formData, adverse_effect: e.target.value })}
                                        className="input-field"
                                        rows={3}
                                    />
                                </div>

                                <div className="flex items-center">
                                    <input
                                        type="checkbox"
                                        id="hospitalization"
                                        checked={formData.hospitalization}
                                        onChange={(e) => setFormData({ ...formData, hospitalization: e.target.checked })}
                                        className="w-5 h-5 rounded text-accent-green1"
                                    />
                                    <label htmlFor="hospitalization" className="ml-3 text-gray-300">
                                        Patient was hospitalized
                                    </label>
                                </div>

                                <button
                                    onClick={handleCreateReport}
                                    disabled={loading}
                                    className="btn-primary w-full disabled:opacity-50"
                                >
                                    {loading ? 'Processing...' : 'Submit Report & Verify Identity'}
                                </button>
                            </div>
                        </div>

                        <div className="space-y-6">
                            <div className="card bg-accent-green1 text-white">
                                <h3 className="text-xl font-bold mb-4">✨ What Happens Next?</h3>
                                <ol className="space-y-3 list-decimal list-inside">
                                    <li>You'll receive an OTP to verify your identity</li>
                                    <li>AI analyzes the report for missing safety data</li>
                                    <li>Risk score is calculated automatically</li>
                                    <li>A micro follow-up question is generated (if needed)</li>
                                    <li>Question sent via SMS/WhatsApp (~20sec to answer)</li>
                                </ol>
                            </div>

                            <div className="card">
                                <h3 className="text-xl font-bold text-sand-light mb-4">🔒 Security Features</h3>
                                <div className="space-y-2 text-gray-300">
                                    <div className="flex items-center gap-2">
                                        <svg className="w-5 h-5 text-accent-green2" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                        </svg>
                                        OTP verification required
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <svg className="w-5 h-5 text-accent-green2" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                        </svg>
                                        AES-256 encrypted PHI
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <svg className="w-5 h-5 text-accent-green2" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                        </svg>
                                        Full audit trail
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Step 2: Risk Assessment */}
                {step === 2 && event && (
                    <div className="space-y-8">
                        <div className="text-center">
                            <h2 className="text-3xl font-bold text-sand-light mb-2">
                                ✅ Report Verified & Analyzed
                            </h2>
                            <p className="text-accent-green2">
                                AI has detected missing fields and calculated risk score
                            </p>
                        </div>

                        <RiskDashboard event={event} />

                        <div className="card">
                            <h3 className="text-2xl font-bold text-sand-light mb-4">
                                📱 Send Follow-up Question
                            </h3>
                            <p className="text-gray-300 mb-6">
                                AI has identified <strong className="text-accent-green2">{event.missing_fields?.length || 0}</strong> missing fields that are important for regulatory compliance.
                                A micro follow-up question will be sent via SMS/WhatsApp.
                            </p>

                            {event.missing_fields && event.missing_fields.length > 0 && (
                                <div className="bg-gray-800 rounded-lg p-4 mb-6">
                                    <div className="text-sm text-gray-400 mb-2">Missing Fields:</div>
                                    <div className="flex flex-wrap gap-2">
                                        {event.missing_fields.map((field, index) => (
                                            <span key={index} className="px-3 py-1 bg-accent-green1 text-white rounded-full text-sm">
                                                {field}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            <button
                                onClick={handleSendFollowup}
                                disabled={loading}
                                className="btn-primary w-full disabled:opacity-50"
                            >
                                {loading ? 'Sending...' : 'Send Follow-up Question'}
                            </button>
                        </div>
                    </div>
                )}

                {/* Step 3: Success */}
                {step === 3 && (
                    <div className="text-center">
                        <div className="card max-w-2xl mx-auto">
                            <div className="text-6xl mb-6">🎉</div>
                            <h2 className="text-3xl font-bold text-sand-light mb-4">
                                Demo Complete!
                            </h2>
                            <p className="text-gray-300 mb-6">
                                The system has successfully:
                            </p>
                            <div className="space-y-3 text-left mb-8">
                                <div className="flex items-start gap-3">
                                    <svg className="w-6 h-6 text-accent-green2 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-gray-300">Verified patient identity via OTP</span>
                                </div>
                                <div className="flex items-start gap-3">
                                    <svg className="w-6 h-6 text-accent-green2 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-gray-300">Detected missing regulatory-relevant fields using AI</span>
                                </div>
                                <div className="flex items-start gap-3">
                                    <svg className="w-6 h-6 text-accent-green2 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-gray-300">Calculated risk score and classification</span>
                                </div>
                                <div className="flex items-start gap-3">
                                    <svg className="w-6 h-6 text-accent-green2 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-gray-300">Generated and sent micro follow-up question</span>
                                </div>
                            </div>

                            <div className="flex gap-4">
                                <button
                                    onClick={() => window.location.href = '/dashboard'}
                                    className="btn-primary flex-1"
                                >
                                    View Metrics Dashboard
                                </button>
                                <button
                                    onClick={() => window.location.reload()}
                                    className="btn-secondary flex-1"
                                >
                                    Start New Demo
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {/* OTP Modal */}
                <OTPModal
                    isOpen={showOTP}
                    onClose={() => setShowOTP(false)}
                    onVerify={handleVerifyOTP}
                    phoneOrEmail={formData.phone}
                    channel="sms"
                />
            </div>
        </div>
    );
};

export default DemoPage;
