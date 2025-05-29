import React, { useState, useEffect } from 'react';
import { Search, Star, Heart, ThumbsDown, User, Film, Clock, TrendingUp } from 'lucide-react';

const API_BASE_URL = 'http://localhost:5001';

//Componente principal de la aplicación
const MovieApp = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [activeTab, setActiveTab] = useState('home');
  const [movies, setMovies] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Cargar el usuario inicialmente
  useEffect(() => {
    if (currentUser) {
      loadMovies();
      loadRecommendations();
    }
  }, [currentUser]);

  const loadMovies = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/movies?limit=20`);
      const data = await response.json();
      setMovies(data);
    } catch (error) {
      console.error('Error cargando películas:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadRecommendations = async () => {
    if (!currentUser?.id) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/recommendations/${currentUser.id}?limit=8`);
      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (error) {
      console.error('Error cargando recomendaciones:', error);
    }
  };

  const handleInteraction = async (movieId, type) => {
    if (!currentUser?.id) return;

    try {
      await fetch(`${API_BASE_URL}/interact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: currentUser.id,
          movie_id: movieId,
          type: type
        }),
      });
      
      //Recargar recomendaciones después de la interacción
      loadRecommendations();
    } catch (error) {
      console.error('Error registrando interacción:', error);
    }
  };

  const searchMovies = async () => {
    if (!searchQuery.trim()) {
      loadMovies();
      return;
    }

    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/movies/search?q=${encodeURIComponent(searchQuery)}`);
      const data = await response.json();
      setMovies(data);
    } catch (error) {
      console.error('Error en búsqueda:', error);
    } finally {
      setLoading(false);
    }
  };

  // Componente de login simple
  const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [isLogin, setIsLogin] = useState(true);

    const handleAuth = async () => {
      try {
        const endpoint = isLogin ? '/login' : '/register';
        const body = isLogin 
          ? { email, password }
          : { email, password, name };

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });

        const data = await response.json();
        
        if (response.ok) {
          setCurrentUser({ 
            id: data.user?.id || 'u1', 
            email: data.user?.email || email,
            name: data.user?.name || name 
          });
        } else {
          alert(data.error || 'Error en autenticación');
        }
      } catch (error) {
        console.error('Error:', error);
        
        setCurrentUser({ 
          id: 'u1', 
          email: email,
          name: name || 'Usuario' 
        });
      }
    };

    const handleKeyPress = (e) => {
      if (e.key === 'Enter') {
        handleAuth();
      }
    };

    return (
      <div className="min-h-screen bg-blue-50 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
          <div className="text-center mb-6">
            <Film className="mx-auto h-12 w-12 text-blue-600 mb-4" />
            <h1 className="text-2xl font-bold text-gray-900">
              {isLogin ? 'Iniciar Sesión' : 'Crear Cuenta'}
            </h1>
          </div>

          <div className="space-y-4">
            {!isLogin && (
              <input
                type="text"
                placeholder="Nombre"
                value={name}
                onChange={(e) => setName(e.target.value)}
                onKeyPress={handleKeyPress}
                className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            )}
            
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyPress={handleKeyPress}
              className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            
            <input
              type="password"
              placeholder="Contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyPress={handleKeyPress}
              className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            
            <button
              onClick={handleAuth}
              className="w-full bg-blue-600 text-white p-3 rounded-md hover:bg-blue-700 transition-colors"
            >
              {isLogin ? 'Entrar' : 'Registrarse'}
            </button>
          </div>

          <p className="text-center mt-4 text-sm text-gray-600">
            {isLogin ? '¿No tienes cuenta?' : '¿Ya tienes cuenta?'}
            <button
              type="button"
              onClick={() => setIsLogin(!isLogin)}
              className="ml-1 text-blue-600 hover:underline"
            >
              {isLogin ? 'Regístrate' : 'Inicia sesión'}
            </button>
          </p>
        </div>
      </div>
    );
  };
}