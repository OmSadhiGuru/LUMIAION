import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./lib/AuthContext";
import AppShell from "./components/AppShell";
import Home from "./pages/Home";
import Modules from "./pages/Modules";
import Settings from "./pages/Settings";
import Login from "./pages/Login";
import Knowledge from "./pages/modules/Knowledge";
import LifeOS from "./pages/modules/LifeOS";
import BusinessOS from "./pages/modules/BusinessOS";
import FinanceOS from "./pages/modules/FinanceOS";
import BodyOS from "./pages/modules/BodyOS";
import ContentOS from "./pages/modules/ContentOS";
import AgentOS from "./pages/modules/AgentOS";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route index element={<Home />} />
            <Route path="modules" element={<Modules />} />
            <Route path="settings" element={<Settings />} />
            <Route path="login" element={<Login />} />
            <Route path="knowledge" element={<Knowledge />} />
            <Route path="life" element={<LifeOS />} />
            <Route path="business" element={<BusinessOS />} />
            <Route path="finance" element={<FinanceOS />} />
            <Route path="body" element={<BodyOS />} />
            <Route path="content" element={<ContentOS />} />
            <Route path="agents" element={<AgentOS />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
