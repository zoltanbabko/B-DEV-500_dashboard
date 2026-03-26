/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** Auth.jsx
*/

import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

export default function Auth({mode}) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const location = useLocation();
    const isRegister = mode === "register";

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const token = params.get("token");
        if (token) {
            localStorage.setItem("token", token);
            navigate("/");
        }
    }, [location, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        let url = `${import.meta.env.VITE_API_URL}/auth/login`;
        if (isRegister)
            url = `${import.meta.env.VITE_API_URL}/auth/register`;

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (!response.ok)
                throw new Error(data.detail || "Error");

            if (data.access_token) {
                localStorage.setItem("token", data.access_token);
                navigate("/");
            } else if (isRegister) {
                navigate("/login");
            }
        } catch (err) {
            setError(err.message);
        }
    };

    const handleOAuth = (provider) => {
        window.location.href = `${import.meta.env.VITE_API_URL}/auth/${provider}/login`;
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="bg-white p-8 rounded-xl shadow-xl w-full max-w-md border border-slate-200">

                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-slate-900">
                        {isRegister ? "Create Account" : "Welcome Back"}
                    </h1>
                    <p className="text-slate-500 mt-2 font-medium">
                        {isRegister ? "Dashboard Access" : "Login to Dashboard"}
                    </p>
                </div>

            <form onSubmit={handleSubmit} className="flex flex-col gap-5">
                <div>
                    <label className="block text-slate-700 font-bold mb-2 text-sm">Email Address</label>
                    <input 
                        type="email" 
                        className="input input-bordered w-full bg-white border-slate-300 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 text-slate-900 rounded-lg" 
                        placeholder="name@example.com"
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                    />
                </div>

                <div>
                    <label className="block text-slate-700 font-bold mb-2 text-sm">Password</label>
                    <input 
                        type="password" 
                        className="input input-bordered w-full bg-white border-slate-300 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 text-slate-900 rounded-lg" 
                        placeholder="••••••••"
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                    />
                </div>

                {error && (<div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-3 text-sm">{error}</div>)}

                <button className="btn btn-primary w-full bg-indigo-600 hover:bg-indigo-700 border-none text-white font-bold text-lg normal-case rounded-lg h-12">
                    {isRegister ? "Sign Up" : "Log In"}
                </button>
            </form>

            <div className="divider my-8 text-slate-400 font-medium">OR</div>
                <div className="grid grid-cols-2 gap-4">
                    <button onClick={() => handleOAuth('google')} className="btn btn-outline border-slate-300 hover:bg-slate-50 hover:text-slate-900 hover:border-slate-400 text-slate-700 normal-case font-medium">
                        Google
                    </button>
                    <button onClick={() => handleOAuth('github')} className="btn btn-outline border-slate-300 hover:bg-slate-50 hover:text-slate-900 hover:border-slate-400 text-slate-700 normal-case font-medium">
                        GitHub
                    </button>
                </div>

                <div className="text-center mt-8 text-sm">
                    <span className="text-slate-500">
                        {isRegister ? "Already have an account?" : "Don't have an account?"}
                    </span>
                    <span 
                        onClick={() => navigate(isRegister ? "/login" : "/register")} 
                        className="text-indigo-600 font-bold cursor-pointer ml-2 hover:underline"
                        >
                        {isRegister ? "Log In" : "Sign Up"}
                    </span>
                </div>
            </div>
        </div>
    );
}
