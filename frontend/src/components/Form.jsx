import { useState } from "react";
import { ACCESS_TOKEN, REFRESH_TOKEN, BASE_URL } from "../constants";
import axios from "axios";
import { useNavigate } from "react-router-dom";  // useNavigate import et

function Form({ method }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState(""); // Email alanı
  const [firstName, setFirstName] = useState(""); // Ad alanı
  const [lastName, setLastName] = useState(""); // Soyad alanı
  const [confirmPassword, setConfirmPassword] = useState(""); // Şifre tekrar alanı
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();  // Yönlendirme için navigate kullan

  const isRegister = method === "register"; // Register modunu kontrol ediyor

  const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
    
      try {
        if (isRegister) {
          // Kayıt işlemi
          await axios.post(`${BASE_URL}/register`, {
            username,
            password,
            email,
            first_name: firstName,
            last_name: lastName,
            confirmPassword,
          });
          alert("Registration successful! Please login.");
        } else {
          // Giriş işlemi
          const response = await axios.post(`${BASE_URL}/login`, {
            username,
            password,
          });
          localStorage.setItem(ACCESS_TOKEN, response.data.access);
          localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
          alert("Login successful!");
    
          // Doğru bir frontend rotasına yönlendirme
          navigate("/"); // BASE_URL kaldırıldı
        }
      } catch (error) {
        alert(error.response?.data?.detail || "Something went wrong");
      } finally {
        setLoading(false);
      }
    };
  

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Username */}
      <input
        className="w-full p-3 border border-gray-300 rounded"
        type="text"
        value={username}
        name="username"
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />

      {/* Password */}
      <input
        className="w-full p-3 border border-gray-300 rounded"
        type="password"
        value={password}
        name="password"
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />

      {/* Ek alanlar (Register için) */}
      {isRegister && (
        <>
          {/* Email */}
          <input
            className="w-full p-3 border border-gray-300 rounded"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
          />

          {/* Ad ve Soyad */}
          <div className="flex space-x-4">
            <input
              className="w-full p-3 border border-gray-300 rounded"
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              placeholder="First Name"
            />
            <input
              className="w-full p-3 border border-gray-300 rounded"
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              placeholder="Last Name"
            />
          </div>

          {/* Şifre Tekrar */}
          <input
            className="w-full p-3 border border-gray-300 rounded"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm Password"
          />
        </>
      )}

      {/* Submit Butonu */}
      <button
        className="w-full p-3 bg-blue-500 text-white rounded hover:bg-blue-600 transition transform hover:-translate-y-1 motion-reduce:transition-none motion-reduce:hover:transform-none ..."
        type="submit"
        disabled={loading}
      >
        {loading ? "Loading..." : isRegister ? "Register" : "Login"}
      </button>
    </form>
  );
}

export default Form;
