import { ClerkProvider, SignedIn, SignedOut } from '@clerk/clerk-react';
import ProfilePage from './pages/profile';
import SignupPage from './pages/signup';
import ThemeProvider from './providers/theme';

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

export default function CloudApp() {
  if (!PUBLISHABLE_KEY) {
    return (
      <ThemeProvider>
        <div style={{ padding: '2rem', textAlign: 'center' }}>
          <h1>Configuration Error</h1>
          <p>Missing Publishable Key. Please set VITE_CLERK_PUBLISHABLE_KEY in your environment variables.</p>
        </div>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider>
      <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
        <SignedIn>
          <ProfilePage />
        </SignedIn>
        <SignedOut>
          <SignupPage />
        </SignedOut>
      </ClerkProvider>
    </ThemeProvider>
  );
}
