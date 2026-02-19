/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** GmailWidget.jsx
*/

export default function GmailWidget({ data }) {
    return (
        <div className="w-full">
            <div className="flex justify-end mb-3">
                {data.count > 0 ? (
                    <span className="badge badge-sm badge-error text-white font-bold">
                        {data.count} new
                    </span>
                ) : (
                    <span className="badge badge-sm badge-ghost text-slate-400">
                        All read
                    </span>
                )}
            </div>

            <ul className="space-y-2">
                {data.emails.map((email, i) => (
                    <li key={i} className="bg-slate-50 p-3 rounded border border-slate-100 text-left hover:bg-white hover:shadow-sm transition-all">
                        <div className="flex justify-between items-start w-full">
                            <p className="font-bold text-sm text-slate-800 truncate w-2/3">{email.from}</p>
                        </div>
                        <p className="text-xs text-slate-500 truncate mt-1">{email.subject}</p>
                    </li>
                ))}
                {data.emails.length === 0 && (
                    <div className="flex flex-col items-center justify-center py-4 text-slate-400">
                        <span className="text-2xl mb-2">🎉</span>
                        <p className="text-sm italic">You're all caught up!</p>
                    </div>
                )}
            </ul>
        </div>
    );
}
