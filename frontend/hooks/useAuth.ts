import { useMutation } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import api, { getErrorMessage } from '@/lib/api';
import { useAuthStore } from '@/lib/auth';
import { useNotificationStore } from '@/lib/notifications';
import { API_ROUTES, APP_ROUTES } from '@/lib/constants';
import type { SignUpRequest, SignInRequest, AuthResponse } from '@/types/api';

export function useAuth() {
  const router = useRouter();
  const { setAuth, clearAuth, isAuthenticated, user } = useAuthStore();
  const { addNotification } = useNotificationStore();

  // Sign Up Mutation
  const signUpMutation = useMutation({
    mutationFn: async (data: SignUpRequest) => {
      const response = await api.post<AuthResponse>(API_ROUTES.SIGNUP, data);
      return response.data;
    },
    onSuccess: (data) => {
      addNotification('success', data.message || 'Account created successfully');
      router.push(APP_ROUTES.SIGNIN);
    },
    onError: (error) => {
      addNotification('error', getErrorMessage(error));
    },
  });

  // Sign In Mutation
  const signInMutation = useMutation({
    mutationFn: async (data: SignInRequest) => {
      const response = await api.post<AuthResponse>(API_ROUTES.SIGNIN, data);
      return response.data;
    },
    onSuccess: (data) => {
      if (data.user && data.accessToken && data.refreshToken) {
        setAuth(data.user, data.accessToken, data.refreshToken);
        addNotification('success', 'Signed in successfully');
        router.push(APP_ROUTES.DASHBOARD);
      }
    },
    onError: (error) => {
      addNotification('error', getErrorMessage(error));
    },
  });

  // Sign Out Mutation
  const signOutMutation = useMutation({
    mutationFn: async () => {
      const response = await api.post(API_ROUTES.SIGNOUT);
      return response.data;
    },
    onSuccess: () => {
      clearAuth();
      addNotification('success', 'Signed out successfully');
      router.push('/landing'); // Redirect to landing page
    },
    onError: (error) => {
      addNotification('error', getErrorMessage(error));
    },
  });

  return {
    isAuthenticated,
    user,
    signUp: signUpMutation.mutate,
    signIn: signInMutation.mutate,
    signOut: signOutMutation.mutate,
    isSigningUp: signUpMutation.isPending,
    isSigningIn: signInMutation.isPending,
    isSigningOut: signOutMutation.isPending,
    signInError: signInMutation.error,
    signUpError: signUpMutation.error,
    resetSignInError: signInMutation.reset,
    resetSignUpError: signUpMutation.reset,
  };
}
