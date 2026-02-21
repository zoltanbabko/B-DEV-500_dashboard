/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** GithubProfileWidget.jsx
*/

export function GithubProfileWidget({ data }) {
    return (
        <div className="flex flex-col items-center text-center w-full">
            <div className="relative group mb-3">
                <div className="absolute -inset-1 bg-gradient-to-r from-gray-600 to-black rounded-full blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
                <img 
                    src={data.avatar} 
                    alt="Avatar" 
                    className="relative w-20 h-20 rounded-full border-4 border-white shadow-sm object-cover" 
                />
            </div>

            <h3 className="font-bold text-xl text-slate-800 mb-1">{data.username}</h3>
      
            <div className="grid grid-cols-2 gap-4 w-full mt-4 bg-slate-50 p-3 rounded-lg border border-slate-100">
                <div className="flex flex-col">
                    <span className="font-bold text-slate-800 text-lg">{data.repos}</span>
                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Public repositories</span>
                </div>
                <div className="flex flex-col border-l border-slate-200">
                    <span className="font-bold text-slate-800 text-lg">{data.followers}</span>
                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Followers</span>
                </div>
            </div>
        </div>
    );
}

export function GithubIssuesWidget({ data }) {
    return (
        <div className="flex flex-col w-full">
            <h3 className="font-bold text-xl text-slate-800 mb-4">Open Issues</h3>
            {data.length === 0 ? (
                <p className="text-sm text-slate-500">No open issues found.</p>
            ) : (
                <ul className="space-y-3">
                    {data.map((issue) => (
                        <li key={issue.id} className="p-3 bg-slate-50 rounded-lg border border-slate-100 hover:bg-slate-100 transition">
                            <a href={issue.url} target="_blank" rel="noopener noreferrer" className="font-medium text-blue-600 hover:underline">
                                {issue.title}
                            </a>
                            <p className="text-sm text-slate-500 mt-1">#{issue.number}</p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
