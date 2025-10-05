import { createSlice } from '@reduxjs/toolkit';
import type { Portfolio } from '../../types';

interface PortfolioState {
  portfolio: Portfolio | null;
  isLoading: boolean;
}

const initialState: PortfolioState = {
  portfolio: null,
  isLoading: false,
};

const portfolioSlice = createSlice({
  name: 'portfolio',
  initialState,
  reducers: {},
});

export default portfolioSlice.reducer;
