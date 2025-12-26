import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// OTP Services
export const sendOTP = (phone_or_email, channel, reporter_id = null) => {
    return api.post('/otp/send', { phone_or_email, channel, reporter_id });
};

export const verifyOTP = (phone_or_email, otp) => {
    return api.post('/otp/verify', { phone_or_email, otp });
};

// Reporter Services  
export const createReporter = (reporterData) => {
    return api.post('/report/reporter', reporterData);
};

// Event Services
export const initializeReport = (eventData) => {
    return api.post('/report/init', eventData);
};

export const getEvent = (eventId) => {
    return api.get(`/report/event/${eventId}`);
};

export const detectMissingFields = (eventId) => {
    return api.post(`/report/missing-fields/${eventId}`);
};

export const generateNarrative = (eventId) => {
    return api.get(`/report/narrative/${eventId}`);
};

// Follow-up Services
export const sendFollowupQuestion = (eventId) => {
    return api.post(`/followup/send?event_id=${eventId}`);
};

export const answerFollowupQuestion = (questionId, answerText, token) => {
    return api.post('/followup/answer', { question_id: questionId, answer_text: answerText, token });
};

export const getEventQuestions = (eventId) => {
    return api.get(`/followup/questions/${eventId}`);
};

// Risk Services
export const getRiskScore = (eventId) => {
    return api.get(`/risk/score/${eventId}`);
};

// Dashboard Services
export const getDashboardMetrics = () => {
    return api.get('/dashboard/metrics');
};
