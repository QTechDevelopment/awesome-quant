import { createSlice } from '@reduxjs/toolkit';
import type { Order } from '../../types';

interface OrdersState {
  orders: Order[];
  isLoading: boolean;
}

const initialState: OrdersState = {
  orders: [],
  isLoading: false,
};

const ordersSlice = createSlice({
  name: 'orders',
  initialState,
  reducers: {},
});

export default ordersSlice.reducer;
