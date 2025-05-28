const API_BASE_URL = 'http://localhost:5000';

class ApiService {
  static async register(userData) {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Error en el registro');
    }
    
    return response.json();
  }

  static async login(credentials) {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Error en el login');
    }
    
    return response.json();
  }

  static async getAllMovies(limit = 50) {
    const response = await fetch(`${API_BASE_URL}/movies?limit=${limit}`);
    if (!response.ok) throw new Error('Error al obtener películas');
    return response.json();
  }

  static async getMovie(movieId) {
    const response = await fetch(`${API_BASE_URL}/movies/${movieId}`);
    if (!response.ok) throw new Error('Error al obtener película');
    return response.json();
  }

  static async searchMovies(query) {
    const response = await fetch(`${API_BASE_URL}/movies/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error('Error en la búsqueda');
    return response.json();
  }

  static async advancedSearch(params) {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value && value.trim()) {
        queryParams.append(key, value);
      }
    });
    
    const response = await fetch(`${API_BASE_URL}/movies/search/advanced?${queryParams}`);
    if (!response.ok) throw new Error('Error en la búsqueda avanzada');
    return response.json();
  }

  static async getTopMovies(limit = 10) {
    const response = await fetch(`${API_BASE_URL}/movies/top?limit=${limit}`);
    if (!response.ok) throw new Error('Error al obtener top películas');
    return response.json();
  }

  static async getLatestMovies(limit = 10) {
    const response = await fetch(`${API_BASE_URL}/movies/latest?limit=${limit}`);
    if (!response.ok) throw new Error('Error al obtener últimas películas');
    return response.json();
  }

  static async getMoviesBySeason(season) {
    const response = await fetch(`${API_BASE_URL}/movies/season/${encodeURIComponent(season)}`);
    if (!response.ok) throw new Error('Error al obtener películas por temporada');
    return response.json();
  }

  static async addInteraction(userId, movieId, type) {
    const response = await fetch(`${API_BASE_URL}/interact`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        movie_id: movieId,
        type: type
      }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Error al registrar interacción');
    }
    
    return response.json();
  }

  static async getRecommendations(userId, limit = 10) {
    const response = await fetch(`${API_BASE_URL}/recommendations/${userId}?limit=${limit}`);
    if (!response.ok) throw new Error('Error al obtener recomendaciones');
    return response.json();
  }

  static async getRecommendationExplanation(userId, movieId) {
    const response = await fetch(`${API_BASE_URL}/recommendations/${userId}/explain/${movieId}`);
    if (!response.ok) throw new Error('Error al obtener explicación');
    return response.json();
  }

  static async getAllGenres() {
    const response = await fetch(`${API_BASE_URL}/genres`);
    if (!response.ok) throw new Error('Error al obtener géneros');
    return response.json();
  }

  static async getAllActors() {
    const response = await fetch(`${API_BASE_URL}/actors`);
    if (!response.ok) throw new Error('Error al obtener actores');
    return response.json();
  }

  static async getAllDirectors() {
    const response = await fetch(`${API_BASE_URL}/directors`);
    if (!response.ok) throw new Error('Error al obtener directores');
    return response.json();
  }

  static async searchActors(query) {
    const response = await fetch(`${API_BASE_URL}/actors/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error('Error al buscar actores');
    return response.json();
  }
}

export default ApiService;