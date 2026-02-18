/*
** EPITECH PROJECT, 2026
** Dashboard
** File description:
** App.jsx
*/

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Auth from "./Auth";
import Dashboard from "./Dashboard";

const PrivateRoute = ({children}) => {
    const token = localStorage.getItem("token");
    return token ? children : <Navigate to="/login" />;
};

const PublicRoute = ({children}) => {
    const token = localStorage.getItem("token");
    return token ? <Navigate to="/" /> : children;
};

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/"
                    element={
                        <PrivateRoute>
                            <Dashboard />
                        </PrivateRoute>
                    }
                />
        
                <Route 
                    path="/login" 
                    element={
                        <PublicRoute>
                        <Auth mode="login" />
                        </PublicRoute>
                    }
                />

                <Route
                    path="/register" 
                    element={
                        <PublicRoute>
                        <Auth mode="register" />
                        </PublicRoute>
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
