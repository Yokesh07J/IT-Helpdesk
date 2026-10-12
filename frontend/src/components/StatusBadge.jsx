import React from 'react';

const STATUS_LABELS = {
  OPEN: 'Open',
  IN_PROGRESS: 'In Progress',
  RESOLVED: 'Resolved',
  CLOSED: 'Closed',
};

const StatusBadge = ({ status }) => {
  const label = STATUS_LABELS[status] || status;
  return (
    <span className={`badge status-${status}`}>
      <span className="badge-dot"></span>
      {label}
    </span>
  );
};

export default StatusBadge;
