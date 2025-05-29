import React, { useState, useEffect } from 'react';
import { Search, Star, Heart, ThumbsDown, User, Film, Clock, TrendingUp } from 'lucide-react';

const API_BASE_URL = 'http://localhost:5001';

/**
 * Componente principal de la aplicación
 */
const MovieApp = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [activeTab, setActiveTab] = useState('home');
  const [movies, setMovies] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  /**  
   * Para cargar el usuario actual al iniciar la aplicación
   */
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

  /**
   * Carga las recomendaciones basadas en el usuario actual
   * @returns 
   */
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
      
      
      loadRecommendations();
    } catch (error) {
      console.error('Error registrando interacción:', error);
    }
  };

  /**
   * Buscar películas basadas en la consulta de búsqueda
   * @returns 
   */
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
}