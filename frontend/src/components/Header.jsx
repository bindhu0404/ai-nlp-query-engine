// frontend/src/components/Header.jsx
import React from "react";

const Header = () => {
  return (
    <header className="bg-blue-600 text-white shadow-md p-4 rounded-xl flex justify-between items-center">
      <h1 className="text-2xl font-bold tracking-wide">AI Query Engine</h1>
      <span className="text-sm opacity-80">Powered by FastAPI + React</span>
    </header>
  );
};

export default Header;
