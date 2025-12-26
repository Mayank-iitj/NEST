import React, { useState } from 'react';

const OTPModal = ({ isOpen, onClose, onVerify, phoneOrEmail, channel }) => {
    const [otp, setOTP] = useState(['', '', '', '', '', '']);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [timer, setTimer] = useState(900); // 15 minutes in seconds

    React.useEffect(() => {
        if (!isOpen) return;

        const countdown = setInterval(() => {
            setTimer((prev) => {
                if (prev <= 0) {
                    clearInterval(countdown);
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);

        return () => clearInterval(countdown);
    }, [isOpen]);

    const handleChange = (index, value) => {
        if (value.length > 1) return;
        if (!/^\d*$/.test(value)) return;

        const newOTP = [...otp];
        newOTP[index] = value;
        setOTP(newOTP);

        // Auto-focus next input
        if (value && index < 5) {
            document.getElementById(`otp-${index + 1}`)?.focus();
        }
    };

    const handleKeyDown = (index, e) => {
        if (e.key === 'Backspace' && !otp[index] && index > 0) {
            document.getElementById(`otp-${index - 1}`)?.focus();
        }
    };

    const handleSubmit = async () => {
        const otpCode = otp.join('');
        if (otpCode.length !== 6) {
            setError('Please enter all 6 digits');
            return;
        }

        setLoading(true);
        setError('');

        try {
            await onVerify(otpCode);
            onClose();
        } catch (err) {
            setError(err.response?.data?.message || 'Invalid OTP');
        } finally {
            setLoading(false);
        }
    };

    const formatTime = () => {
        const mins = Math.floor(timer / 60);
        const secs = timer % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4">
            <div className="bg-sand-light rounded-2xl p-8 max-w-md w-full shadow-2xl border-4 border-accent-green1 animate-fade-in">
                {/* Secure Badge */}
                <div className="flex justify-center mb-6">
                    <div className="secure-badge">
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 1.944A11.954 11.954 0 012.166 5C2.056 5.649 2 6.319 2 7c0 5.225 3.34 9.67 8 11.317 4.66-1.647 8-6.092 8-11.317 0-.68-.057-1.35-.166-2.001A11.954 11.954 0 0110 1.944zM11 14a1 1 0 11-2 0 1 1 0 012 0zm0-7a1 1 0 10-2 0v3a1 1 0 102 0V7z" clipRule="evenodd" />
                        </svg>
                        Verified Medical Sender
                    </div>
                </div>

                <h2 className="text-2xl font-bold text-primary-dark mb-2 text-center">
                    Verify Your Identity
                </h2>
                <p className="text-gray-600 mb-6 text-center">
                    We sent a 6-digit code to {phoneOrEmail} via {channel}
                </p>

                {/* OTP Input */}
                <div className="flex justify-center gap-2 mb-6">
                    {otp.map((digit, index) => (
                        <input
                            key={index}
                            id={`otp-${index}`}
                            type="text"
                            inputMode="numeric"
                            maxLength={1}
                            value={digit}
                            onChange={(e) => handleChange(index, e.target.value)}
                            onKeyDown={(e) => handleKeyDown(index, e)}
                            className="w-12 h-14 text-center text-2xl font-bold bg-white border-2 border-accent-green1 rounded-lg focus:border-accent-green2 focus:outline-none transition-colors"
                        />
                    ))}
                </div>

                {/* Timer */}
                <div className="text-center mb-4">
                    <span className={`text-sm font-semibold ${timer < 60 ? 'text-red-600' : 'text-gray-600'}`}>
                        Code expires in {formatTime()}
                    </span>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4">
                        {error}
                    </div>
                )}

                {/* Buttons */}
                <button
                    onClick={handleSubmit}
                    disabled={loading || timer === 0}
                    className="btn-primary w-full mb-3 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {loading ? 'Verifying...' : 'Verify'}
                </button>

                <button
                    onClick={onClose}
                    className="w-full text-accent-green1 font-semibold hover:text-accent-green2 transition-colors"
                >
                    Cancel
                </button>

                {/* Security Notice */}
                <div className="mt-6 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                    <div className="flex">
                        <div className="flex-shrink-0">
                            <svg className="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                        </div>
                        <div className="ml-3">
                            <p className="text-sm text-yellow-700 font-medium">
                                🛡️ Never share this code with anyone. We will never ask for payment.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OTPModal;
