# SpeedTrade Frontend

React + TypeScript frontend for the SpeedTrade trading application.

## Features

- ✅ User authentication (login/register)
- ✅ Redux state management
- ✅ TypeScript type safety
- ✅ React Router for navigation
- ✅ Axios for API calls
- 🚧 Real-time WebSocket support
- 🚧 Trading interface
- 🚧 Portfolio dashboard
- 🚧 Order management
- 🚧 Price charts

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Redux Toolkit** - State management
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Socket.io** - WebSocket client

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults should work for local dev)
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── main.tsx                 # Application entry point
│   ├── App.tsx                  # Root component with routing
│   ├── components/              # Reusable UI components
│   ├── pages/                   # Page components
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   └── DashboardPage.tsx
│   ├── services/                # API services
│   │   ├── api.ts              # Axios instance
│   │   ├── authService.ts      # Authentication API
│   │   ├── tradingService.ts   # Trading API
│   │   └── websocket.ts        # WebSocket client
│   ├── store/                   # Redux store
│   │   ├── index.ts            # Store configuration
│   │   ├── hooks.ts            # Typed Redux hooks
│   │   └── slices/             # Redux slices
│   │       ├── authSlice.ts
│   │       ├── portfolioSlice.ts
│   │       └── ordersSlice.ts
│   ├── types/                   # TypeScript types
│   │   └── index.ts
│   └── styles/                  # CSS files
│       └── index.css
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
└── README.md
```

## Available Scripts

### Development

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

## Features

### Current Features ✅

- User registration with email validation
- User login with JWT authentication
- Protected routes (dashboard requires login)
- Redux state management for auth
- Responsive layout
- Dark theme optimized for trading
- API integration with backend
- Environment configuration

### Upcoming Features 🚧

- Real-time price updates via WebSocket
- Order placement and management
- Portfolio tracking and analytics
- Position management
- Interactive price charts (TradingView)
- Price alerts and notifications
- Trade history
- Advanced order types
- Watchlist management
- Settings and preferences

## Development

### Adding a New Page

1. Create page component in `src/pages/`
2. Add route in `src/App.tsx`
3. Update navigation if needed

### Adding API Endpoints

1. Add types in `src/types/index.ts`
2. Add service methods in appropriate service file
3. Create Redux slice if needed for state management
4. Connect to components

### Styling

The app uses custom CSS in `src/styles/index.css`. 

Key classes:
- `.container` - Main content wrapper
- `.card` - Card component
- `.button` - Button styles
- `.input` - Input field styles

## Environment Variables

```bash
VITE_API_URL=http://localhost:8000    # Backend API URL
VITE_WS_URL=ws://localhost:8000       # WebSocket URL
VITE_ENVIRONMENT=development          # Environment
```

## API Integration

The frontend connects to the FastAPI backend:

- Auth: `/api/v1/auth/*`
- Orders: `/api/v1/orders/*`
- Portfolio: `/api/v1/portfolio`
- Positions: `/api/v1/positions/*`
- WebSocket: `/ws/{user_id}`

## State Management

Redux Toolkit is used for global state management:

- **authSlice** - User authentication state
- **portfolioSlice** - Portfolio data
- **ordersSlice** - Orders and trading state

## Testing

```bash
# Add testing framework (TODO)
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest
```

## Contributing

1. Follow TypeScript best practices
2. Use functional components with hooks
3. Keep components small and focused
4. Use Redux for global state, local state for component-specific data
5. Write meaningful commit messages

## Next Steps

- [ ] Add TradingView charts
- [ ] Implement order placement UI
- [ ] Add portfolio analytics
- [ ] Create watchlist feature
- [ ] Add price alerts
- [ ] Implement WebSocket price updates
- [ ] Add dark/light theme toggle
- [ ] Mobile responsive improvements
- [ ] Add loading states and skeleton screens
- [ ] Implement error boundaries

## License

See LICENSE file in root directory.
