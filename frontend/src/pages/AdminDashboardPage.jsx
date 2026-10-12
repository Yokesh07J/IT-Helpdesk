import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ticketApi } from '../api/ticketApi';
import { useAuth } from '../context/AuthContext';
import StatCard from '../components/StatCard';
import TicketTable from '../components/TicketTable';
import { Shield, Ticket, Clock, CheckCircle2, AlertTriangle, Archive, ArrowRight, RefreshCw } from 'lucide-react';

const AdminDashboardPage = () => {
  const { user, isAdmin } = useAuth();
  const [stats, setStats] = useState({
    totalTickets: 0,
    openTickets: 0,
    inProgressTickets: 0,
    resolvedTickets: 0,
    closedTickets: 0,
  });
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [statsData, ticketsData] = await Promise.all([
        ticketApi.getDashboardStats(),
        ticketApi.getTickets(),
      ]);
      setStats(statsData);
      setTickets(ticketsData.slice(0, 8));
    } catch (err) {
      console.error('Failed to load admin dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.75rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <Shield size={20} color="#f87171" />
            <span style={{ fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', color: '#f87171', letterSpacing: '0.05em' }}>
              {isAdmin ? 'Administrator Console' : 'Support Team Console'}
            </span>
          </div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 700, color: '#fff' }}>
            IT Operations & Incident Overview
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Real-time monitoring, triage, and ticket resolution across all departments
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button onClick={loadData} className="btn btn-secondary">
            <RefreshCw size={16} />
            <span>Refresh</span>
          </button>
          <Link to="/tickets" className="btn btn-primary">
            <span>Manage All Tickets</span>
            <ArrowRight size={16} />
          </Link>
        </div>
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
          label="Open (Unresolved)"
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
        <StatCard
          label="Closed"
          value={stats.closedTickets}
          icon={Archive}
          type="closed"
        />
      </div>

      {/* Ticket List Preview */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
          <div>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#fff' }}>
              Recent Tickets Awaiting Attention
            </h2>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.82rem' }}>
              Latest tickets reported across all departments
            </p>
          </div>

          <Link to="/tickets" className="btn btn-secondary btn-sm">
            <span>View All & Filter</span>
            <ArrowRight size={14} />
          </Link>
        </div>

        {loading ? (
          <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            Loading tickets...
          </div>
        ) : (
          <TicketTable tickets={tickets} showCreator={true} />
        )}
      </div>
    </div>
  );
};

export default AdminDashboardPage;
