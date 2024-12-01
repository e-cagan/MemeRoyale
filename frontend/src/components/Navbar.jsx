import { Link, useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants';

function Navbar() {
  const navigate = useNavigate();

  // Logout işlemi
  const handleLogout = () => {
    // LocalStorage'dan token'ları sil
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem(REFRESH_TOKEN);

    // Kullanıcıyı login sayfasına yönlendir
    navigate("/login");
  };

  return (
    <nav className="bg-blue-500 p-4 text-white">
      <div className="flex justify-between items-center">
        {/* Logo veya Ana Sayfaya Yönlendirme */}
        <Link to="/" className="text-2xl">Home</Link>

        {/* Giriş yapılmışsa logout, yapılmamışsa giriş ve kayıt */}
        <div>
          {localStorage.getItem(ACCESS_TOKEN) ? (
            <button
              onClick={handleLogout}
              className="bg-red-500 p-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          ) : (
            <div>
              <Link to="/login" className="mx-2">Login</Link>
              <Link to="/register" className="mx-2">Register</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
