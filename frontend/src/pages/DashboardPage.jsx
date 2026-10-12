import React from 'react';
import { useAuth } from '../context/AuthContext';
import AdminDashboardPage from './AdminDashboardPage';
import EmployeeDashboardPage from './EmployeeDashboardPage';

const DashboardPage = () => {
  const { isStaff } = useAuth();
  return isStaff ? <AdminDashboardPage /> : <EmployeeDashboardPage />;
};

export default DashboardPage;
