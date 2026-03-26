/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** WidgetsCard.jsx
*/

import { useState, useEffect } from "react";
import WeatherWidget from "./widgets/WeatherWidget";
import GmailWidget from "./widgets/GmailWidget";
import { GithubProfileWidget, GithubIssuesWidget } from "./widgets/GithubProfileWidget";
import NasaWidget from "./widgets/NasaWidget";
import CatWidget from "./widgets/CatWidget";
import CalendarWidget from "./widgets/CalendarWidget";
import CityBikesWidget from "./widgets/CityBikesWidget";

const WIDGET_COMPONENTS = {
    "city_temperature": WeatherWidget,
    "gmail_unread": GmailWidget,
    "user_profile": GithubProfileWidget,
    "github_issues": GithubIssuesWidget,
    "nasa_apod": NasaWidget,
    "random_cat": CatWidget,
    "google_calendar": CalendarWidget,
    "city_bikes": CityBikesWidget,
};

export default function WidgetCard({widget, onDelete, refreshTrigger}) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const getWidgetSubtitle = () => {
        if (widget.params.city)
            return widget.params.city;
        if (widget.type === 'gmail_unread')
            return 'GMAIL';
        if (widget.type === 'user_profile')
            return 'PROFILE';
        if (widget.type === 'github_issues' && widget.params.repo)
            return widget.params.repo;
        if (widget.type === 'nasa_apod')
            return 'APOD';
        if (widget.type === 'random_cat')
            return 'MEOW';
        if (widget.type === 'google_calendar')
            return 'CALENDAR';
        if (widget.type === 'city_bikes' && widget.params.city)
            return widget.params.city;
        return '';
    };

    const subtitle = getWidgetSubtitle();

    useEffect(() => {
        const fetchData = async () => {
            if (!data)
                setLoading(true);

            const token = localStorage.getItem("token");
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/widgets/${widget.id}/data`,
                    {headers: { Authorization: `Bearer ${token}` },});
                const result = await response.json();
                if (!response.ok) {
                    if (response.status === 401 || response.status === 403) {
                        throw new Error("Login required");
                    }
                    throw new Error(result.detail || "Error");
                }
                setData(result);
                setError("");
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [widget.id, refreshTrigger]);

    const SpecificWidgetComponent = WIDGET_COMPONENTS[widget.type];

    return (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm relative group hover:shadow-lg transition-all hover:border-indigo-200 flex flex-col h-full">
            <button onClick={() => onDelete(widget.id)}
            className="absolute top-3 right-3 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-full w-8 h-8 flex items-center justify-center transition-colors opacity-0 group-hover:opacity-100 z-10"
            >✕
            </button>

            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${widget.service === 'github' ? 'bg-black' : widget.service === 'google' ? 'bg-red-500' : 'bg-blue-400'}`}></span>
                {widget.service} {subtitle && `• ${subtitle}`}
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

