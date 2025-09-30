import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the main page header', () => {
  render(<App />);
  const headerElement = screen.getByText(/AI E-commerce Assistant/i);
  expect(headerElement).toBeInTheDocument();
});