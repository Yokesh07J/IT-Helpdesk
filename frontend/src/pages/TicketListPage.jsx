import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ticketApi } from '../api/ticketApi';
import { useAuth } from '../context/AuthContext';
import TicketTable from '../components/TicketTable';
import { PlusCircle, Search, Filter, RefreshCw } from 'lucide-react';

const TicketListPage = () => {
  const { isStaff } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [priority, setPriority] = useState('');
  const [category, setCategory] = useState('');

  useEffect(() => {
    fetchTickets();
  }, [status, priority, category]);

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const data = await ticketApi.getTickets({
        status: status || undefined,
        priority: priority || undefined,
        category: category || undefined,
        search: search || undefined,
      });
      setTickets(data);
    } catch (err) {
      console.error('Failed to load tickets:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchTickets();
  };

  const handleResetFilters = () => {
    setSearch('');
    setStatus('');
    setPriority('');
    setCategory('');
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.75rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 700, color: '#fff' }}>
            {isStaff ? 'All IT Support Tickets' : 'My IT Tickets'}
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            {isStaff
              ? 'Triage, assign, search, and update resolution states'
              : 'Track the status and conversation updates on your reported issues'}
          </p>
        </div>

        <Link to="/tickets/new" className="btn btn-primary">
          <PlusCircle size={18} />
          <span>New Ticket</span>
        </Link>
      </div>

      {/* Toolbar & Filters */}
      <div className="card" style={{ marginBottom: '1.5rem', padding: '1.25rem' }}>
        <div className="toolbar" style={{ margin: 0 }}>
          <form onSubmit={handleSearchSubmit} className="search-box">
            <Search size={16} className="search-icon" />
            <input
              type="text"
              className="input"
              placeholder="Search by ID (HD-1001) or title..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </form>

          <div className="toolbar-filters">
            <select
              className="select"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              style={{ minWidth: '130px' }}
            >
              <option value="">All Statuses</option>
              <option value="OPEN">Open</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="RESOLVED">Resolved</option>
              <option value="CLOSED">Closed</option>
            </select>

            <select
              className="select"
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              style={{ minWidth: '130px' }}
            >
              <option value="">All Priorities</option>
              <option value="LOW">Low</option>
              <option value="MEDIUM">Medium</option>
              <option value="HIGH">High</option>
              <option value="URGENT">Urgent</option>
            </select>

            <select
              className="select"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              style={{ minWidth: '140px' }}
            >
              <option value="">All Categories</option>
              <option value="HARDWARE">Hardware</option>
              <option value="SOFTWARE">Software</option>
              <option value="NETWORK">Network</option>
              <option value="ACCESS_REQUEST">Access Request</option>
              <option value="OTHER">Other</option>
            </select>

            <button type="button" onClick={handleResetFilters} className="btn btn-secondary btn-sm" title="Reset Filters">
              Reset
            </button>

            <button type="button" onClick={fetchTickets} className="btn btn-secondary btn-sm" title="Refresh">
              <RefreshCw size={14} />
            </button>
          </div>
        </div>
      </div>

      {/* Results Table */}
      <div className="card" style={{ padding: 0 }}>
        {loading ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            Loading tickets...
          </div>
        ) : (
          <TicketTable tickets={tickets} showCreator={isStaff} />
        )}
      </div>
    </div>
  );
};

export default TicketListPage;
