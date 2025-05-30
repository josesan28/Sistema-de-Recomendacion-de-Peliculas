import React, { useState, useEffect } from 'react';
import { Search, Star, Heart, ThumbsDown, User, Film, Clock, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';

const API_BASE_URL = 'http://localhost:5001';

// Componente principal de la aplicación
const MovieApp = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [activeTab, setActiveTab] = useState('home');
  const [movies, setMovies] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [notification, setNotification] = useState(null);

  // Función para mostrar notificaciones
  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

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
      const response = await fetch(`${API_BASE_URL}/movies?limit=150`);
      if (!response.ok) throw new Error('Error cargando películas');
      const data = await response.json();
      setMovies(data);
    } catch (error) {
      console.error('Error cargando películas:', error);
      showNotification('Error cargando películas', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadRecommendations = async () => {
    if (!currentUser?.id) return;
    
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/recommendations/${currentUser.id}?limit=8`);
      if (!response.ok) throw new Error('Error cargando recomendaciones');
      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (error) {
      console.error('Error cargando recomendaciones:', error);
      showNotification('Error cargando recomendaciones', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleInteraction = async (movieId, type) => {
    if (!currentUser?.id) {
      showNotification('Debes iniciar sesión para interactuar', 'error');
      return;
    }

    try {
      console.log('Enviando interacción:', { user_id: currentUser.id, movie_id: movieId, type });
      
      const response = await fetch(`${API_BASE_URL}/interact`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          user_id: currentUser.id,
          movie_id: movieId,
          type: type
        }),
      });

      const data = await response.json();
      console.log('Respuesta del servidor:', data);

      if (response.ok) {
        showNotification(
          type === 'like' ? '¡Te gusta esta película!' : 'Marcada como no me gusta',
          'success'
        );
        // Recargar recomendaciones después de la interacción
        setTimeout(() => loadRecommendations(), 1000);
      } else {
        throw new Error(data.error || 'Error en la interacción');
      }
    } catch (error) {
      console.error('Error registrando interacción:', error);
      showNotification('Error registrando tu preferencia', 'error');
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
      if (!response.ok) throw new Error('Error en la búsqueda');
      const data = await response.json();
      setMovies(data);
    } catch (error) {
      console.error('Error en búsqueda:', error);
      showNotification('Error en la búsqueda', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Componente de notificación
  const Notification = ({ notification }) => {
    if (!notification) return null;

    const isError = notification.type === 'error';
    const bgColor = isError ? 'bg-red-100 border-red-400 text-red-700' : 'bg-green-100 border-green-400 text-green-700';
    
    return (
      <div className={`fixed top-4 right-4 z-50 border px-4 py-3 rounded ${bgColor}`}>
        <div className="flex items-center">
          {isError ? (
            <AlertCircle className="h-4 w-4 mr-2" />
          ) : (
            <CheckCircle className="h-4 w-4 mr-2" />
          )}
          <span>{notification.message}</span>
        </div>
      </div>
    );
  };

  // Componente de login
  const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [isLogin, setIsLogin] = useState(true);

    const handleAuth = async () => {
      if (!email || !password) {
        showNotification('Email y contraseña son requeridos', 'error');
        return;
      }

      try {
        const endpoint = isLogin ? '/login' : '/register';
        const body = isLogin 
          ? { email, password }
          : { email, password, name: name || email.split('@')[0] };

        console.log('Enviando datos de autenticación:', body);

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(body),
        });

        const data = await response.json();
        console.log('Respuesta de autenticación:', data);
        
        if (response.ok) {
          const userData = {
            id: data.user?.id || `user_${Date.now()}`,
            email: data.user?.email || email,
            name: data.user?.name || name || email.split('@')[0]
          };
          setCurrentUser(userData);
          showNotification(
            isLogin ? '¡Bienvenido de vuelta!' : '¡Cuenta creada exitosamente!',
            'success'
          );
        } else {
          throw new Error(data.error || 'Error en autenticación');
        }
      } catch (error) {
        console.error('Error de autenticación:', error);
        showNotification(error.message || 'Error en autenticación', 'error');
        
        if (error.message.includes('fetch')) {
          const userData = {
            id: `user_${Date.now()}`, 
            email: email,
            name: name || email.split('@')[0] || 'Usuario Demo'
          };
          setCurrentUser(userData);
          showNotification('Modo demo activado - Usuario creado automáticamente', 'success');
        }
      }
    };

    const handleKeyPress = (e) => {
      if (e.key === 'Enter') {
        handleAuth();
      }
    };

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100">
          <div className="text-center mb-8">
            <Film className="mx-auto h-16 w-16 text-blue-600 mb-4" />
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              MovieRec
            </h1>
            <p className="text-gray-600">
              {isLogin ? 'Inicia sesión para continuar' : 'Crea tu cuenta'}
            </p>
          </div>

          <div className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nombre
                </label>
                <input
                  type="text"
                  placeholder="Tu nombre"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            )}
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                placeholder="tu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onKeyPress={handleKeyPress}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Contraseña
              </label>
              <input
                type="password"
                placeholder="Tu contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyPress={handleKeyPress}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <button
              onClick={handleAuth}
              className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition-colors font-medium text-lg"
            >
              {isLogin ? 'Iniciar Sesión' : 'Crear Cuenta'}
            </button>
          </div>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              {isLogin ? '¿No tienes cuenta?' : '¿Ya tienes cuenta?'}
            </p>
            <button
              type="button"
              onClick={() => setIsLogin(!isLogin)}
              className="mt-1 text-blue-600 hover:text-blue-700 font-medium"
            >
              {isLogin ? 'Crear cuenta nueva' : 'Iniciar sesión'}
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Componente de tarjeta de película
  const MovieCard = ({ movie, showInteractions = false }) => {
    const [isInteracting, setIsInteracting] = useState(false);

    const handleMovieInteraction = async (type) => {
      setIsInteracting(true);
      await handleInteraction(movie.id, type);
      setIsInteracting(false);
    };

    return (
      <div className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all duration-300 border border-gray-100">
        <div className="mb-4">
          <h3 className="font-bold text-xl text-gray-900 mb-2">{movie.title}</h3>
          {movie.year && (
            <p className="text-sm text-gray-600 flex items-center">
              <Clock className="h-4 w-4 mr-1" />
              {movie.year}
            </p>
          )}
        </div>
        
        {movie.genres && movie.genres.length > 0 && (
          <div className="mb-3">
            <div className="flex flex-wrap gap-2">
              {movie.genres.slice(0, 3).map((genre, i) => (
                <span key={i} className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium">
                  {genre}
                </span>
              ))}
            </div>
          </div>
        )}

        {movie.directors && movie.directors.length > 0 && (
          <p className="text-sm text-gray-600 mb-2">
            <strong>Director:</strong> {movie.directors[0]}
          </p>
        )}

        {movie.actors && movie.actors.length > 0 && (
          <p className="text-sm text-gray-600 mb-3">
            <strong>Actores:</strong> {movie.actors.slice(0, 2).join(', ')}
            {movie.actors.length > 2 && '...'}
          </p>
        )}

        {showInteractions && (
          <div className="flex space-x-3 pt-4 border-t border-gray-100">
            <button
              onClick={() => handleMovieInteraction('like')}
              disabled={isInteracting}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 text-sm font-medium ${
                isInteracting 
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-green-100 text-green-700 hover:bg-green-200 hover:scale-105'
              }`}
            >
              <Heart className="h-4 w-4" />
              <span>Me gusta</span>
            </button>
            <button
              onClick={() => handleMovieInteraction('dislike')}
              disabled={isInteracting}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 text-sm font-medium ${
                isInteracting 
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-red-100 text-red-700 hover:bg-red-200 hover:scale-105'
              }`}
            >
              <ThumbsDown className="h-4 w-4" />
              <span>No me gusta</span>
            </button>
          </div>
        )}
      </div>
    );
  };

  // Navegación
  const Navigation = () => (
    <nav className="bg-white shadow-lg border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-3">
              <Film className="h-8 w-8 text-blue-600" />
              <span className="text-2xl font-bold text-gray-900">MovieRec</span>
            </div>
            
            <div className="hidden md:flex space-x-1">
              <button
                onClick={() => setActiveTab('home')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  activeTab === 'home' 
                    ? 'bg-blue-600 text-white shadow-md' 
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Explorar
              </button>
              <button
                onClick={() => setActiveTab('recommendations')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  activeTab === 'recommendations' 
                    ? 'bg-blue-600 text-white shadow-md' 
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Recomendadas
              </button>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center space-x-2 bg-gray-100 px-3 py-2 rounded-lg">
              <User className="h-4 w-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">{currentUser?.name}</span>
            </div>
            <button
              onClick={() => {
                setCurrentUser(null);
                setMovies([]);
                setRecommendations([]);
                showNotification('Sesión cerrada', 'success');
              }}
              className="text-sm text-gray-500 hover:text-gray-700 font-medium"
            >
              Salir
            </button>
          </div>
        </div>
      </div>
    </nav>
  );

  // Contenido principal
  const MainContent = () => (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <Notification notification={notification} />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Barra de búsqueda */}
        <div className="mb-8">
          <div className="flex space-x-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar películas..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && searchMovies()}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={searchMovies}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Buscar
            </button>
          </div>
        </div>

        {/* Contenido por pestañas */}
        {activeTab === 'home' && (
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Explorar Películas</h2>
              <button
                onClick={loadMovies}
                className="text-blue-600 hover:text-blue-700 font-medium"
              >
                Actualizar
              </button>
            </div>
            
            {loading ? (
              <div className="flex justify-center items-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {movies.map((movie) => (
                  <MovieCard 
                    key={movie.id} 
                    movie={movie} 
                    showInteractions={true}
                  />
                ))}
              </div>
            )}
            
            {!loading && movies.length === 0 && (
              <div className="text-center py-12">
                <Film className="mx-auto h-16 w-16 text-gray-400 mb-4" />
                <p className="text-gray-600 text-lg">No se encontraron películas</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Recomendaciones Personalizadas</h2>
              <button
                onClick={loadRecommendations}
                className="text-blue-600 hover:text-blue-700 font-medium"
              >
                Actualizar
              </button>
            </div>
            
            {recommendations.length > 0 ? (
              <div>
                <div className="mb-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <p className="text-blue-800 text-sm">
                    <TrendingUp className="inline h-4 w-4 mr-1" />
                    Estas recomendaciones se basan en tus preferencias y películas que te han gustado.
                  </p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {recommendations.map((movie) => (
                    <MovieCard 
                      key={movie.id} 
                      movie={movie} 
                      showInteractions={true}
                    />
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <TrendingUp className="mx-auto h-16 w-16 text-gray-400 mb-4" />
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  No hay recomendaciones aún
                </h3>
                <p className="text-gray-600 mb-6">
                  Marca algunas películas como "me gusta" para obtener recomendaciones personalizadas
                </p>
                <button
                  onClick={() => setActiveTab('home')}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                >
                  Explorar Películas
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );

  // Renderizado principal
  if (!currentUser) {
    return <LoginForm />;
  }

  return <MainContent />;
};

export default MovieApp;