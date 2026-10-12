import axiosClient from './axiosClient';

export const ticketApi = {
  getTickets: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.status) params.append('status', filters.status);
    if (filters.priority) params.append('priority', filters.priority);
    if (filters.category) params.append('category', filters.category);
    if (filters.search) params.append('search', filters.search);

    const res = await axiosClient.get(`/tickets?${params.toString()}`);
    return res.data;
  },

  getTicketById: async (id) => {
    const res = await axiosClient.get(`/tickets/${id}`);
    return res.data;
  },

  createTicket: async (ticketData) => {
    const res = await axiosClient.post('/tickets', ticketData);
    return res.data;
  },

  updateStatus: async (id, statusData) => {
    const res = await axiosClient.put(`/tickets/${id}/status`, statusData);
    return res.data;
  },

  assignTicket: async (id, assignData) => {
    const res = await axiosClient.put(`/tickets/${id}/assign`, assignData);
    return res.data;
  },

  addComment: async (ticketId, commentData) => {
    const res = await axiosClient.post(`/tickets/${ticketId}/comments`, commentData);
    return res.data;
  },

  getComments: async (ticketId) => {
    const res = await axiosClient.get(`/tickets/${ticketId}/comments`);
    return res.data;
  },

  getDashboardStats: async () => {
    const res = await axiosClient.get('/dashboard/stats');
    return res.data;
  },
};
