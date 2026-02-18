/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** WeatherWidget.jsx
*/

export default function WeatherWidget({data}) {
    return (
    <div className="text-center py-2">
        <div className="flex justify-center items-center gap-3">
            <img src={data.icon} alt="Météo" className="w-16 h-16 drop-shadow-sm" />
            <span className="text-5xl font-bold text-slate-800">{data.temp}°</span>
        </div>
        <p className="text-slate-500 capitalize font-medium mt-1">{data.desc}</p>

        <div className="flex justify-between text-xs text-slate-400 mt-4 px-4 border-t border-slate-100 pt-3">
            <div className="flex flex-col">
                <span className="font-bold text-slate-600">{data.humidity}%</span>
                <span>Humidité</span>
            </div>
            <div className="flex flex-col">
                <span className="font-bold text-slate-600">{data.wind} km/h</span>
                <span>Vent</span>
            </div>
        </div>
    </div>
    );
}
