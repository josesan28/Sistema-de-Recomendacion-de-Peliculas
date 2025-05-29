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

  // Componente de tarjeta de película
  const MovieCard = ({ movie, showInteractions = false }) => (
    <div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
      <h3 className="font-semibold text-lg mb-2 text-gray-900">{movie.title}</h3>
      <p className="text-sm text-gray-600 mb-2">Año: {movie.year}</p>
      
      {movie.genres && movie.genres.length > 0 && (
        <div className="mb-2">
          <div className="flex flex-wrap gap-1">
            {movie.genres.slice(0, 3).map((genre, i) => (
              <span key={i} className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                {genre}
              </span>
            ))}
          </div>
        </div>
      )}

      {movie.directors && movie.directors.length > 0 && (
        <p className="text-sm text-gray-600 mb-2">
          Director: {movie.directors[0]}
        </p>
      )}

      {movie.actors && movie.actors.length > 0 && (
        <p className="text-sm text-gray-600 mb-3">
          Actores: {movie.actors.slice(0, 2).join(', ')}
        </p>
      )}

      {movie.score && (
        <div className="mb-3 flex items-center">
          <Star className="h-4 w-4 text-yellow-500 mr-1" />
          <span className="text-sm font-medium">{movie.score}</span>
        </div>
      )}

      {showInteractions && (
        <div className="flex space-x-2 pt-2 border-t">
          <button
            onClick={() => handleInteraction(movie.id, 'like')}
            className="flex items-center space-x-1 px-3 py-1 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors text-sm"
          >
            <Heart className="h-4 w-4" />
            <span>Me gusta</span>
          </button>
          <button
            onClick={() => handleInteraction(movie.id, 'dislike')}
            className="flex items-center space-x-1 px-3 py-1 bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors text-sm"
          >
            <ThumbsDown className="h-4 w-4" />
            <span>No me gusta</span>
          </button>
        </div>
      )}
    </div>
  );

  // Navegación
  const Navigation = () => (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-2">
              <Film className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">MovieRec</span>
            </div>
            
            <div className="flex space-x-4">
              <button
                onClick={() => setActiveTab('home')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === 'home' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Explorar
              </button>
              <button
                onClick={() => setActiveTab('recommendations')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === 'recommendations' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Recomendadas
              </button>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <User className="h-4 w-4" />
              <span>{currentUser?.name}</span>
            </div>
            <button
              onClick={() => setCurrentUser(null)}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Salir
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}