import React from "react";
import PropTypes from "prop-types";

const GitHubButton = ({ username, repoName , alternativeDescription}) => {
  const repoUrl = `https://github.com/${username}/${repoName}`;

  return (
    <a
      href={repoUrl}
      target="_blank"
      rel="noopener noreferrer"
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: "10px 20px",
        backgroundColor: "#24292e", // GitHub's default background color
        color: "#fff",
        textDecoration: "none",
        borderRadius: "5px",
        fontSize: "16px",
        fontWeight: "bold",
        cursor: "pointer",
        margin: "10px",
      }}
    >
       {"View on GitHub" ? alternativeDescription : repoName} 
    </a>
  );
};

GitHubButton.propTypes = {
  username: PropTypes.string.isRequired,
  repoName: PropTypes.string.isRequired,
  alternativeDescription: PropTypes.string,
};

export default GitHubButton;
