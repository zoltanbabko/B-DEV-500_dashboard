/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** WidgetsCard.jsx
*/

import { useState, useEffect } from "react";
import WeatherWidget from "./widgets/WeatherWidget";

const WIDGET_COMPONENTS = {
    "city_temperature": WeatherWidget
};


export default function WidgetCard({widget, onDelete}) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/widgets/${widget.id}/data`,
                    {headers: { Authorization: `Bearer ${token}` },});
                const result = await response.json();
                if (!response.ok) {
                    if (response.status === 401 || response.status === 403) {
                        throw new Error("Login required");
                    }
                    throw new Error(result.detail || "Error");
                }
                setData(result);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [widget.id]);

    const SpecificWidgetComponent = WIDGET_COMPONENTS[widget.type];

    return (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm relative group hover:shadow-lg transition-all hover:border-indigo-200 flex flex-col h-full">
            <button onClick={() => onDelete(widget.id)}
            className="absolute top-3 right-3 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-full w-8 h-8 flex items-center justify-center transition-colors opacity-0 group-hover:opacity-100 z-10"
            >✕
            </button>

            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${widget.service === 'github' ? 'bg-black' : 'bg-blue-400'}`}></span>
                {widget.service} {widget.params.city && `• ${widget.params.city}`}
            </h3>

            <div className="flex-1 flex items-center justify-center w-full">
                {loading && <div className="animate-pulse h-20 bg-slate-100 rounded w-full"></div>}
                {error && <div className="text-red-500 text-sm bg-red-50 p-2 rounded w-full text-center">⚠️ {error}</div>}
                {!loading && !error && SpecificWidgetComponent && (<SpecificWidgetComponent data={data} />)}
                {!loading && !error && !SpecificWidgetComponent && (<p className="text-slate-400 italic">Widget unknown: {widget.type}</p>)}
            </div>
        </div>
    );
}
