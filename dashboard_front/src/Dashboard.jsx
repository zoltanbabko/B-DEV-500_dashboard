/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** Dashboard.jsx
*/

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import WidgetsCard from "./components/WidgetsCard";

export default function Dashboard() {
    const navigate = useNavigate();
    const [widgets, setWidgets] = useState([]);
    const [availableWidgets, setAvailableWidgets] = useState([]);
    const [lastUpdated, setLastUpdated] = useState(new Date());
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedType, setSelectedType] = useState("");
    const [formParams, setFormParams] = useState({});

    const logout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            logout();
            return;
        }

        const initData = async () => {
            await fetchWidgets(token);
            await fetchCatalog();
        };

        initData();

        const interval = setInterval(() => {
            setLastUpdated(new Date());
        }, 30000);

        return () => clearInterval(interval);
    }, [navigate]);

    const fetchWidgets = async (token) => {
        try {
            const response = await fetch("http://127.0.0.1:8000/widgets/", {
                headers: { Authorization: `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                setWidgets(data);
            } else if (response.status === 401) {
                    logout();
            }
        } catch (error) {
            console.error("Server connection error:", error);
        }
    };

    const fetchCatalog = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/widgets/available");
            if (response.ok) {
                const data = await response.json();
                setAvailableWidgets(data);
            }
        } catch (error) {
            console.error(error);
        }
    };

    const handleDelete = async (id) => {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:8000/widgets/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.ok) {
            setWidgets(widgets.filter(w => w.id !== id));
        } else if (response.status === 401) {
            logout();
        }
    };

    const handleAddWidget = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("token");

        const definition = availableWidgets.find(w => w.type === selectedType);
        if (!definition)
            return;

        const response = await fetch("http://127.0.0.1:8000/widgets/", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json", 
                Authorization: `Bearer ${token}` 
            },
            body: JSON.stringify({
                service: definition.service,
                type: definition.type,
                params: formParams,
                position: widgets.length
            })
        });

        if (response.ok) {
            const newWidget = await response.json();
            setWidgets([...widgets, newWidget]);
            setIsModalOpen(false);
            setFormParams({});
            setSelectedType("");
        } else if (response.status === 401) {
            logout();
        }
    };

    const handleParamChange = (name, value) => {
        setFormParams(prev => ({ ...prev, [name]: value }));
    };

    const selectedDefinition = availableWidgets.find(w => w.type === selectedType);

    return (
        <div className="min-h-screen bg-slate-100 text-slate-900 pb-20">
            <div className="bg-white border-b border-slate-200 px-8 py-4 flex justify-between items-center shadow-sm sticky top-0 z-40">
                <div className="flex items-center gap-4">
                    <div className="text-2xl font-bold text-slate-800 tracking-tight">Dashboard</div>
                    <div className="badge badge-ghost gap-2 text-slate-500 font-mono text-xs hidden md:flex">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-3 h-3 animate-spin">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
                        </svg>
                        Last update: {lastUpdated.toLocaleTimeString()}
                    </div>
                </div>
                <div className="dropdown dropdown-end">
                    <div tabIndex={0} role="button" className="btn btn-circle btn-ghost bg-slate-50 border border-slate-200">U</div>
                    <ul tabIndex={0} className="mt-3 z-[1] p-2 shadow-lg menu menu-sm dropdown-content bg-white rounded-lg w-40 border border-slate-100">
                        <li><a onClick={logout} className="text-red-600">Logout</a></li>
                    </ul>
                </div>
            </div>

            <div className="max-w-7xl mx-auto p-8">
                <div className="flex justify-between items-end mb-8 border-b border-slate-200 pb-4">
                    <div>
                        <h1 className="text-3xl font-bold text-slate-900">My Widgets</h1>
                        <p className="text-slate-500 mt-1">Manage your personal space</p>
                        <p className="text-xs text-slate-400 mt-2 md:hidden">Updated: {lastUpdated.toLocaleTimeString()}</p>
                    </div>
                    <button 
                        onClick={() => setIsModalOpen(true)}
                        className="btn btn-primary bg-indigo-600 hover:bg-indigo-700 text-white border-none normal-case font-medium rounded-lg px-6 shadow-md shadow-indigo-200"
                        >
                        + Add Widget
                    </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {widgets.map(widget => (
                        <WidgetsCard 
                            key={widget.id} 
                            widget={widget} 
                            onDelete={handleDelete} 
                            refreshTrigger={lastUpdated}
                        />
                    ))}

                    <div onClick={() => setIsModalOpen(true)} className="bg-slate-50 p-10 rounded-xl border-2 border-dashed border-slate-300 flex flex-col items-center justify-center text-center hover:border-indigo-400 hover:bg-white cursor-pointer transition-all group min-h-[250px]">
                        <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center mb-4 group-hover:bg-indigo-50 shadow-sm transition-colors">
                            <span className="text-3xl text-slate-400 group-hover:text-indigo-500 font-light">+</span>
                        </div>
                        <h3 className="text-lg font-bold text-slate-700 group-hover:text-indigo-700">Add New Widget</h3>
                    </div>
                </div>
            </div>

            {isModalOpen && (
                <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg overflow-hidden">
                        <div className="bg-slate-50 px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                            <h3 className="font-bold text-lg text-slate-800">Configure Widget</h3>
                            <button onClick={() => setIsModalOpen(false)} className="btn btn-sm btn-circle btn-ghost">✕</button>
                        </div>
                        <form onSubmit={handleAddWidget} className="p-6 flex flex-col gap-6">
                            <div>
                                <label className="block text-sm font-bold text-slate-700 mb-2">Select Widget Type</label>
                                <select 
                                    className="select select-bordered w-full bg-white text-slate-900 border-slate-300"
                                    value={selectedType}
                                    onChange={(e) => { setSelectedType(e.target.value); setFormParams({}); }}
                                    required
                                    >
                                    <option value="" disabled>Choose a widget</option>
                                    {availableWidgets.map(w => (
                                        <option key={w.type} value={w.type}>{w.name} ({w.service})</option>
                                    ))}
                                </select>
                                {selectedDefinition && <p className="text-xs text-slate-500 mt-2">{selectedDefinition.description}</p>}
                            </div>
                            {selectedDefinition && selectedDefinition.params.map(param => (
                                <div key={param.name}>
                                    <label className="block text-sm font-bold text-slate-700 mb-2">{param.label || param.name}</label>
                                    <input
                                        type={param.type === "int" ? "number" : "text"}
                                        className="input input-bordered w-full bg-white text-slate-900 border-slate-300 focus:border-indigo-500"
                                        placeholder={`Enter ${param.name}...`}
                                        required
                                        onChange={(e) => handleParamChange(param.name, e.target.value)}
                                    />
                                </div>
                            ))}
                            <div className="flex gap-3 mt-4">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="btn flex-1 bg-white border-slate-300 text-slate-700 hover:bg-slate-50 normal-case">Cancel</button>
                                <button type="submit" className="btn flex-1 btn-primary bg-indigo-600 hover:bg-indigo-700 border-none text-white normal-case">Add Widget</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
