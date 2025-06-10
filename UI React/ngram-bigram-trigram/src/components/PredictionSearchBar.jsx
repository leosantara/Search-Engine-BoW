import React, { useState, useEffect, useRef, useCallback } from 'react';

const API_BASE_URL = 'http://127.0.0.1:5050/api'; 

function PredictionSearchBar() {
    const [searchTerm, setSearchTerm] = useState('');
    const [predictions, setPredictions] = useState([]);
    const [loading, setLoading] = useState(false); // Untuk prediksi
    const [error, setError] = useState(null); // Untuk prediksi
    const debounceTimeoutRef = useRef(null); 

    const [searchResults, setSearchResults] = useState([]); 
    const [searching, setSearching] = useState(false);
    const [searchError, setSearchError] = useState(null); 

    const [showPredictions, setShowPredictions] = useState(false); 

    const fetchPredictions = useCallback(async (query) => {
        const trimmedQuery = query.trimEnd();

        if (trimmedQuery.length === 0) {
            setPredictions([]);
            setLoading(false);
            return;
        }

        setLoading(true);
        setError(null);
        setSearchResults([]); 

        try {
            const requestUrl = `${API_BASE_URL}/predict?query=${encodeURIComponent(trimmedQuery)}`;
            console.log("Fetching predictions from URL:", requestUrl);
            const response = await fetch(requestUrl);
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, Response: ${errorText}`);
            }
            const data = await response.json();
            setPredictions(data);
        } catch (err) {
            console.error("Gagal mengambil prediksi:", err);
            setError("Gagal mengambil prediksi. Pastikan backend berjalan dan merespons JSON yang valid.");
            setPredictions([]);
        } finally {
            setLoading(false);
        }
    }, []);

    const fetchSearchResults = useCallback(async (query) => {
        const trimmedQuery = query.trim();

        if (trimmedQuery.length === 0) {
            setSearchResults([]);
            setSearching(false);
            return;
        }

        setSearching(true);
        setSearchError(null);
        setPredictions([]); // Hapus prediksi saat melakukan pencarian
        setShowPredictions(false); 

        try {
            const searchApiUrl = `${API_BASE_URL}/search?query=${encodeURIComponent(trimmedQuery)}`;
            console.log("Fetching search results from URL:", searchApiUrl);
            const response = await fetch(searchApiUrl);

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, Response: ${errorText}`);
            }
            const data = await response.json();
            setSearchResults(data);
        } catch (err) {
            console.error("Gagal mengambil hasil pencarian:", err);
            setSearchError("Gagal mengambil hasil pencarian. Pastikan backend berjalan.");
            setSearchResults([]);
        } finally {
            setSearching(false);
        }
    }, []);

    useEffect(() => {
        if (debounceTimeoutRef.current) {
            clearTimeout(debounceTimeoutRef.current);
        }

        if (!searching && showPredictions) { 
            debounceTimeoutRef.current = setTimeout(() => {
                fetchPredictions(searchTerm);
            }, 300);
        }

        return () => {
            if (debounceTimeoutRef.current) {
                clearTimeout(debounceTimeoutRef.current);
            }
        };
    }, [searchTerm, fetchPredictions, searching, showPredictions]); 
    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Mencegah perilaku default pengiriman form
            fetchSearchResults(searchTerm); // Panggil fungsi pencarian
            setPredictions([]); // Hapus prediksi saat Enter ditekan
            setShowPredictions(false); // Sembunyikan daftar prediksi
        }
    };

    // Handle perubahan input
    const handleChange = (event) => {
        setSearchTerm(event.target.value);
        setSearchResults([]); // Hapus hasil pencarian saat input berubah
        setSearchError(null); // Reset error pencarian
        setShowPredictions(true); // Tampilkan prediksi saat mulai mengetik
    };

    const handleFocus = () => {
        setShowPredictions(true); 
        if (searchTerm.length > 0) {
            fetchPredictions(searchTerm);
        }
    };

    const handleBlur = () => {
        setTimeout(() => {
            setShowPredictions(false);
        }, 100); 
    };

    const findOverlap = (inputWords, predictionWords) => {
        let maxOverlap = 0;
        const maxLen = Math.min(inputWords.length, predictionWords.length, 3); 

        for (let i = 1; i <= maxLen; i++) {
            const inputSuffix = inputWords.slice(inputWords.length - i).join(' ');
            const predictionPrefix = predictionWords.slice(0, i).join(' ');

            if (inputSuffix === predictionPrefix) {
                maxOverlap = i;
            }
        }
        return maxOverlap;
    };

    const handlePredictionClick = (prediction) => {
        setSearchTerm(prevSearchTerm => {
            console.log("biji isinya apa hei:", prediction);
            const predictionString = Array.isArray(prediction) ? prediction.join(' ') : prediction;
            const trimmedPrevSearchTerm = prevSearchTerm.trimEnd();
            
            if (!trimmedPrevSearchTerm) {
                return predictionString + ' ';
            }

            const inputWords = trimmedPrevSearchTerm.split(' ');
            const predictionWords = predictionString.split(' ');
            const overlapCount = findOverlap(inputWords, predictionWords);

            let newSearchTermWords;

            if (overlapCount > 0) {
                newSearchTermWords = inputWords.slice(0, inputWords.length - overlapCount);
                newSearchTermWords.push(predictionString);
            } else if (predictionString.startsWith(trimmedPrevSearchTerm)) {
                newSearchTermWords = [predictionString];
            } else {
                newSearchTermWords = [...inputWords, predictionString];
            }
            
            return newSearchTermWords.join(' ') + ' ';
        });
        setPredictions([]); // Sembunyikan prediksi setelah diklik
        setShowPredictions(false); // Sembunyikan daftar prediksi
        setSearchResults([]); // Hapus hasil pencarian saat prediksi diklik
        setSearchError(null); // Reset error pencarian
    };

    return (
        <div style={styles.searchContainer}>
            <h1 style={styles.title}>Tugas Akhir NLP Kelompok 4</h1>
            <h2 style={styles.title}>Search Engine</h2>
            <input
                type="text"
                placeholder="Ketik sesuatu..."
                value={searchTerm}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
                onFocus={handleFocus}   
                onBlur={handleBlur}     
                style={styles.searchInput}
            />
            {loading && <p style={styles.statusText}>Memuat prediksi...</p>}
            {error && <p style={styles.errorText}>{error}</p>}

            {predictions.length > 0 && !loading && showPredictions && (
                <ul style={styles.predictionList}>
                    {predictions.map((prediction, index) => (
                        <li key={index} onClick={() => handlePredictionClick(prediction)} style={styles.predictionItem}>
                            {Array.isArray(prediction) ? prediction.join(' ') : prediction}
                        </li>
                    ))}
                </ul>
            )}

            {searching && <p style={styles.statusText}>Mencari...</p>}
            {searchError && <p style={styles.errorText}>{searchError}</p>}
            
            {searchResults.length > 0 && !searching && (
                <div style={styles.searchResultsContainer}>
                    <h2 style={styles.resultsTitle}>Hasil Pencarian:</h2>
                    {searchResults.map((result, index) => (
                        <div key={index} style={styles.searchResultItem}>
                            <p style={styles.resultDocName}>**Dokumen:** {result.document_name} (Baris: {result.sentence_number})</p>
                            <p style={styles.resultSentence}>"{result.sentence_text}"</p>
                            <p style={styles.resultScore}>Relevansi: {result.score}</p>
                        </div>
                    ))}
                </div>
            )}

            {!searching && !searchError && searchTerm.length > 0 && searchResults.length === 0 && (
                <p style={styles.statusText}>Tidak ada hasil yang ditemukan.</p>
            )}
        </div>
    );
}


const styles = {
    searchContainer: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '20px',
        fontFamily: 'Arial, sans-serif',
        maxWidth: '600px',
        margin: '50px auto',
        border: '1px solid #ddd',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
        backgroundColor: '#fff',
    },
    title: {
        color: '#333',
        marginBottom: '20px',
    },
    searchInput: {
        width: 'calc(100% - 40px)', 
        padding: '12px 20px',
        fontSize: '18px',
        borderRadius: '24px',
        border: '1px solid #dfe1e5',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        outline: 'none',
        marginBottom: '10px',
        transition: 'border-color 0.2s, box-shadow 0.2s',
    },
    searchInputFocus: {
        borderColor: '#4285f4',
        boxShadow: '0 2px 6px rgba(66, 133, 244, 0.2)',
    },
    predictionList: {
        listStyle: 'none',
        padding: '0',
        margin: '0',
        color: '#333',
        width: 'calc(100% - 40px)',
        border: '1px solid #dfe1e5',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        backgroundColor: '#fff',
        maxHeight: '200px',
        overflowY: 'auto',
    },
    predictionItem: {
        padding: '10px 20px',
        fontSize: '16px',
        cursor: 'pointer',
        borderBottom: '1px solid #eee',
    },
    predictionItemHover: {
        backgroundColor: '#f0f0f0',
    },
    statusText: {
        color: '#666',
        fontSize: '14px',
    },
    errorText: {
        color: 'red',
        fontSize: '14px',
    },

    searchResultsContainer: {
        marginTop: '20px',
        width: 'calc(100% - 40px)',
        borderTop: '1px solid #eee',
        paddingTop: '15px',
    },
    resultsTitle: {
        fontSize: '20px',
        color: '#333',
        marginBottom: '15px',
        textAlign: 'center',
    },
    searchResultItem: {
        backgroundColor: '#f9f9f9',
        border: '1px solid #ddd',
        borderRadius: '5px',
        padding: '10px 15px',
        marginBottom: '10px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
    },
    resultDocName: {
        fontWeight: 'bold',
        color: '#007bff',
        marginBottom: '5px',
    },
    resultSentence: {
        fontSize: '15px',
        color: '#555',
        marginBottom: '5px',
    },
    resultScore: {
        fontSize: '13px',
        color: '#888',
        textAlign: 'right',
    }
};

export default PredictionSearchBar;
