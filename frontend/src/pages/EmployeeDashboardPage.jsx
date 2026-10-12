import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ticketApi } from '../api/ticketApi';
import { useAuth } from '../context/AuthContext';
import StatCard from '../components/StatCard';
import TicketTable from '../components/TicketTable';
import { PlusCircle, Ticket, Clock, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';

const EmployeeDashboardPage = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalTickets: 0,
    openTickets: 0,
    inProgressTickets: 0,
    resolvedTickets: 0,
    closedTickets: 0,
  });
  const [recentTickets, setRecentTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [statsData, ticketsData] = await Promise.all([
        ticketApi.getDashboardStats(),
        ticketApi.getTickets(),
      ]);
      setStats(statsData);
      setRecentTickets(ticketsData.slice(0, 5));
    } catch (err) {
      console.error('Failed to load employee dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.75rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 700, color: '#fff' }}>
            Welcome back, {user?.fullName}
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            {user?.department} • Track and submit your IT service requests
          </p>
        </div>

        <Link to="/tickets/new" className="btn btn-primary">
          <PlusCircle size={18} />
          <span>Report an Issue</span>
        </Link>
      </div>

      {/* Metrics Row */}
      <div className="stats-grid">
        <StatCard
          label="Total Tickets"
          value={stats.totalTickets}
          icon={Ticket}
          type="all"
        />
        <StatCard
          label="Open Issues"
          value={stats.openTickets}
          icon={AlertTriangle}
          type="open"
        />
        <StatCard
          label="In Progress"
          value={stats.inProgressTickets}
          icon={Clock}
          type="in-progress"
        />
        <StatCard
          label="Resolved"
          value={stats.resolvedTickets}
          icon={CheckCircle2}
          type="resolved"
        />
      </div>

      {/* Recent Tickets Section */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
          <div>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#fff' }}>
              My Recent Tickets
            </h2>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.82rem' }}>
              Showing your 5 most recently created IT tickets
            </p>
          </div>

          <Link to="/tickets" className="btn btn-secondary btn-sm">
            <span>View All</span>
            <ArrowRight size={14} />
          </Link>
        </div>

        {loading ? (
          <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            Loading tickets...
          </div>
        ) : (
          <TicketTable tickets={recentTickets} showCreator={false} />
        )}
      </div>
    </div>
  );
};

export default EmployeeDashboardPage;
