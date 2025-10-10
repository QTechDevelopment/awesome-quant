import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { logout } from '../store/slices/authSlice';

function DashboardPage() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const user = useAppSelector((state) => state.auth.user);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  return (
    <div className="container">
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
        <h1>SpeedTrade Dashboard</h1>
        <button className="button" onClick={handleLogout}>Logout</button>
      </header>

      <div className="card" style={{ marginBottom: '24px' }}>
        <h2 style={{ marginBottom: '16px' }}>Welcome, {user?.username}!</h2>
        <p>Your trading dashboard is under construction.</p>
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <h3 style={{ marginBottom: '16px' }}>Portfolio Summary</h3>
        <p style={{ color: '#adb5bd' }}>Portfolio tracking coming soon...</p>
      </div>

      <div className="card">
        <h3 style={{ marginBottom: '16px' }}>Recent Orders</h3>
        <p style={{ color: '#adb5bd' }}>No orders yet. Start trading to see your orders here.</p>
      </div>
    </div>
  );
}

export default DashboardPage;
