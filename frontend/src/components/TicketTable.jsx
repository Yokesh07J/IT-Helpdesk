import React from 'react';
import { useNavigate } from 'react-router-dom';
import StatusBadge from './StatusBadge';
import PriorityBadge from './PriorityBadge';
import CategoryBadge from './CategoryBadge';
import { ExternalLink, User } from 'lucide-react';

const TicketTable = ({ tickets, showCreator = true }) => {
  const navigate = useNavigate();

  if (!tickets || tickets.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem 1.5rem' }}>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>No tickets found matching your query.</p>
      </div>
    );
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return '—';
    const d = new Date(dateStr);
    return d.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Ticket ID</th>
            <th>Title</th>
            <th>Category</th>
            <th>Priority</th>
            <th>Status</th>
            {showCreator && <th>Created By</th>}
            <th>Assigned To</th>
            <th>Created</th>
            <th style={{ textAlign: 'right' }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map((ticket) => (
            <tr
              key={ticket.id}
              onClick={() => navigate(`/tickets/${ticket.id}`)}
              style={{ cursor: 'pointer' }}
            >
              <td>
                <span className="ticket-code-pill">{ticket.ticketCode}</span>
              </td>
              <td>
                <div style={{ fontWeight: 600, color: '#fff', maxWidth: '320px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {ticket.title}
                </div>
              </td>
              <td>
                <CategoryBadge category={ticket.category} />
              </td>
              <td>
                <PriorityBadge priority={ticket.priority} />
              </td>
              <td>
                <StatusBadge status={ticket.status} />
              </td>
              {showCreator && (
                <td>
                  <span style={{ color: 'var(--text-muted)' }}>
                    {ticket.createdBy?.fullName || '—'}
                  </span>
                </td>
              )}
              <td>
                {ticket.assignedTo ? (
                  <span style={{ color: '#c084fc', display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.85rem' }}>
                    <User size={13} />
                    {ticket.assignedTo.fullName}
                  </span>
                ) : (
                  <span style={{ color: 'var(--text-dim)', fontStyle: 'italic', fontSize: '0.82rem' }}>
                    Unassigned
                  </span>
                )}
              </td>
              <td style={{ color: 'var(--text-dim)', fontSize: '0.82rem' }}>
                {formatDate(ticket.createdAt)}
              </td>
              <td style={{ textAlign: 'right' }}>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/tickets/${ticket.id}`);
                  }}
                >
                  <ExternalLink size={14} />
                  <span>View</span>
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TicketTable;
