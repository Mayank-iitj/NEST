import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import MicroForm from '../components/MicroForm';
import { answerFollowupQuestion } from '../services/api';

const AnswerPage = () => {
    const [searchParams] = useSearchParams();
    const [question] = useState("We only need one detail — were you hospitalized?");
    const [submitted, setSubmitted] = useState(false);

    const token = searchParams.get('token');
    const questionId = searchParams.get('question_id') || 1;

    const handleSubmit = async (answer) => {
        try {
            await answerFollowupQuestion(questionId, answer, token);
            setSubmitted(true);
        } catch (error) {
            alert('Error submitting answer: ' + (error.response?.data?.detail || error.message));
        }
    };

    if (submitted) {
        return (
            <div className="min-h-screen bg-primary-dark flex items-center justify-center p-4">
                <div className="card max-w-md text-center">
                    <div className="text-6xl mb-4">✅</div>
                    <h2 className="text-2xl font-bold text-sand-light mb-3">
                        Thank You!
                    </h2>
                    <p className="text-gray-300 mb-6">
                        Your answer has been recorded and will help improve medication safety.
                    </p>
                    <div className="bg-accent-green1 text-white p-4 rounded-lg">
                        <p className="text-sm">
                            🛡️ Your information is secure and encrypted.
                            We use it only for pharmacovigilance purposes.
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    return <MicroForm question={question} onSubmit={handleSubmit} />;
};

export default AnswerPage;
