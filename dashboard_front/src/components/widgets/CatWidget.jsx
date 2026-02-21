/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** CatWidget.jsx
*/

export default function CatWidget({ data }) {
    return (
        <div className="w-full h-full flex items-center justify-center bg-slate-50 rounded-lg overflow-hidden relative group">
            <img 
                src={data.image} 
                alt="Random Cat" 
                className="w-full h-48 object-cover rounded-lg group-hover:scale-105 transition-transform duration-500" 
            />
            <div className="absolute bottom-2 right-2 bg-white/80 px-2 py-1 rounded-full text-xs font-bold text-slate-600 shadow-sm backdrop-blur-sm">
                Meow 🐱
            </div>
        </div>
    );
}
