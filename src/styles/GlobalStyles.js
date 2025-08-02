import { createGlobalStyle } from 'styled-components';

export const GlobalStyles = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Inter', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow: hidden;
  }

  /* Colorblind-safe colors */
  :root {
    --primary-blue: #2563eb;
    --secondary-blue: #1d4ed8;
    --success-green: #059669;
    --warning-yellow: #d97706;
    --error-red: #dc2626;
    --neutral-gray: #6b7280;
    --light-gray: #f3f4f6;
    --dark-gray: #374151;
    --white: #ffffff;
    --black: #111827;
  }

  /* Scrollbar styling */
  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: var(--light-gray);
  }

  ::-webkit-scrollbar-thumb {
    background: var(--neutral-gray);
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: var(--dark-gray);
  }

  /* Focus styles for accessibility */
  *:focus {
    outline: 2px solid var(--primary-blue);
    outline-offset: 2px;
  }

  /* Button reset */
  button {
    border: none;
    background: none;
    cursor: pointer;
    font-family: inherit;
  }

  /* Input reset */
  input, select, textarea {
    font-family: inherit;
  }
`; 