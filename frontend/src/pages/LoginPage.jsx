import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LifeBuoy, LogIn, AlertCircle, Sparkles } from 'lucide-react';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, loading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      const msg = err.response?.data?.message || 'Login failed. Please check your credentials.';
      setError(msg);
    }
  };

  const fillCredentials = (demoEmail, demoPass) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setError('');
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <div className="auth-header">
          <div className="nav-brand-icon" style={{ margin: '0 auto 1rem auto', width: '44px', height: '44px' }}>
            <LifeBuoy size={26} color="#fff" />
          </div>
          <h1 className="auth-title">IT Helpdesk Portal</h1>
          <p className="auth-subtitle">Sign in to report and track IT support tickets</p>
        </div>

        {error && (
          <div className="alert alert-error">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Email Address</label>
            <input
              type="email"
              className="input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. employee@company.com"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={loading}
            style={{ marginTop: '0.75rem' }}
          >
            <LogIn size={18} />
            <span>{loading ? 'Authenticating...' : 'Sign In'}</span>
          </button>
        </form>

        <div style={{ marginTop: '1.25rem', textAlign: 'center', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          Don't have an employee account?{' '}
          <Link to="/register" style={{ color: 'var(--primary)', fontWeight: 600 }}>
            Register here
          </Link>
        </div>

        {/* Demo Fast Login Buttons for Lab CAT evaluation */}
        <div className="quick-roles">
          <div className="quick-roles-title">
            <Sparkles size={13} style={{ display: 'inline', marginRight: '4px', verticalAlign: '-1px' }} />
            Demo Fast-Login Credentials
          </div>
          <div className="quick-roles-grid">
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => fillCredentials('john.doe@company.com', 'Pass@123')}
            >
              Employee
            </button>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => fillCredentials('support.alex@helpdesk.com', 'Support@123')}
            >
              Support Staff
            </button>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => fillCredentials('admin@helpdesk.com', 'Admin@123')}
            >
              Admin
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
