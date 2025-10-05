import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/authService';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await authService.register({ username, email, password });
      setSuccess(true);
      setTimeout(() => navigate('/login'), 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '400px', marginTop: '100px' }}>
      <div className="card">
        <h1 style={{ marginBottom: '24px', textAlign: 'center' }}>SpeedTrade</h1>
        <h2 style={{ marginBottom: '24px', textAlign: 'center', fontSize: '20px' }}>Register</h2>
        
        {success ? (
          <div className="success" style={{ textAlign: 'center' }}>
            Registration successful! Redirecting to login...
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <input
              className="input"
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            
            <input
              className="input"
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            
            <input
              className="input"
              type="password"
              placeholder="Password (min 8 characters)"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              minLength={8}
              required
            />
            
            {error && <div className="error">{error}</div>}
            
            <button className="button" type="submit" disabled={isLoading} style={{ width: '100%', marginTop: '16px' }}>
              {isLoading ? 'Registering...' : 'Register'}
            </button>
          </form>
        )}
        
        <p style={{ marginTop: '16px', textAlign: 'center' }}>
          Already have an account? <Link to="/login" style={{ color: '#4c6ef5' }}>Login</Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
