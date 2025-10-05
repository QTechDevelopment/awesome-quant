# SpeedTrade Frontend

React + TypeScript + Vite frontend for the SpeedTrade trading platform.

## 🚀 Tech Stack

- **React 18.2** - UI library
- **TypeScript 5.2** - Type safety
- **Vite 5.0** - Build tool & dev server
- **Redux Toolkit 1.9** - State management
- **TailwindCSS 3.3** - Styling
- **Axios 1.6** - HTTP client
- **Socket.io-client 4.5** - WebSocket
- **React Router 6.20** - Routing
- **React Hot Toast 2.6** - Notifications
- **Lucide React 0.294** - Icons

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── layout/        # Layout components (Header, Sidebar, etc.)
│   ├── pages/             # Page components (Dashboard, Trade, etc.)
│   ├── services/          # API services
│   ├── store/             # Redux store & slices
│   ├── hooks/             # Custom React hooks
│   ├── types/             # TypeScript types
│   ├── utils/             # Utility functions
│   ├── App.tsx            # Root component
│   ├── main.tsx           # Application entry point
│   └── index.css          # Global styles
├── public/                # Static assets
├── index.html             # HTML template
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # TailwindCSS configuration
├── tsconfig.json          # TypeScript configuration
└── package.json           # Dependencies
```

## 🛠️ Setup & Installation

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Install Dependencies

```bash
npm install
```

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 🏃 Development

### Start Dev Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`.

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

### Lint Code

```bash
npm run lint
```

### Type Check

```bash
npm run type-check
```

### Run Tests

```bash
npm test              # Run tests
npm run test:ui       # Run tests with UI
npm run test:coverage # Run tests with coverage
```

## 📄 Pages

### Authentication
- **Login** (`/login`) - User login with email/username
- **Register** (`/register`) - New user registration

### Main App (Protected)
- **Dashboard** (`/dashboard`) - Portfolio overview, stats, recent activity
- **Trade** (`/trade`) - Place orders, search symbols, view quotes
- **Portfolio** (`/portfolio`) - View positions, P&L analysis
- **Orders** (`/orders`) - Order history, cancel pending orders

## 🔌 API Integration

The frontend connects to the backend API through:

### REST API
- Base URL: `http://localhost:8000/api/v1`
- Axios client with JWT token interceptors
- Auto token refresh on 401 errors

### WebSocket
- URL: `ws://localhost:8000/ws`
- Socket.io client for real-time market data
- Auto-reconnection on disconnect

## 🎨 Styling

### TailwindCSS

Custom utility classes defined in `src/index.css`:

```css
/* Buttons */
.btn-primary
.btn-secondary
.btn-danger

/* Inputs */
.input

/* Cards */
.card
```

### Color Scheme

```css
primary: Blue (#3B82F6)
success: Green (#10B981)
danger: Red (#EF4444)
warning: Yellow (#F59E0B)
```

## 🔒 Authentication Flow

1. User logs in via `/login`
2. JWT tokens stored in Redux + localStorage
3. Axios interceptor adds `Authorization` header
4. Protected routes check `isAuthenticated` state
5. Auto-redirect to login on 401 errors

## 📊 State Management

Redux Toolkit with 4 slices:

### authSlice
- User authentication state
- Login/logout actions
- Token management

### portfolioSlice
- Portfolio summary
- Positions array
- Loading states

### marketSlice
- Real-time quotes
- Selected symbol
- Market data cache

### ordersSlice
- Order history
- Pending orders
- Order CRUD operations

## 🧪 Testing

Tests use Vitest and React Testing Library:

```bash
# Run all tests
npm test

# Run specific test file
npm test -- Dashboard.test.tsx

# Watch mode
npm test -- --watch

# Coverage report
npm run test:coverage
```

## 📦 Dependencies

### Production Dependencies
- `@reduxjs/toolkit` - Redux state management
- `axios` - HTTP client
- `react-router-dom` - Routing
- `socket.io-client` - WebSocket
- `react-hot-toast` - Toast notifications
- `lucide-react` - Icon library
- `recharts` - Charting library
- `react-hook-form` + `zod` - Form validation
- `date-fns` - Date utilities
- `clsx` + `tailwind-merge` - Class name utilities

### Dev Dependencies
- `vite` - Build tool
- `typescript` - Type checking
- `eslint` - Linting
- `tailwindcss` + `autoprefixer` + `postcss` - Styling
- `vitest` - Testing framework

## 🚀 Deployment

### Build

```bash
npm run build
```

### Output

Static files in `dist/` directory ready for deployment to:
- Vercel
- Netlify
- AWS S3 + CloudFront
- Any static hosting provider

### Environment Variables for Production

```env
VITE_API_URL=https://api.speedtrade.com
VITE_WS_URL=wss://api.speedtrade.com
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### TypeScript Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Build Errors

```bash
# Clean build cache
rm -rf dist .vite
npm run build
```

## 📝 Code Style

- Use functional components with hooks
- TypeScript strict mode enabled
- ESLint + Prettier for formatting
- 2-space indentation
- Single quotes for strings
- Trailing commas in objects/arrays

## 🔗 Related Documentation

- [Backend API Documentation](../backend/README.md)
- [API Endpoints Guide](../docs/API_GUIDE.md)
- [Deployment Guide](../docs/DEPLOYMENT.md)
- [Architecture Overview](../docs/ARCHITECTURE.md)

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ using React + TypeScript + Vite**
