import React from "react";
import "./SearchResults.css"; // Ensure this file exists in the same directory

const SearchResults = ({ results }) => {
  // Ensure results is always an array
  const searchResults = Array.isArray(results?.results) ? results.results : [];

  if (searchResults.length === 0) {
    return <p>No results found.</p>;
  }

  return (
    <div className="results-container">
      {searchResults.map((result, index) => (
        <div key={index} className="result-item">
          <h3>
            <a href={result.url} target="_blank" rel="noopener noreferrer">
              {result.title}
            </a>
          </h3>
          <p>{result.snippet}</p>
          <small>
            Relevance Score:{" "}
            {typeof result.score === "number" ? result.score.toFixed(2) : "N/A"}
          </small>
        </div>
      ))}
    </div>
  );
};

export default SearchResults;
