import React, { useState, useEffect } from 'react';
import { 
  StyleSheet, 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  FlatList, 
  ActivityIndicator, 
  SafeAreaView, 
  StatusBar,
  Dimensions
} from 'react-native';
import { Image } from 'expo-image';
import { Search, Popcorn, Star, Calendar } from 'lucide-react-native';
import axios from 'axios';
import { API_URL } from '../../backend_config';

const { width } = Dimensions.get('window');
const COLUMN_WIDTH = (width - 40) / 2;

export default function HomeScreen() {
  const [search, setSearch] = useState('');
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [allMovies, setAllMovies] = useState([]);
  const [filteredMovies, setFilteredMovies] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);

  const [error, setError] = useState(false);

  useEffect(() => {
    fetchAllMovies();
  }, []);

  const fetchAllMovies = async () => {
    try {
      setError(false);
      console.log("Connecting to:", `${API_URL}/movies`);
      const response = await axios.get(`${API_URL}/movies`, { timeout: 10000 });
      setAllMovies(response.data);
      console.log("Movie list loaded:", response.data.length);
    } catch (error) {
      console.error("Connection failed:", error.message);
      setError(true);
    }
  };

  const handleSearchChange = (text: string) => {
    setSearch(text);
    if (text.length > 1) {
      const filtered = allMovies
        .filter(m => m.title.toLowerCase().includes(text.toLowerCase()))
        .slice(0, 10);
      setFilteredMovies(filtered);
      setShowDropdown(true);
    } else {
      setShowDropdown(false);
    }
  };

  const getRecommendations = async (title: string) => {
    setLoading(true);
    setSearch(title);
    setShowDropdown(false);
    try {
      const response = await axios.get(`${API_URL}/recommend/${encodeURIComponent(title)}`);
      setMovies(response.data.recommendations);
    } catch (error) {
      alert("Movie not found or server error");
    } finally {
      setLoading(false);
    }
  };

  const renderMovie = ({ item }) => (
    <View style={styles.card}>
      <Image 
        source={{ uri: item.poster_url }} 
        style={styles.poster}
        contentFit="cover"
        transition={500}
      />
      <View style={styles.cardInfo}>
        <Text style={styles.movieTitle} numberOfLines={2}>{item.title}</Text>
        <View style={styles.metaRow}>
          <View style={styles.iconText}>
            <Star size={14} color="#FFD700" fill="#FFD700" />
            <Text style={styles.metaText}>{item.rating.toFixed(1)}</Text>
          </View>
          {item.year && (
            <View style={styles.iconText}>
              <Calendar size={14} color="#AAAAAA" />
              <Text style={styles.metaText}>{item.year}</Text>
            </View>
          )}
        </View>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      
      <View style={[styles.mainWrapper, movies.length === 0 && styles.centeredWrapper]}>
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.logoRow}>
            <Popcorn color="#FF3333" size={40} strokeWidth={2.5} />
            <Text style={styles.logoText}>MovieCafe<Text style={styles.logoTextAI}> AI</Text></Text>
          </View>
          <Text style={styles.subtitle}>Discover your next cinematic masterpiece</Text>
        </View>

        {/* Search Section */}
        <View style={styles.searchContainer}>
          <View style={styles.inputWrapper}>
            <Search color="#888" size={20} style={styles.searchIcon} />
            <TextInput
              style={styles.input}
              placeholder="Search for a movie..."
              placeholderTextColor="#888"
              value={search}
              onChangeText={handleSearchChange}
            />
            {loading && <ActivityIndicator color="#FF3333" style={styles.loader} />}
          </View>

          {showDropdown && (
            <View style={styles.dropdown}>
              {filteredMovies.map((item) => (
                <TouchableOpacity 
                  key={item.movie_id} 
                  style={styles.dropdownItem}
                  onPress={() => getRecommendations(item.title)}
                >
                  <Text style={styles.dropdownText}>{item.title}</Text>
                </TouchableOpacity>
              ))}
            </View>
          )}
        </View>
      </View>

      {/* Results */}
      {error && (
        <View style={styles.errorBanner}>
          <Text style={styles.errorText}>Unable to connect to PC backend. Verify Wi-Fi and IP.</Text>
          <TouchableOpacity onPress={fetchAllMovies} style={styles.retryButton}>
            <Text style={styles.retryText}>Retry</Text>
          </TouchableOpacity>
        </View>
      )}

      {movies.length > 0 ? (
        <FlatList
          data={movies}
          renderItem={renderMovie}
          keyExtractor={(item) => item.id.toString()}
          numColumns={2}
          contentContainerStyle={styles.listContent}
          columnWrapperStyle={styles.columnWrapper}
          showsVerticalScrollIndicator={false}
          ListHeaderComponent={<Text style={styles.resultsTitle}>Recommended for you</Text>}
        />
      ) : (
        <View style={styles.emptyState}>
          {!loading && (
            <>
              <Popcorn color="#333" size={80} style={{ opacity: 0.5 }} />
              <Text style={styles.emptyText}>Start searching to get personalized recommendations</Text>
            </>
          )}
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0A0A0A',
  },
  mainWrapper: {
    width: '100%',
    transition: 'all 0.5s ease',
  },
  centeredWrapper: {
    flex: 0.8,
    justifyContent: 'center',
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 20,
    marginBottom: 20,
    alignItems: 'center',
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  logoText: {
    color: '#FFFFFF',
    fontSize: 34,
    fontWeight: '900',
    letterSpacing: 1,
  },
  logoTextAI: {
    color: '#FF3333',
  },
  subtitle: {
    color: '#AAAAAA',
    fontSize: 14,
    marginTop: 4,
  },
  searchContainer: {
    paddingHorizontal: 20,
    zIndex: 10,
    marginBottom: 10,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1E1E1E',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#333',
    paddingHorizontal: 15,
  },
  searchIcon: {
    marginRight: 10,
  },
  input: {
    flex: 1,
    height: 50,
    color: '#FFF',
    fontSize: 16,
  },
  loader: {
    marginLeft: 10,
  },
  dropdown: {
    position: 'absolute',
    top: 55,
    left: 20,
    right: 20,
    backgroundColor: '#1E1E1E',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#333',
    maxHeight: 250,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
  },
  dropdownItem: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#333',
  },
  dropdownText: {
    color: '#EEE',
    fontSize: 15,
  },
  resultsTitle: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 20,
    marginTop: 10,
  },
  listContent: {
    paddingHorizontal: 15,
    paddingBottom: 40,
  },
  columnWrapper: {
    justifyContent: 'space-between',
  },
  card: {
    width: COLUMN_WIDTH,
    backgroundColor: '#161616',
    borderRadius: 15,
    marginBottom: 20,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#222',
  },
  poster: {
    width: '100%',
    height: COLUMN_WIDTH * 1.5,
  },
  cardInfo: {
    padding: 12,
  },
  movieTitle: {
    color: '#FFF',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
    minHeight: 40,
  },
  metaRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  iconText: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  metaText: {
    color: '#AAA',
    fontSize: 11,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  emptyText: {
    color: '#555',
    textAlign: 'center',
    marginTop: 20,
    fontSize: 16,
    lineHeight: 24,
  },
  errorBanner: {
    backgroundColor: '#300',
    padding: 15,
    marginHorizontal: 20,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#F33',
  },
  errorText: {
    color: '#FAA',
    fontSize: 13,
    textAlign: 'center',
    marginBottom: 10,
  },
  retryButton: {
    backgroundColor: '#F33',
    paddingHorizontal: 20,
    paddingVertical: 8,
    borderRadius: 5,
  },
  retryText: {
    color: '#FFF',
    fontSize: 12,
    fontWeight: '700',
  }
});
