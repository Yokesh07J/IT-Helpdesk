import React from 'react';

const StatCard = ({ label, value, icon: Icon, type = 'all' }) => {
  return (
    <div className={`stat-card ${type}`}>
      <div>
        <div className="stat-label">{label}</div>
        <div className="stat-value">{value}</div>
      </div>
      {Icon && (
        <div className="stat-icon">
          <Icon size={22} className="text-muted" />
        </div>
      )}
    </div>
  );
};

export default StatCard;
