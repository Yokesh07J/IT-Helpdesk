import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ticketApi } from '../api/ticketApi';
import { userApi } from '../api/userApi';
import { useAuth } from '../context/AuthContext';
import StatusBadge from '../components/StatusBadge';
import PriorityBadge from '../components/PriorityBadge';
import CategoryBadge from '../components/CategoryBadge';
import {
  ArrowLeft,
  User,
  Calendar,
  Building,
  CheckCircle,
  MessageSquare,
  Send,
  Lock,
  UserCheck,
  AlertCircle,
} from 'lucide-react';

const TicketDetailPage = () => {
  const { id } = useParams();
  const { user, isStaff, isEmployee } = useAuth();

  const [ticket, setTicket] = useState(null);
  const [comments, setComments] = useState([]);
  const [staffList, setStaffList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [actionSuccess, setActionSuccess] = useState('');

  // Status & Assignment Form
  const [newStatus, setNewStatus] = useState('');
  const [resolutionNotes, setResolutionNotes] = useState('');
  const [selectedStaffId, setSelectedStaffId] = useState('');

  // Comment Form
  const [commentText, setCommentText] = useState('');
  const [isInternalComment, setIsInternalComment] = useState(false);
  const [submittingComment, setSubmittingComment] = useState(false);

  useEffect(() => {
    loadTicket();
    if (isStaff) {
      loadStaff();
    }
  }, [id, isStaff]);

  const loadTicket = async () => {
    setLoading(true);
    try {
      const data = await ticketApi.getTicketById(id);
      setTicket(data);
      setComments(data.comments || []);
      setNewStatus(data.status);
      setResolutionNotes(data.resolutionNotes || '');
      setSelectedStaffId(data.assignedTo?.id ? String(data.assignedTo.id) : '');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load ticket details.');
    } finally {
      setLoading(false);
    }
  };

  const loadStaff = async () => {
    try {
      const staff = await userApi.getSupportStaff();
      setStaffList(staff);
    } catch (err) {
      console.error('Failed to load support staff:', err);
    }
  };

  const handleStatusUpdate = async (e) => {
    e.preventDefault();
    setActionSuccess('');
    setError('');

    try {
      const updated = await ticketApi.updateStatus(id, {
        status: newStatus,
        resolutionNotes: resolutionNotes || undefined,
      });
      setTicket(updated);
      setActionSuccess('Ticket status updated successfully!');
      setTimeout(() => setActionSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update status.');
    }
  };

  const handleAssignStaff = async (e) => {
    e.preventDefault();
    if (!selectedStaffId) return;
    setActionSuccess('');
    setError('');

    try {
      const updated = await ticketApi.assignTicket(id, {
        assignedToUserId: Number(selectedStaffId),
      });
      setTicket(updated);
      setActionSuccess('Ticket successfully assigned!');
      setTimeout(() => setActionSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to assign ticket.');
    }
  };

  const handleCloseOwnTicket = async () => {
    setActionSuccess('');
    try {
      const updated = await ticketApi.updateStatus(id, {
        status: 'CLOSED',
        resolutionNotes: 'Closed by employee',
      });
      setTicket(updated);
      setNewStatus('CLOSED');
      setActionSuccess('Ticket closed.');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to close ticket.');
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    setSubmittingComment(true);
    try {
      const newComment = await ticketApi.addComment(id, {
        message: commentText.trim(),
        internalNote: isInternalComment,
      });
      setComments((prev) => [...prev, newComment]);
      setCommentText('');
      setIsInternalComment(false);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to post comment.');
    } finally {
      setSubmittingComment(false);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '—';
    const d = new Date(dateStr);
    return d.toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>Loading ticket details...</div>;
  }

  if (error && !ticket) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <AlertCircle size={32} color="#f87171" style={{ margin: '0 auto 1rem' }} />
        <h2 style={{ color: '#fff', marginBottom: '0.5rem' }}>Ticket Not Found</h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>{error}</p>
        <Link to="/tickets" className="btn btn-secondary">
          Return to Tickets
        </Link>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <Link to="/tickets" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '1.25rem' }}>
        <ArrowLeft size={16} />
        <span>Back to Ticket List</span>
      </Link>

      {actionSuccess && (
        <div className="alert alert-success">
          <CheckCircle size={18} />
          <span>{actionSuccess}</span>
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Main Ticket Card */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div className="ticket-header">
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
              <span className="ticket-code-pill" style={{ fontSize: '0.95rem' }}>{ticket.ticketCode}</span>
              <StatusBadge status={ticket.status} />
              <PriorityBadge priority={ticket.priority} />
              <CategoryBadge category={ticket.category} />
            </div>
            <h1 style={{ fontSize: '1.45rem', fontWeight: 700, color: '#fff' }}>{ticket.title}</h1>
          </div>

          {isEmployee && ticket.status === 'RESOLVED' && (
            <button onClick={handleCloseOwnTicket} className="btn btn-secondary btn-sm">
              <CheckCircle size={16} />
              <span>Confirm & Close Ticket</span>
            </button>
          )}
        </div>

        {/* Metadata Grid */}
        <div className="meta-grid">
          <div>
            <div className="meta-item-label">Reported By</div>
            <div className="meta-item-val" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <User size={14} color="var(--primary)" />
              {ticket.createdBy?.fullName}
            </div>
          </div>
          <div>
            <div className="meta-item-label">Department</div>
            <div className="meta-item-val" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Building size={14} color="var(--text-dim)" />
              {ticket.createdBy?.department || 'General'}
            </div>
          </div>
          <div>
            <div className="meta-item-label">Assigned Staff</div>
            <div className="meta-item-val" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <UserCheck size={14} color="#c084fc" />
              {ticket.assignedTo ? ticket.assignedTo.fullName : 'Unassigned'}
            </div>
          </div>
          <div>
            <div className="meta-item-label">Created Date</div>
            <div className="meta-item-val" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Calendar size={14} color="var(--text-dim)" />
              {formatDate(ticket.createdAt)}
            </div>
          </div>
        </div>

        {/* Description Body */}
        <div style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.6rem' }}>
            Problem Description
          </h3>
          <div style={{ background: 'rgba(0, 0, 0, 0.25)', padding: '1rem 1.25rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
            {ticket.description}
          </div>
        </div>

        {/* Resolution Notes Banner */}
        {ticket.resolutionNotes && (
          <div className="resolution-box">
            <h4>
              <CheckCircle size={18} />
              <span>Resolution Notes</span>
            </h4>
            <p style={{ color: 'var(--text-main)', fontSize: '0.9rem', whiteSpace: 'pre-wrap' }}>
              {ticket.resolutionNotes}
            </p>
            {ticket.resolvedAt && (
              <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginTop: '0.5rem' }}>
                Resolved on {formatDate(ticket.resolvedAt)}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Staff Actions Panel */}
      {isStaff && (
        <div className="card" style={{ marginBottom: '1.5rem', background: 'var(--bg-secondary)' }}>
          <h2 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#fff', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <UserCheck size={18} color="var(--primary)" />
            <span>Staff Ticket Operations</span>
          </h2>

          <div className="form-row">
            {/* Status Update Form */}
            <form onSubmit={handleStatusUpdate} style={{ flex: 1 }}>
              <div className="form-group">
                <label className="form-label">Update Status</label>
                <select
                  className="select"
                  value={newStatus}
                  onChange={(e) => setNewStatus(e.target.value)}
                >
                  <option value="OPEN">OPEN</option>
                  <option value="IN_PROGRESS">IN_PROGRESS</option>
                  <option value="RESOLVED">RESOLVED</option>
                  <option value="CLOSED">CLOSED</option>
                </select>
              </div>

              {(newStatus === 'RESOLVED' || newStatus === 'CLOSED') && (
                <div className="form-group">
                  <label className="form-label">Resolution Notes</label>
                  <textarea
                    className="textarea"
                    rows={2}
                    value={resolutionNotes}
                    onChange={(e) => setResolutionNotes(e.target.value)}
                    placeholder="Describe how the problem was resolved..."
                  />
                </div>
              )}

              <button type="submit" className="btn btn-secondary btn-sm">
                Save Status
              </button>
            </form>

            {/* Assignment Form */}
            <form onSubmit={handleAssignStaff} style={{ flex: 1 }}>
              <div className="form-group">
                <label className="form-label">Assign Support Staff</label>
                <select
                  className="select"
                  value={selectedStaffId}
                  onChange={(e) => setSelectedStaffId(e.target.value)}
                >
                  <option value="">Select Support Staff...</option>
                  {staffList.map((st) => (
                    <option key={st.id} value={st.id}>
                      {st.fullName} ({st.department})
                    </option>
                  ))}
                </select>
              </div>

              <button
                type="submit"
                className="btn btn-primary btn-sm"
                disabled={!selectedStaffId || selectedStaffId === String(ticket.assignedTo?.id)}
              >
                Assign Ticket
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Activity / Comments Thread */}
      <div className="card">
        <h2 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#fff', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <MessageSquare size={18} color="var(--primary)" />
          <span>Ticket Activity & Comments ({comments.length})</span>
        </h2>

        {comments.length === 0 ? (
          <p style={{ color: 'var(--text-dim)', fontStyle: 'italic', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
            No comments yet on this ticket.
          </p>
        ) : (
          <div className="comments-container">
            {comments.map((c) => (
              <div key={c.id} className={`comment-card ${c.internalNote ? 'internal' : ''}`}>
                <div className="comment-header">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span className="comment-author">{c.author?.fullName}</span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                      • {c.author?.department || c.author?.role}
                    </span>
                    {c.internalNote && (
                      <span className="badge" style={{ background: 'rgba(234, 179, 8, 0.15)', color: '#facc15', fontSize: '0.68rem', padding: '1px 6px' }}>
                        <Lock size={10} style={{ marginRight: '3px' }} /> Internal Note
                      </span>
                    )}
                  </div>
                  <span>{formatDate(c.createdAt)}</span>
                </div>
                <div className="comment-text">{c.message}</div>
              </div>
            ))}
          </div>
        )}

        {/* Add Comment Form */}
        <form onSubmit={handleAddComment} style={{ marginTop: '1.5rem' }}>
          <div className="form-group" style={{ marginBottom: '0.75rem' }}>
            <label className="form-label">Add a Note or Reply</label>
            <textarea
              className="textarea"
              rows={3}
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              placeholder="Type your message, troubleshooting step, or question..."
              required
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
            {isStaff ? (
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                <input
                  type="checkbox"
                  checked={isInternalComment}
                  onChange={(e) => setIsInternalComment(e.target.checked)}
                />
                <Lock size={14} color="#facc15" />
                <span>Internal staff note (hidden from employee)</span>
              </label>
            ) : (
              <div></div>
            )}

            <button type="submit" className="btn btn-primary btn-sm" disabled={submittingComment || !commentText.trim()}>
              <Send size={15} />
              <span>{submittingComment ? 'Posting...' : 'Post Comment'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TicketDetailPage;
