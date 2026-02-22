/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** CityBikesWidget.jsx
*/

export default function CityBikesWidget({ data }) {
  return (
    <div className="w-full h-full flex flex-col text-left">
        <div className="flex justify-between items-center mb-3 bg-slate-50 p-2 rounded-lg border border-slate-100">
            <div className="flex flex-col items-center w-1/2 border-r border-slate-200">
                <span className="text-xl font-black text-green-600 leading-none">{data.total_bikes}</span>
                <span className="text-[10px] text-slate-500 uppercase font-bold mt-1 tracking-wider">Bikes</span>
            </div>
            <div className="flex flex-col items-center w-1/2">
                <span className="text-xl font-black text-slate-700 leading-none">{data.total_slots}</span>
                <span className="text-[10px] text-slate-500 uppercase font-bold mt-1 tracking-wider">Slots</span>
            </div>
        </div>

        <div className="text-[10px] text-slate-400 mb-2 uppercase font-bold tracking-wider border-b border-slate-100 pb-1">
            Top 5 bike stations ({data.network_name})
        </div>

        <ul className="space-y-2 overflow-y-auto flex-1 pr-1">
            {data.stations.map((st, i) => (
                <li key={i} className="flex justify-between items-center text-sm border-l-2 border-indigo-400 pl-2 bg-white">
                    <span className="truncate w-3/5 font-medium text-slate-700 text-xs" title={st.name}>
                        {st.name}
                    </span>
                    <div className="w-2/5 text-right text-xs">
                        <span className="text-green-600 font-bold">{st.free_bikes} 🚲</span> 
                        <span className="text-slate-300 mx-1">|</span> 
                        <span className="text-slate-500 font-medium">{st.empty_slots} 🅿️</span>
                    </div>
                </li>
            ))}
        </ul>
    </div>
  );
}
