import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ticketApi } from '../api/ticketApi';
import { PlusCircle, ArrowLeft, AlertCircle } from 'lucide-react';

const CreateTicketPage = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'SOFTWARE',
    priority: 'MEDIUM',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.title.trim().length < 3) {
      setError('Title must be at least 3 characters');
      return;
    }

    if (formData.description.trim().length < 5) {
      setError('Description must be at least 5 characters');
      return;
    }

    setLoading(true);
    try {
      const created = await ticketApi.createTicket(formData);
      navigate(`/tickets/${created.id}`);
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to create ticket. Please verify inputs.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <Link to="/tickets" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '0.75rem' }}>
          <ArrowLeft size={16} />
          <span>Back to Tickets</span>
        </Link>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 700, color: '#fff' }}>
          Create New Support Ticket
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          Submit an IT incident or service request. A unique ticket ID will be generated automatically.
        </p>
      </div>

      <div className="card">
        {error && (
          <div className="alert alert-error">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Ticket Title / Summary</label>
            <input
              type="text"
              name="title"
              className="input"
              value={formData.title}
              onChange={handleChange}
              placeholder="e.g. Cannot connect to staging database via VPN"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Category</label>
              <select
                name="category"
                className="select"
                value={formData.category}
                onChange={handleChange}
              >
                <option value="SOFTWARE">Software & Applications</option>
                <option value="HARDWARE">Hardware & Peripherals</option>
                <option value="NETWORK">Network & VPN</option>
                <option value="ACCESS_REQUEST">Access & Permissions</option>
                <option value="OTHER">Other Technical Inquiries</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Priority</label>
              <select
                name="priority"
                className="select"
                value={formData.priority}
                onChange={handleChange}
              >
                <option value="LOW">Low (Minor convenience issue)</option>
                <option value="MEDIUM">Medium (Normal workflow affected)</option>
                <option value="HIGH">High (Major blockage in work)</option>
                <option value="URGENT">Urgent (System outage / critical)</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Detailed Description</label>
            <textarea
              name="description"
              className="textarea"
              rows={6}
              value={formData.description}
              onChange={handleChange}
              placeholder="Provide error codes, steps to reproduce, device information, or access requirements..."
              required
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem' }}>
            <Link to="/tickets" className="btn btn-secondary">
              Cancel
            </Link>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              <PlusCircle size={18} />
              <span>{loading ? 'Submitting Ticket...' : 'Create Ticket'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateTicketPage;
