import axiosClient from './axiosClient';

export const userApi = {
  getSupportStaff: async () => {
    const res = await axiosClient.get('/users/staff');
    return res.data;
  },
};
