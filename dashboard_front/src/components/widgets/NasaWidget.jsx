/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** SpacexWidget.jsx
*/

export default function NasaWidget({ data }) {
    return (
        <div className="flex flex-col w-full h-full">
            <div className="relative w-full h-40 rounded-lg overflow-hidden mb-3 bg-black group">
                {data.type === "video" ? (
                    <iframe 
                        src={data.url} 
                        title="Nasa Video" 
                        className="w-full h-full pointer-events-none" 
                        frameBorder="0"
                    ></iframe>
                ) : (
                    <img 
                        src={data.url} 
                        alt="Space" 
                        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" 
                    />
                )}
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-2">
                    <p className="text-[10px] text-white/80 text-right">© {data.copyright}</p>
                </div>
            </div>

            <h3 className="font-bold text-sm text-slate-800 leading-tight">
                {data.title}
            </h3>
        </div>
    );
}
