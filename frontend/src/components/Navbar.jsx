import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LifeBuoy, PlusCircle, LayoutDashboard, Ticket, LogOut } from 'lucide-react';

const Navbar = () => {
  const { user, logout, isStaff } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getRoleBadgeClass = () => {
    if (user?.role === 'ROLE_ADMIN') return 'admin';
    if (user?.role === 'ROLE_SUPPORT') return 'support';
    return 'employee';
  };

  const getRoleLabel = () => {
    if (user?.role === 'ROLE_ADMIN') return 'Admin';
    if (user?.role === 'ROLE_SUPPORT') return 'Support Staff';
    return 'Employee';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="nav-brand">
          <div className="nav-brand-icon">
            <LifeBuoy size={20} color="#fff" />
          </div>
          <span>IT Helpdesk</span>
        </Link>

        <div className="nav-links">
          <Link
            to="/dashboard"
            className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}
          >
            <LayoutDashboard size={17} />
            <span>Dashboard</span>
          </Link>

          <Link
            to="/tickets"
            className={`nav-link ${location.pathname === '/tickets' ? 'active' : ''}`}
          >
            <Ticket size={17} />
            <span>{isStaff ? 'All Tickets' : 'My Tickets'}</span>
          </Link>

          <Link
            to="/tickets/new"
            className={`nav-link ${location.pathname === '/tickets/new' ? 'active' : ''}`}
          >
            <PlusCircle size={17} />
            <span>New Ticket</span>
          </Link>
        </div>

        <div className="nav-user">
          <div className="user-badge">
            <span className="user-name">{user?.fullName}</span>
            <span className={`role-chip ${getRoleBadgeClass()}`}>{getRoleLabel()}</span>
          </div>

          <button onClick={handleLogout} className="btn btn-secondary btn-sm" title="Sign out">
            <LogOut size={16} />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
