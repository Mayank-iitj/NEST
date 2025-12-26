import React, { useState, useEffect } from 'react';

const MicroForm = ({ question, onSubmit, fieldName, currentStep = 1, totalSteps = 3 }) => {
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [voiceSupported] = useState('webkitSpeechRecognition' in window || 'SpeechRecognition' in window);
    const [isListening, setIsListening] = useState(false);

    const handleVoiceInput = () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        recognition.onstart = () => setIsListening(true);
        recognition.onend = () => setIsListening(false);

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setAnswer(transcript);
        };

        recognition.start();
    };

    const handleSubmit = async () => {
        if (!answer.trim()) return;

        setLoading(true);
        try {
            await onSubmit(answer);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-primary-dark to-accent-green1">
            <div className="max-w-lg w-full">
                {/* Progress Dots */}
                <div className="flex justify-center gap-2 mb-8">
                    {[...Array(totalSteps)].map((_, index) => (
                        <div
                            key={index}
                            className={`h-2 rounded-full transition-all duration-300 ${index + 1 === currentStep
                                    ? 'w-8 bg-accent-green2'
                                    : index + 1 < currentStep
                                        ? 'w-2 bg-accent-green1'
                                        : 'w-2 bg-gray-600'
                                }`}
                        />
                    ))}
                </div>

                {/* Card */}
                <div className="bg-sand-light rounded-3xl p-8 shadow-2xl border-4 border-accent-green2">
                    {/* Question */}
                    <div className="mb-6">
                        <div className="inline-block bg-accent-green1 text-white px-3 py-1 rounded-full text-xs font-semibold mb-3">
                            Quick Question
                        </div>
                        <h2 className="text-2xl font-bold text-primary-dark leading-relaxed whitespace-pre-line">
                            {question}
                        </h2>
                    </div>

                    {/* Answer Input */}
                    <div className="mb-6">
                        <textarea
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                            placeholder="Type your answer here..."
                            className="input-field min-h-[120px] resize-none text-base"
                            rows={4}
                        />
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-3 mb-4">
                        <button
                            onClick={handleSubmit}
                            disabled={!answer.trim() || loading}
                            className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed text-lg"
                        >
                            {loading ? 'Submitting...' : 'Submit Answer'}
                        </button>

                        {voiceSupported && (
                            <button
                                onClick={handleVoiceInput}
                                disabled={isListening}
                                className={`btn-secondary w-14 h-14 flex items-center justify-center rounded-full ${isListening ? 'animate-pulse bg-red-500' : ''
                                    }`}
                                title="Voice input"
                            >
                                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
                                </svg>
                            </button>
                        )}
                    </div>

                    {/* Estimated Time */}
                    <div className="text-center text-gray-600 text-sm mb-4">
                        <svg className="w-4 h-4 inline mr-1" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                        </svg>
                        Estimated time: ~20 seconds
                    </div>

                    {/* Safety Notice */}
                    <div className="bg-green-50 border-l-4 border-accent-green1 p-3 rounded text-sm">
                        <p className="text-gray-700">
                            🛡️ <strong>Safe & Secure:</strong> Your response helps ensure medication safety.
                            We never ask for payment or financial information.
                        </p>
                    </div>
                </div>

                {/* Footer */}
                <div className="text-center mt-6 text-sand-light text-sm">
                    Step {currentStep} of {totalSteps} • Press Enter to submit
                </div>
            </div>
        </div>
    );
};

export default MicroForm;
