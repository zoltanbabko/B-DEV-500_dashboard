/*
** EPITECH PROJECT, 2025
** Dashboard
** File description:
** CalendarWidget.jsx
*/

export default function CalendarWidget({ data }) {
    const formatDate = (isoString) => {
        const date = new Date(isoString);
        return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
    };

    return (
        <div className="w-full text-left h-full overflow-y-auto pr-1">
            <ul className="space-y-3">
                {data.map((event, i) => (
                    <li key={i} className="flex flex-col border-l-2 border-blue-100 pl-3 hover:border-blue-500 transition-colors">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">
                            {formatDate(event.start)}
                        </span>
                        <a 
                            href={event.link} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-sm font-medium text-slate-700 hover:text-blue-600 truncate block"
                            title={event.summary}
                            >
                            {event.summary}
                        </a>
                    </li>
                ))}
                {data.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full text-slate-400">
                        <span className="text-2xl mb-1">📅</span>
                        <p className="text-xs italic">No events scheduled</p>
                    </div>
                )}
            </ul>
        </div>
    );
}
