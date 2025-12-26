/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    dark: '#1B211A',
                },
                accent: {
                    green1: '#628141',
                    green2: '#8BAE66',
                },
                sand: {
                    light: '#EBD5AB',
                },
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
