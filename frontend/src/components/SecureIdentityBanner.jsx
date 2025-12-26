import React from 'react';

const SecureIdentityBanner = ({ hospitalName = "Verified Healthcare Provider" }) => {
    return (
        <div className="bg-accent-green1 text-white py-3 px-4 shadow-lg">
            <div className="container mx-auto flex items-center justify-between">
                <div className="flex items-center gap-3">
                    {/* Shield Icon */}
                    <div className="bg-white rounded-full p-2">
                        <svg className="w-6 h-6 text-accent-green1" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 1.944A11.954 11.954 0 012.166 5C2.056 5.649 2 6.319 2 7c0 5.225 3.34 9.67 8 11.317 4.66-1.647 8-6.092 8-11.317 0-.68-.057-1.35-.166-2.001A11.954 11.954 0 0110 1.944zM11 14a1 1 0 11-2 0 1 1 0 012 0zm0-7a1 1 0 10-2 0v3a1 1 0 102 0V7z" clipRule="evenodd" />
                        </svg>
                    </div>

                    <div>
                        <div className="font-bold text-sm">✓ Verified Medical Sender</div>
                        <div className="text-xs opacity-90">{hospitalName}</div>
                    </div>
                </div>

                {/* Scam Safety Badge */}
                <div className="hidden md:flex items-center gap-2 bg-white bg-opacity-20 px-4 py-2 rounded-full">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="text-sm font-semibold">Scam-Safe</span>
                </div>
            </div>
        </div>
    );
};

export default SecureIdentityBanner;
