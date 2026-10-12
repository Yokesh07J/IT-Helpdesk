import React from 'react';
import { Monitor, Cpu, Wifi, Key, HelpCircle } from 'lucide-react';

const CATEGORY_MAP = {
  HARDWARE: { label: 'Hardware', icon: Cpu },
  SOFTWARE: { label: 'Software', icon: Monitor },
  NETWORK: { label: 'Network', icon: Wifi },
  ACCESS_REQUEST: { label: 'Access Request', icon: Key },
  OTHER: { label: 'Other', icon: HelpCircle },
};

const CategoryBadge = ({ category }) => {
  const item = CATEGORY_MAP[category] || { label: category, icon: HelpCircle };
  const IconComponent = item.icon;

  return (
    <span className="category-tag">
      <IconComponent size={13} />
      <span>{item.label}</span>
    </span>
  );
};

export default CategoryBadge;
